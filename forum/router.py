import base64
import requests
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
)
from forum import app, db
from forum.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
import json
from forum.utilities.datetime import *

app.secret_key = "your_secret_key"


# direct to home page
@app.route("/")
@app.route("/home")
def home():
    try:
        posts = Posts.get_all_posts(db)  # Get all posts
        res_data = []

        for post in posts:
            post_data = {
                "id": post.ID,
                "userID": post.UserID,
                "title": post.Title,
                "content": (
                    post.Content[:40] + "..."
                    if len(post.Content) > 40
                    else post.Content
                ),  # Make sure the content is not too long
            }
            res_data.append(post_data)

        return render_template("home.html", questions=res_data)
    except Exception as e:
        print(f"Exception caught: {e}")

# direct to about page
@app.route("/about")
def about():
    try:
        abouts = About.get_abouts(db)
        # Categorise data based on AboutType
        about_dict = {
            "Description": [],
            "Languages": [],
            "Education": [],
            "Frameworks": [],
            "Database": [],
            "Others": [],
        }

        for about in abouts:
            if about.AboutType == "Description":
                about_dict["Description"].append(about.AboutDesc)
            elif about.AboutType == "Education":
                about_dict["Education"].append(about.AboutDesc)
            elif about.AboutType == "Languages":
                about_dict["Languages"].append(about.AboutDesc)
            elif about.AboutType == "Frameworks":
                about_dict["Frameworks"].append(about.AboutDesc)
            elif about.AboutType == "Database":
                about_dict["Database"].append(about.AboutDesc)
            elif about.AboutType == "Others":
                about_dict["Others"].append(about.AboutDesc)

        # Pass data to template
        return render_template("about.html", about_dict=about_dict)
    except Exception as e:
        print(f"Exception caught: {e}")


# direct to login page/ login function
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user_id = request.form["userID"]
            password = request.form["password"]
            user = UserInfo.get_userinfo_by_id(user_id, db=db)
            if not user or user is None:
                flash("This user is not found, sign up to log in!")
                return redirect(url_for("login"))
            is_right_password = check_password_hash(user.Password, password)
            if is_right_password:
                session["user"] = user_id
                login_user(user, remember=True)
                flash("You have logged in now!")
                return redirect(url_for("home"))
            else:
                flash("The account or password is wrong, please re-enter it!")
                return redirect(url_for("login"))
        return render_template("login.html")
    except Exception as e:
        print(f"Exception caught: {e}")


# log out function
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        logout_user()
        session.pop("user", None)  # Clear user information in session
        flash(f"You have successfully logged out!")
        return redirect(url_for("home"))
    except Exception as e:
        print(f"Exception caught: {e}")


