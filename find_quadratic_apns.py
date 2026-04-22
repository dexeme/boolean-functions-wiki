from sage.all import *
import argparse

class QAMSearcher:
    def __init__(self, m, modulus=None):
        if m <= 2:
            raise ValueError("Require m > 2")

        self.m = m
        self.n = 2 * m - 1
        self.F2 = GF(2)

        if modulus is None:
            self.F = GF(2**self.n, name='a')
        else:
            self.F = GF(2**self.n, name='a', modulus=modulus)

        self.zero = self.F(0)
        self.one = self.F(1)

        self.V, self.from_V, self.to_V = self.F.vector_space(map=True)

        self.alpha_basis, self.theta_basis = self._build_normal_and_dual_basis()

        self.M_alpha = Matrix(
            self.F, self.n, self.n,
            lambda i, u: self.alpha_basis[u] ** (2**i)
        )
        self.M_theta = Matrix(
            self.F, self.n, self.n,
            lambda i, u: self.theta_basis[u] ** (2**i)
        )

    # ============================================================
    # Helpers
    # ============================================================
    def poly_exponents(self, poly):
        return sorted(poly.exponents())

    def frobenius_orbit_of_exponents(self, exps):
        mod = 2 ** self.n - 1
        orbit = []

        current = tuple(sorted(exps))
        seen = set()

        for _ in range(self.n):
            if current in seen:
                break
            seen.add(current)
            orbit.append(current)
            current = tuple(sorted((2 * e) % mod for e in current))

        return orbit

    def canonicalize_poly(self, poly):
        exps = list(poly.exponents())
        orbit = self.frobenius_orbit_of_exponents(exps)
        best = min(orbit)

        R = PolynomialRing(self.F2, 'x')
        x = R.gen()
        out = R(0)
        for e in best:
            out += x ** e
        return out

    def field_vector(self, x):
        return self.to_V(self.F(x))

    def span_rank(self, elems):
        vecs = [self.field_vector(x) for x in elems]
        if not vecs:
            return 0
        return Matrix(self.F2, vecs).rank()

    def vector_rank_over_F2(self, row):
        return self.span_rank(row)

    def gf2_span_set(self, elems):
        elems = [self.F(x) for x in elems]
        if not elems:
            return {self.zero}
        sub = self.V.subspace([self.to_V(x) for x in elems])
        return {self.from_V(v) for v in sub}

    def nonzero_field_elements(self):
        return [x for x in self.F if x != 0]

    def _is_normal_element(self, beta):
        conj = [beta ** (2**k) for k in range(self.n)]
        return self.span_rank(conj) == self.n

    def _build_normal_and_dual_basis(self):
        beta = None
        for x in self.F:
            if x != 0 and self._is_normal_element(x):
                beta = x
                break

        if beta is None:
            raise RuntimeError("Could not find a normal element")

        alpha = [beta ** (2**k) for k in range(self.n)]

        G = Matrix(
            self.F2, self.n, self.n,
            lambda i, j: self.F2((alpha[i] * alpha[j]).trace())
        )
        Ginv = G.inverse()

        theta = []
        for j in range(self.n):
            tj = self.zero
            for l in range(self.n):
                if Ginv[l, j] == 1:
                    tj += alpha[l]
            theta.append(tj)

        theta0 = theta[0]
        theta = [theta0 ** (2**i) for i in range(self.n)]

        return alpha, theta

    # ============================================================
    # QAM / proper
    # ============================================================

    def linear_combination_of_rows(self, rows, mask):
        r = len(rows)
        k = len(rows[0])
        out = [self.zero for _ in range(k)]
        for i in range(r):
            if (mask >> i) & 1:
                for j in range(k):
                    out[j] += rows[i][j]
        return out

    def is_proper(self, A):
        m = len(A)
        if m == 0:
            return True
        k = len(A[0])

        for mask in range(1, 2**m):
            row = self.linear_combination_of_rows(A, mask)
            if self.vector_rank_over_F2(row) < k - 1:
                return False
        return True

    def is_qam(self, H):
        for i in range(self.n):
            if H[i][i] != 0:
                return False
            for j in range(self.n):
                if H[i][j] != H[j][i]:
                    return False

        for mask in range(1, 2**self.n):
            row = self.linear_combination_of_rows(H, mask)
            if self.vector_rank_over_F2(row) != self.n - 1:
                return False
        return True

    # ============================================================
    # Teorema 2
    # ============================================================

    def H_list_to_matrix(self, H):
        return Matrix(self.F, self.n, self.n, lambda i, j: H[i][j])

    def matrix_to_polynomial(self, H, var='x'):
        Hmat = self.H_list_to_matrix(H)
        CF = self.M_theta * Hmat * self.M_theta.transpose()

        R = PolynomialRing(self.F2, var)
        x = R.gen()
        poly = R(0)

        for i in range(self.n):
            for t in range(i):
                cij = CF[i, t]
                if cij not in self.F2:
                    raise ValueError(f"Coefficient c_{{{i},{t}}} = {cij} is not in GF(2)")
                if self.F2(cij) == 1:
                    poly += x ** (2**i + 2**t)

        return poly

    # ============================================================
    # Construção correta da matriz a partir dos parâmetros da 1a linha
    # ============================================================

    def build_H_from_first_row_params(self, params):
        """
        params[k] representa H[0][k+1], isto é:
          params[0] = H[0][1]
          params[1] = H[0][2]
          ...
        Pode receber prefixos parciais durante a recursão.
        """

        H = [[self.zero for _ in range(self.n)] for _ in range(self.n)]

        # só usa os parâmetros realmente disponíveis
        for d in range(1, len(params) + 1):
            w = self.F(params[d - 1])

            H[0][d] = w
            H[d][0] = w

            for t in range(1, self.n):
                u = t
                v = (d + t) % self.n
                pu = t - 1
                pv = (d + t - 1) % self.n

                H[u][v] = H[pu][pv] ** 2
                H[v][u] = H[u][v]

        return H

    # ============================================================
    # Algoritmo 1: representantes de Frobenius
    # ============================================================

    def get_none_square(self):
        remaining = set(self.nonzero_field_elements())
        reps = set()

        while remaining:
            x = next(iter(remaining))
            orbit = set()
            y = x
            for _ in range(self.n):
                orbit.add(y)
                y = y ** 2

            rep = min(orbit, key=lambda z: tuple(self.field_vector(z)))
            reps.add(rep)
            remaining -= orbit

        return sorted(reps, key=lambda z: tuple(self.field_vector(z)))

    def get_elm_c(self, j, params):
        """
        j é 1-based como no paper, com 2 <= j <= m
        params guarda [H[0][1], H[0][2], ..., H[0][j-2]]
        """

        resu = set(self.nonzero_field_elements())

        if j == 2:
            return self.get_none_square()

        # Reconstrói a matriz parcial a partir dos parâmetros já escolhidos
        H_partial = self.build_H_from_first_row_params(params)

        # No paper:
        # S = Span({H[1, i], H[1, n + 2 - i] : i in [2..j-1]})   (1-based)
        # Em 0-based:
        # H[0][i-1] e H[0][n+1-i]
        gens = []
        for i in range(2, j):
            gens.append(H_partial[0][i - 1])
            gens.append(H_partial[0][self.n + 1 - i])

        S = self.gf2_span_set(gens)

        if len(S) < 2 ** (2 * j - 4):
            return []

        resu -= S

        good = []
        for r in sorted(resu, key=lambda z: tuple(self.field_vector(z))):
            trial_params = list(params) + [r]
            H = self.build_H_from_first_row_params(trial_params)

            # No paper:
            # A = Submatrix(H, 1, 1, j-1, j)   (1-based)
            # Em 0-based: primeiras (j-1) linhas e primeiras j colunas
            A = [row[:j] for row in H[:j - 1]]

            if self.is_proper(A):
                good.append(r)

        return good

    def search_recursive(self, j, params, out_polys, out_seen, output_fp=None, max_results=None):
        if max_results is not None and len(out_polys) >= max_results:
            return

        candidates = self.get_elm_c(j, params)

        if j == self.m:
            for w in candidates:
                if max_results is not None and len(out_polys) >= max_results:
                    return
                full_params = list(params) + [w]
                H = self.build_H_from_first_row_params(full_params)
                if self.is_qam(H):
                    poly = self.matrix_to_polynomial(H)
                    canon = self.canonicalize_poly(poly)
                    canon_str = str(canon)
                    if canon_str not in out_seen:
                        out_seen.add(canon_str)
                        out_polys.append(canon_str)
                        if output_fp is not None:
                            output_fp.write(canon_str + "\n")
                            output_fp.flush()
            return

        for w in candidates:
            if max_results is not None and len(out_polys) >= max_results:
                return
            self.search_recursive(
                j + 1,
                list(params) + [w],
                out_polys,
                out_seen,
                output_fp=output_fp,
                max_results=max_results
            )

    def search(self, max_results=None, output_path=None):
        out_polys = []
        out_seen = set()

        output_fp = None
        if output_path is not None:
            try:
                with open(output_path, "r", encoding="utf-8") as f_in:
                    for line in f_in:
                        poly_line = line.strip()
                        if poly_line and poly_line not in out_seen:
                            out_seen.add(poly_line)
                            out_polys.append(poly_line)
            except FileNotFoundError:
                pass
            output_fp = open(output_path, "a", encoding="utf-8")

        try:
            self.search_recursive(
                2, [], out_polys, out_seen, output_fp=output_fp, max_results=max_results
            )
        finally:
            if output_fp is not None:
                output_fp.close()

        return out_polys

    # ============================================================
    # Grafo e código associado
    # ============================================================

    def poly_to_function_table(self, poly):
        """
        Retorna [(x, F(x)) for x in F_{2^n}]
        """
        return [(x, self.F(poly(x))) for x in self.F]

    def graph_columns_binary(self, poly):
        """
        Cada coluna é:
            (1, coords(x), coords(F(x))) em F2^(1+2n)
        """
        cols = []
        for x in self.F:
            xv = list(self.field_vector(x))
            y = self.F(poly(x))
            yv = list(self.field_vector(y))
            col = vector(self.F2, [1] + xv + yv)
            cols.append(col)
        return cols

    def graph_generator_matrix(self, poly):
        """
        Matriz geradora do código associado ao grafo.
        Dimensão de linhas: 1 + 2n
        Número de colunas: 2^n
        """
        cols = self.graph_columns_binary(poly)
        return Matrix(self.F2, 1 + 2 * self.n, len(cols), lambda i, j: cols[j][i])

    def graph_code(self, poly):
        """
        Código linear binário associado ao grafo de F.
        """
        G = self.graph_generator_matrix(poly)
        return LinearCode(G)

    # ============================================================
    # Invariantes do código
    # ============================================================

    def safe_weight_distribution(self, C):
        """
        Para n pequeno funciona bem.
        """
        wd = C.weight_distribution()
        return tuple(int(v) for v in wd)

    def graph_code_signature(self, poly):
        """
        Assinatura forte baseada no código associado ao grafo.
        Não é prova de equivalência CCZ, mas é bem melhor que
        só usar órbita de Frobenius ou derivadas.
        """
        canon = self.canonicalize_poly(poly)
        C = self.graph_code(canon)

        return (
            C.length(),
            C.dimension(),
            self.safe_weight_distribution(C),
        )

    def canonical_poly_string(self, poly):
        return str(self.canonicalize_poly(poly))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QAM polynomial search")
    parser.add_argument("-m", type=int, default=3, help="Parameter m (>2), n=2m-1")
    parser.add_argument("-p", type=int, default=None, help="Stop after finding the first p functions")
    parser.add_argument("-o", "--output", default="output.txt", help="Output file to append found functions")
    args = parser.parse_args()
    if args.p is not None and args.p <= 0:
        parser.error("-p must be a positive integer")

    S = QAMSearcher(args.m)
    polys = S.search(max_results=args.p, output_path=args.output)
    print("Polinomios encontrados:", len(polys))
    for poly in polys:
        print(poly)
