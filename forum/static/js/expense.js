$(document).ready(function () {
  $("#addExpense").on("click", (e) => {
    e.preventDefault();
    $("#addExpenseModalLabel").text("Add New Expense");

    $("#modalExpenseID").val("");
    $("#modalExpenseName").val("");
    $("#modalCategoryName").val("");
    $("#modalAmountName").val("");
    $("#modalExpenseDateName").val("");
    $("#modalNotesName").val("");
  });

  $(".updateExpense").on("click", (e) => {
    e.preventDefault();
    const $tableTr = $(e.target).closest("tr");
    $("#addExpenseModalLabel").text("Update Expense");

    $("#modalExpenseID").val($tableTr.find(".td-id").text());
    $("#modalExpenseName").val($tableTr.find(".td-expense-name").text());
    $("#modalCategoryName").val($tableTr.find(".td-category").text());
    $("#modalAmountName").val($tableTr.find(".td-amount").text());
    $("#modalExpenseDateName").val(
      $tableTr
        .find(".td-expense-date")
        .text()
        .trim()
        .split("/")
        .reverse()
        .join("-")
    );
    $("#modalNotesName").val($tableTr.find(".td-notes").text());
  });
});