# direct to signup page/ signup function
@app.route("/signup", methods=["GET", "POST"])
def signup():
    try:
        # print(f"request.content_type: {request.content_type}")
        if request.method == "POST":
            data = request.get_json()

            user_id = data.get("userID")
            password = data.get("password")
            hashed_password = generate_password_hash(password)
            firstName = data.get("firstName")
            lastName = data.get("lastName")
            email = data.get("email")
            birthDate = data.get("birthDate")
            mobile = data.get("mobile")
            res = UserInfo.add_userinfo(
                user_id,
                hashed_password,
                firstName,
                lastName,
                email,
                birthDate,
                mobile,
                db,
            )
            if res == "UserExists":
                # return flash(f"User exists! Try to use another user ID")
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "User exists! Try to use another user ID",
                        }
                    ),
                    400,
                )
            else:
                return jsonify(
                    {"status": "success", "message": "User registered successfully!"}
                )
        else:
            return render_template("signup.html")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# direct to account page/ update account function
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    try:
        # print(f"request.content_type: {request.content_type}")
        user_id = session["user"]
        user = UserInfo.get_userinfo_by_id(user_id, db=db)
        if request.method == "POST":
            user_id = request.form.get("userID")
            firstName = request.form.get("firstName")
            lastName = request.form.get("lastName")
            email = request.form.get("email")
            birthDate = date_convert_to_yyyyMMddstr(request.form.get("birthDate"))
            mobile = request.form.get("mobile")
            res = UserInfo.update_userinfo(
                user,
                firstName,
                lastName,
                email,
                birthDate,
                mobile,
                db,
            )
            if res:
                flash("User information successfully Updated!")
                return redirect(url_for("home"))
            else:
                flash("Updated failed, try agaain!")
                return redirect(url_for("home"))
        else:
            user_list = []
            user_list.append(
                {
                    "userID": f"{user.UserID}",
                    "firstName": f"{user.FirstName}",
                    "lastName": f"{user.LastName}",
                    "email": f"{user.Email}",
                    "birthDate": f"{user.BirthDate.replace('/', '-')}",
                    "mobile": f"{user.Mobile}",
                }
            )
            return render_template("account.html", user_list=user_list)
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# direct to forgot password page/ forgot password function
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    try:
        if request.method == "POST":
            data = request.get_json()
            email = data.get("email")
            userID = data.get("userID")
            birthday = data.get("birthDate")
            new_password = data.get("password")

            # check whether user ID exists!
            user = (
                db.session.query(UserInfo)
                .filter_by(Email=email, UserID=userID, BirthDate=birthday)
                .first()
            )
            if not user:
                return jsonify(
                    {
                        "status": "error",
                        "message": "User ID, Email or Birthday is incorrect.",
                    }
                )
            user.Password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify(
                {
                    "status": "success",
                    "message": "Password recovery successful. Try to user new password to log in now.",
                }
            )
        return render_template("forgot_password.html")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# direct to post page/ post function
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    try:
        if "user" in session:
            if request.method == "POST":
                title = request.form.get("title")
                content = request.form.get("content")
                photo = request.files.get("photo")
                photo_binary = photo.read() if photo else None
                user_id = session["user"]
                user = UserInfo.get_userinfo_by_id(user_id, db=db)
                Posts.add_post(db, user_id, title, content, photo_binary)
                flash(
                    f"Post submitted: user name is {user.FirstName}, title is {title}"
                )
                return redirect(url_for("home"))
            return render_template("post.html")
        return render_template("home.html")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# direct to question page/ question function
