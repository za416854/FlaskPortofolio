$(document).ready(function () {
  $("#signup").on("click", function (e) {
    e.preventDefault();
    if (
      !$("#userID").val() ||
      !$("#password").val() ||
      !$("#confirmPassword").val() ||
      !$("#firstName").val() ||
      !$("#lastName").val() ||
      !$("#email").val() ||
      !$("#birthDate").val()
    ) {
      alert("Please enter required fields!");
      return;
    }
    if ($("#password").val() !== $("#confirmPassword").val()) {
      alert("The password is not identical with the confirmation password!");
      return;
    }
    const data = {
      userID: $("#userID").val() || "",
      password: $("#password").val() || "",
      firstName: $("#firstName").val() || "",
      lastName: $("#lastName").val() || "",
      email: $("#email").val() || "",
      birthDate: $("#birthDate").val().replace(/-/g, '/') || "",
      mobile: $("#mobile").val() || "",
    };
    fetch("/signup", {
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
