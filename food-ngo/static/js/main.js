(function () {
  "use strict";

  document.querySelectorAll('.navbar-nav a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var id = this.getAttribute("href");
      if (id.length > 1 && id.startsWith("#")) {
        var target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
          var nav = document.getElementById("mainNav");
          if (nav && nav.classList.contains("show")) {
            bootstrap.Collapse.getOrCreateInstance(nav).hide();
          }
        }
      }
    });
  });

  var forms = document.querySelectorAll(".needs-validation");
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  var dateInput = document.getElementById("preferred_date");
  if (dateInput && !dateInput.value) {
    var t = new Date();
    var y = t.getFullYear();
    var m = String(t.getMonth() + 1).padStart(2, "0");
    var d = String(t.getDate()).padStart(2, "0");
    dateInput.min = y + "-" + m + "-" + d;
  }
})();
