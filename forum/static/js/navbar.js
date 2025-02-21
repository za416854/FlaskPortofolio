// Handle logout logic
$(document).ready(function () {
  $("#authLink").on("click", function (e) {
    e.preventDefault();
    if ($(this).text().trim() === "Logout") {
      fetch("/logout", { method: "POST" }).then((response) => {
        if (response.ok) {
          window.location.href = "/home";
        } else {
          console.error("logout failed" + error);
          window.location.href = "/login";
        }
      });
    } else {
      window.location.href = "/login";
    }
  });
});
