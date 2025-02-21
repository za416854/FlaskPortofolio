$(document).ready(function () {
  $("#forgotPassword").on("click", function (e) {
    e.preventDefault(); // Block default behavior
    if (!$("#email").val() || !$("#userID").val() || !$("#birthDate").val()|| !$("#password").val()|| !$("#confirmPassword").val()) {
      alert("Please enter required fields!");
      return;
    }
    if ($("#password").val() !== $("#confirmPassword").val()) {
      alert("The password is not identical with the confirmation password!");
      return;
    }
    const data = {
      email: $("#email").val() || "",
      userID: $("#userID").val() || "",
      birthDate: $("#birthDate").val().replace(/-/g, '/')  || "",
      password: $("#password").val() || "",
      confirmPassword: $("#confirmPassword").val() || "",
    }; 
    fetch("/forgot_password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.message); // throw error
          });
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message);
        window.location.href = "/login";
      })
      .catch((error) => {
        alert(error.message);
      });
  });
});