@app.route("/question/<int:post_id>", methods=["GET", "POST"])
def question(post_id):
    try:
        post = Posts.get_post_by_id(db, post_id)
        post_list = []
        post_list.append(
            {
                "id": post.ID,
                "userID": f"{post.UserID}",
                "title": post.Title,
                "content": post.Content,
                "photo": (
                    base64.b64encode(post.Photo).decode("utf-8") if post.Photo else None
                ),
                "createDate": (
                    dateTime_convert_to_ddMMyyyyHHMMssStr(post.CreateDate)
                    if post.CreateDate
                    else "no time set"
                ),
            }
        )

        user_id = post.UserID
        comments = Comments.get_comments_by_post_id(post_id, db)
        comment_list = []
        for comment in comments:
            comment_list.append(
                {
                    "id": comment.ID,
                    "userID": comment.UserID,
                    "firstName": comment.FirstName,
                    "lastName": comment.LastName,
                    "commentText": comment.Comment_Text,
                    "createDate": (
                        dateTime_convert_to_ddMMyyyyHHMMssStr(comment.CreateDate)
                        if comment.CreateDate
                        else "no time set"
                    ),
                }
            )
        if request.method == "POST":
            if "user" in session:
                new_comment = request.form.get("comment")
                if new_comment == None or new_comment.strip() == "":
                    flash(f"comment cannot be empty or space!")
                    return render_template(
                        "question.html",
                        post_id=post_id,
                        posts=post_list,
                        comments=comment_list,
                    )
                post_id = post.ID
                user_id = session["user"]
                res = Comments.add_comment(post_id, user_id, new_comment, db)
                if res:
                    new_comment_list = []
                    for comment in Comments.get_comments_by_post_id(post_id, db):
                        new_comment_list.append(
                            {
                                "id": comment.ID,
                                "userID": comment.UserID,
                                "firstName": comment.FirstName,
                                "lastName": comment.LastName,
                                "commentText": comment.Comment_Text,
                                "createDate": (
                                    dateTime_convert_to_ddMMyyyyHHMMssStr(
                                        comment.CreateDate
                                    )
                                    if comment.CreateDate
                                    else "no time set"
                                ),
                            }
                        )
                    flash(f"Successfully posted a comment!")
                    return render_template(
                        "question.html",
                        post_id=post_id,
                        posts=post_list,
                        comments=new_comment_list,
                    )
                else:
                    flash(f"Some problems occured, please leave a comment again!")
                    return render_template(
                        "question.html",
                        post_id=post_id,
                        posts=post_list,
                        comments=comment_list,
                    )
            else:
                flash(f"Please log in to leave comments!")
                return render_template(
                    "question.html",
                    post_id=post_id,
                    posts=post_list,
                    comments=comment_list,
                )
        else:
            return render_template(
                "question.html", posts=post_list, comments=comment_list
            )
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# delete post function
@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    try:
        if "user" in session:
            user_id = session["user"]
            # search the article
            post = Posts.get_post_by_id(db, post_id)
            # Check whether the article exists and the matches UserID
            if post and post.UserID == user_id:
                Posts.delete_post(db, post_id)
                flash("Post deleted successfully!")
            else:
                flash("You are not authorized to delete this post.")
            return redirect(url_for("home"))
        else:
            flash("Please log in to delete a post.")
            return redirect(url_for("login"))
    except Exception as e:
        db.session.rollback()
        print(f"Exception caught: {e.args[0]}")


# direct to expense page
@app.route("/expense")
@login_required
def expense():
    try:
        user_id = session["user"]
        expenses = Expense.get_expense_by_userID(
            user_id, db
        )  # Get all expense information from database by user id
        res_data = []
        for expense in expenses:
            data = {
                "ID": expense.ID,
                "userID": expense.UserID,
                "expenseName": expense.ExpenseName,
                "category": expense.Category,
                "amount": expense.Amount,
                "expenseDate": (
                    dateTime_convert_to_ddMMyyyystr(expense.ExpenseDate)
                    if expense.ExpenseDate
                    else "no time set"
                ),
                "notes": expense.Notes,
                "createDate": (
                    dateTime_convert_to_ddMMyyyyHHMMssStr(expense.CreateDate)
                    if expense.CreateDate
                    else "no time set"
                ),
                "updateDate": (
                    dateTime_convert_to_ddMMyyyyHHMMssStr(expense.UpdateDate)
                    if expense.UpdateDate
                    else "no time set"
                ),
            }
            res_data.append(data)
        categories = set(expense.Category for expense in expenses)
        # expenses = []
        return render_template("expense.html", expenses=res_data, categories=categories)
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# get expenses by interval function
@app.route("/expense/get_expenses_by_interval", methods=["POST"])
def get_expenses_by_interval():
    try:
        start_date = date_convert_to_yyyyMMddstr(request.form["startDate"]).replace(
            "/", "-"
        )
        end_date = date_convert_to_yyyyMMddstr(request.form["endDate"]).replace(
            "/", "-"
        )
        expenses = Expense.get_expenses_by_interval(start_date, end_date, db)
        user_id = session["user"]
        res_data = []
        for expense in expenses:
            if user_id == expense.UserID:
                data = {
                    "ID": expense.ID,
                    "userID": expense.UserID,
                    "expenseName": expense.ExpenseName,
                    "category": expense.Category,
                    "amount": expense.Amount,
                    "expenseDate": (
                        date_convert_to_ddMMyyyystr(expense.ExpenseDate)
                        if expense.ExpenseDate
                        else "no time set"
                    ),
                    "notes": expense.Notes,
                    "createDate": (
                        dateTime_convert_to_ddMMyyyyHHMMssStr(expense.CreateDate)
                        if expense.CreateDate
                        else "no time set"
                    ),
                    "updateDate": (
                        dateTime_convert_to_ddMMyyyyHHMMssStr(expense.UpdateDate)
                        if expense.UpdateDate
                        else "no time set"
                    ),
                }
                res_data.append(data)
        return render_template("expense.html", expenses=res_data)

    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# last 30 days search
