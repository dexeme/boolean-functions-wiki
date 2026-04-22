from sage.all import *
from itertools import product


def compute_dual_basis(alpha, F, n):
    """
    Compute the dual basis θ of a given basis α.

    Given a basis α = {α_1, ..., α_n} over F_2, compute the dual basis θ = {θ_1, ..., θ_n}
    such that Tr(α_i * θ_j) = δ_{i,j} (Kronecker delta), where Tr is the trace function.

    Args:
        alpha: List of basis elements in F
        F: The finite field F_{2^n}
        n: The dimension

    Returns:
        List of dual basis elements
    """
    # Build the trace matrix
    trace_matrix = matrix(GF(2), n, n)
    for i in range(n):
        for j in range(n):
            # Compute Tr(α_i * α_j)
            element = alpha[i] * alpha[j]
            # Trace in characteristic 2 is computed as sum of Frobenius powers
            trace_val = 0
            temp = element
            for _ in range(n):
                trace_val += temp
                temp = temp ** 2
            trace_matrix[i, j] = int(trace_val)

    # Invert the trace matrix to get dual basis
    try:
        inv_matrix = trace_matrix.inverse()
    except ZeroDivisionError:
        print("Error: Trace matrix is singular. The basis may be linearly dependent.")
        return None

    # Compute dual basis elements
    theta = []
    for j in range(n):
        # θ_j = sum_i (inv_matrix[i,j] * α_i)
        theta_j = F(0)
        for i in range(n):
            if inv_matrix[i, j] == 1:
                theta_j += alpha[i]
        theta.append(theta_j)

    return theta


def compute_quadratic_coefficients(H, theta, n):
    """
    Compute the coefficients c_{i,t} of the quadratic function F(x).

    Using the formula: c_{i,t} = sum_{1 ≤ u,v ≤ n} θ_u^{2^{i-1}} * θ_v^{2^{t-1}} * h_{u,v}

    Args:
        H: The n×n matrix over F_{2^n}
        theta: The dual basis {θ_1, ..., θ_n}
        n: The dimension

    Returns:
        Dictionary with keys (i, t) and values c_{i,t}
    """
    coefficients = {}

    for i in range(1, n + 1):
        for t in range(1, i):  # Only for t < i
            c_it = 0
            for u in range(1, n + 1):
                for v in range(1, n + 1):
                    # Compute θ_u^{2^{i-1}}
                    theta_u_power = theta[u - 1] ** (2 ** (i - 1))
                    # Compute θ_v^{2^{t-1}}
                    theta_v_power = theta[v - 1] ** (2 ** (t - 1))
                    # Add the term to the coefficient
                    c_it += theta_u_power * theta_v_power * H[u - 1, v - 1]

            coefficients[(i, t)] = c_it

    return coefficients


def build_quadratic_function(coefficients, F, n, var='x'):
    """
    Build the quadratic function F(x) from the coefficients.

    F(x) = sum_{1 ≤ t < i ≤ n} c_{i,t} * x^{2^{i-1} + 2^{t-1}}

    Args:
        coefficients: Dictionary with keys (i, t) and values c_{i,t}
        F: The finite field F_{2^n}
        n: The dimension
        var: The variable name (default 'x')

    Returns:
        The polynomial representing F(x)
    """
    R = PolynomialRing(F, var)
    x = R.gen()

    F_x = R(0)
    for (i, t), c_it in coefficients.items():
        if c_it != 0:
            exponent = 2 ** (i - 1) + 2 ** (t - 1)
            F_x += c_it * (x ** exponent)

    return F_x


def extract_quadratic_function(H, F, n, alpha=None):
    """
    Extract the quadratic function F(x) from a given matrix H over F_{2^n}.

    Args:
        H: The n×n matrix over F_{2^n}
        F: The finite field F_{2^n}
        n: The dimension
        alpha: The basis to use (if None, uses the default basis of F)

    Returns:
        The quadratic function as a polynomial, and the coefficients
    """
    # If no basis is provided, use the default basis (powers of the generator)
    if alpha is None:
        gen = F.gen()
        alpha = [gen ** i for i in range(n)]

    # Compute the dual basis
    theta = compute_dual_basis(alpha, F, n)
    if theta is None:
        return None, None

    # Compute the coefficients
    coefficients = compute_quadratic_coefficients(H, theta, n)

    # Build the quadratic function
    F_x = build_quadratic_function(coefficients, F, n)

    return F_x, coefficients


