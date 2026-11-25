(function () {
  var root = document.documentElement;
  var stored = localStorage.getItem("theme");
  if (stored) root.setAttribute("data-theme", stored);

  function toggleTheme() {
    var current = root.getAttribute("data-theme");
    var isLight = current === "light";
    var next = isLight ? "dark" : "light";
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".theme-toggle");
    if (btn) btn.addEventListener("click", toggleTheme);

    var navToggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    if (navToggle && nav) {
      navToggle.addEventListener("click", function () {
        nav.classList.toggle("open");
      });
    }

    var filters = document.querySelectorAll(".pub-filter");
    var items = document.querySelectorAll(".pub-item");
    var years = document.querySelectorAll(".pub-year");
    if (filters.length) {
      filters.forEach(function (filter) {
        filter.addEventListener("click", function () {
          filters.forEach(function (f) { f.classList.remove("active"); });
          filter.classList.add("active");
          var type = filter.getAttribute("data-type");

          items.forEach(function (item) {
            var match = type === "all" || item.getAttribute("data-type") === type;
            item.style.display = match ? "" : "none";
          });

          years.forEach(function (year) {
            var grid = year.nextElementSibling;
            var hasVisible = false;
            if (grid && grid.classList && grid.classList.contains("pub-grid")) {
              grid.querySelectorAll(".pub-item").forEach(function (item) {
                if (item.style.display !== "none") hasVisible = true;
              });
            }
            year.style.display = hasVisible ? "" : "none";
          });
        });
      });
    }
  });
})();