@app.route("/expense/get_expenses_last_30_days", methods=["POST"])
def get_expenses_last_30_days():
    try:
        expenses = Expense.get_expenses_last_30_days(db)
        user_id = session["user"]
        res_data = []
        for expense in expenses:
            if user_id == expense.UserID:
                data = {
                    "ID": expense.ID,
                    "userID": expense.UserID,
                    "expenseName": expense.ExpenseName,
                    "category": expense.Category,
                    "amount": expense.Amount,
                    "expenseDate": (
                        dateTime_convert_to_ddMMyyyystr(expense.ExpenseDate)
                        if expense.ExpenseDate
                        else "no time set"
                    ),
                    "notes": expense.Notes,
                    "createDate": (
                        dateTime_convert_to_ddMMyyyyHHMMssStr(expense.CreateDate)
                        if expense.CreateDate
                        else "no time set"
                    ),
                    "updateDate": (
                        dateTime_convert_to_ddMMyyyyHHMMssStr(expense.UpdateDate)
                        if expense.UpdateDate
                        else "no time set"
                    ),
                }
                res_data.append(data)
        return render_template("expense.html", expenses=res_data)

    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# add or update by whether it has user id
@app.route("/expense/add_update_expense", methods=["POST"])
def add_update_expense():
    try:
        expense_id = request.form.get("modalExpenseID")
        expense_name = request.form.get("modalExpenseName")
        category = request.form.get("modalCategoryName")
        amount = request.form.get("modalAmountName")
        try:
            amount = float(amount) if amount else 0.0
        except ValueError:
            amount = 0.0
        expense_date = request.form.get("modalExpenseDateName")
        notes = request.form.get("modalNotesName")
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = session["user"]

        res = Expense.add_update_expense(
            expense_id,
            expense_name,
            category,
            amount,
            expense_date,
            notes,
            now_time,
            user_id,
            db,
        )
        if res:
            if expense_id:
                flash("Expense successfully Updated.")
                return redirect(url_for("expense"))
            else:
                flash("New expense successfully added.")
                return redirect(url_for("expense"))
        else:
            flash("Action failed, some technical issues occured!")
            return redirect(url_for("expense"))
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


# delete expense function
@app.route("/expense/delete_expense", methods=["POST"])
def delete_expense():
    try:
        expense_id = request.form.get("ID")

        if not expense_id:
            flash("Expense ID is missing!", "error")
            return redirect(url_for("expense"))

        is_delete_expense = Expense.delete_expense(expense_id, db)
        if is_delete_expense:
            flash("Expense deleted successfully!", "success")
        else:
            flash("Expense not found!", "error")

        return redirect(url_for("expense"))
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")

@app.route('/latest-news', methods=['GET'])
def get_latest_news():
    try:
        api_key = '94cf5d7733ba443eae06080168ac588b'
        base_url = 'https://newsapi.org/v2/top-headlines'
        # fetch datta from NewsAPI 
        response = requests.get(base_url, params={
            'country': 'us',
            'from':{datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')},
            'sortBy': 'popularity',
            'apiKey': api_key
        })
        data = response.json()
        first_article = data['articles'][0]
        # return lastest news
        if response.status_code == 200 and 'articles' in data:
            return jsonify({'news': data['articles'][0]})
        else:
            return jsonify({'error': 'Not get news'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# direct to 404_no_page.html
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_no_page.html", error_message=str(e)), 404