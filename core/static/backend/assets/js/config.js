(function () {
  var primary = localStorage.getItem("primary") || "#8e6d4a";
  var secondary = localStorage.getItem("secondary") || "#838383";

  window.CubaAdminConfig = {
    // Theme Primary Color
    primary: primary,
    // theme secondary color
    secondary: secondary,
  };
})();