def generate_qam(i, H, S, n):
    e_i_vec = [0] * (n - 1)
    e_i_vec[i - 1] = 1
    e_i = tuple(e_i_vec)

    if i == n - 1:
        for x_i in S[e_i]:
            H_new = copy(H)
            H_new[n - 1, n - 2] = x_i
            H_new[n - 2, n - 1] = x_i
            yield H_new
    else:
        for x_i in S[e_i]:
            H_new = copy(H)
            H_new[n - 1, i - 1] = x_i
            H_new[i - 1, n - 1] = x_i

            S_prime = S.copy()

            for bits in product([0, 1], repeat=n - 1 - i):
                if any(bits):
                    suffix = list(bits)
                    lambda_vec = [0] * i + suffix
                    lambda_tuple = tuple(lambda_vec)

                    lambda_xor_ei = list(lambda_vec)
                    lambda_xor_ei[i - 1] ^= 1
                    lambda_xor_ei_tuple = tuple(lambda_xor_ei)

                    if lambda_tuple in S and lambda_xor_ei_tuple in S:
                        S_prime[lambda_tuple] = S[lambda_tuple].intersection(S[lambda_xor_ei_tuple])

            yield from generate_qam(i + 1, H_new, S_prime, n)


def solve_problem_1(H_initial, n, F):
    A = H_initial.submatrix(0, 0, n - 1, n - 1)
    S = {}

    for bits in product([0, 1], repeat=n - 1):
        if not any(bits):
            continue

        lambda_vec = vector(GF(2), bits)

        sum_lambda_A = vector(F, [0] * (n - 1))
        for j in range(n - 1):
            if lambda_vec[j] == 1:
                sum_lambda_A += A.row(j)

        span_set = {F(0)}
        element = sum_lambda_A[0]
        if element != 0:
            for c in GF(2):
                span_set.add(F(c * element))

        S[tuple(bits)] = set(F) - span_set

    return generate_qam(1, H_initial, S, n)



if __name__ == "__main__":
    n_val = 4
    F_2n = GF(2 ** n_val, 'x')

    # Create a test matrix H
    H_test = matrix(F_2n, n_val, n_val, 0)
    for i in range(n_val - 1):
        H_test[i, i] = F_2n.random_element()

    print(f"Initial matrix H ((n-1)x(n-1) submatrix populated):")
    print(H_test)
    print("-" * 50)

    # Extract the quadratic function from H
    print("\n=== Extracting Quadratic Function from Initial Matrix H ===\n")
    F_x, coefficients = extract_quadratic_function(H_test, F_2n, n_val)

    if F_x is not None:
        print("Quadratic Function F(x):")
        print(F_x)
        print("\nCoefficients c_{i,t}:")
        for (i, t), c_it in sorted(coefficients.items()):
            print(f"  c_{{{i},{t}}} = {c_it}")
    else:
        print("Could not extract the quadratic function.")

    print("\n" + "=" * 50)
    print("=== Generating QAM Matrices and Their Functions ===")
    print("=" * 50 + "\n")

    results = list(solve_problem_1(H_test, n_val, F_2n))

    print(f"Found {len(results)} QAM matrices.\n")

    # Extract and print all quadratic functions from each QAM matrix
    F_functions = []
    for idx, H_matrix in enumerate(results, 1):
        print(f"\n{'─' * 50}")
        print(f"QAM Matrix #{idx}:")
        print(H_matrix)

        # Extract the quadratic function from this matrix
        F_x_i, coeffs_i = extract_quadratic_function(H_matrix, F_2n, n_val)

        if F_x_i is not None:
            print(f"\nCorresponding Quadratic Function F_{idx}(x):")
            print(f"F_{idx}(x) = {F_x_i}")
            F_functions.append((idx, F_x_i, coeffs_i))
        else:
            print(f"Could not extract the quadratic function for matrix #{idx}")

    for idx, F_func, _ in F_functions:
        print(f"F_{idx}(x) = {F_func}")

    print(f"\nTotal of {len(F_functions)} quadratic functions extracted.")

