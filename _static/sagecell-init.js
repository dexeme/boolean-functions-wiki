(function () {
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function initSageCells() {
    if (!window.sagecell || typeof window.sagecell.makeSagecell !== "function") return;

    var cells = document.querySelectorAll(".sagecell");
    for (var i = 0; i < cells.length; i++) {
      var el = cells[i];
      if (el.getAttribute("data-sagecell-initialized") === "1") continue;
      el.setAttribute("data-sagecell-initialized", "1");

      var server = el.getAttribute("data-sagecell-server") || "https://sagecell.sagemath.org";
      var autoeval = (el.getAttribute("data-sagecell-autoeval") || "false").toLowerCase() === "true";

      var input = el.querySelector("textarea.sagecell-input") || el.querySelector("textarea");
      var output = el.querySelector(".sagecell-output");
      if (!input) continue;

      input.value = input.defaultValue;

      window.sagecell.makeSagecell({
        inputLocation: input,
        outputLocation: output || undefined,
        evalButtonText: "Run",
        autoeval: autoeval,
        server: server,
      });
    }
  }

  function ensureEmbeddedLoadedThenInit() {
    if (window.sagecell && typeof window.sagecell.makeSagecell === "function") {
      initSageCells();
      return;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureEmbeddedLoadedThenInit);
  } else {
    ensureEmbeddedLoadedThenInit();
  }

  window.addEventListener("pageshow", function (e) {
    if (!e || !e.persisted) return;
    var cells = document.querySelectorAll(".sagecell");
    for (var i = 0; i < cells.length; i++) {
      cells[i].removeAttribute("data-sagecell-initialized");
      var input = cells[i].querySelector("textarea.sagecell-input") || cells[i].querySelector("textarea");
      if (input) input.value = input.defaultValue;
    }
    ensureEmbeddedLoadedThenInit();
  });
})();
