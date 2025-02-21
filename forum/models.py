from sqlalchemy import Float, and_, desc, text
from sqlalchemy import Column, Integer, String, Table, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, relationship
from typing import List
from forum import Base, db, login_manager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from flask_login import UserMixin  # provides default implementations for the methods that Flask-Login expects user objects to have.
from datetime import datetime, timedelta


# class UserInfo
class UserInfo(Base, UserMixin, db.Model):
    __tablename__ = "UserInfo"

    UserID = Column(String, primary_key=True, nullable=False)
    Password = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    BirthDate = Column(String)
    Mobile = Column(String)

    # construction
    def __init__(self, UserID, Password, FirstName, LastName, Email, BirthDate, Mobile):
        self.UserID = UserID
        self.Password = Password
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.BirthDate = BirthDate
        self.Mobile = Mobile

    def get_id(self):
        try:
            return str(self.UserID)
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: Query users by ID
    @staticmethod
    def get_userinfo_by_id(userID, db):
        try:
            query = select(UserInfo).where(UserInfo.UserID == userID)
            return db.session.scalar(query)
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: get userinfo by login
    @staticmethod
    def get_userinfo_by_login(userID, password, db):
        try:
            query = select(UserInfo).where(
                UserInfo.UserID == userID and UserInfo.Password == password
            )
            return db.session.scalar(query)
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: add userinfo
    @staticmethod
    def add_userinfo(
        userID, password, firstName, lastName, email, birthDate, mobile, db
    ):
        try:
            new_user_info = UserInfo(
                UserID=userID,
                Password=password,
                FirstName=firstName,
                LastName=lastName,
                Email=email,
                BirthDate=birthDate,
                Mobile=mobile,
            )
            query = db.session.scalar(select(UserInfo).where(UserInfo.UserID == userID))
            if query != None:
                return "UserExists"
            db.session.add(new_user_info)
            db.session.commit()
            return new_user_info
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()

    # Static method: add userinfo
    @staticmethod
    def update_userinfo(
        existing_user,
        firstName,
        lastName,
        email,
        birthDate,
        mobile,
        db,
    ):
        try:
            if existing_user is None:
                return False
            if firstName is not None:
                existing_user.FirstName = firstName
            if lastName is not None:
                existing_user.LastName = lastName
            if email is not None:
                existing_user.Email = email
            if birthDate is not None:
                existing_user.BirthDate = birthDate
            if mobile is not None:
                existing_user.Mobile = mobile

            db.session.commit()
            return True 
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return False

    # Static method: add userinfo
    @staticmethod
    def get_all_userinfos(db):
        try:
            res = db.session.query(UserInfo).all()
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return False

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(str(user_id))
# class Posts
class Posts(Base, db.Model):
    __tablename__ = "Posts"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String, ForeignKey("UserInfo.UserID"), nullable=False)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Photo = Column(LargeBinary, nullable=True)
    CreateDate = Column(db.DateTime, nullable=True)

    # construction
    def __init__(self, UserID, Title, Content, Photo, CreateDate):
        self.UserID = UserID
        self.Title = Title
        self.Content = Content
        self.Photo = Photo
        self.CreateDate = CreateDate

    # Static method: add post
    @staticmethod
    def add_post(db, user_id, title, content, photo=None):
        try:
            new_post = Posts(
                UserID=user_id,
                Title=title,
                Content=content,
                Photo=photo,
                CreateDate=datetime.now().replace(microsecond=0),
            )
            db.session.add(new_post)
            db.session.commit()
            return new_post
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()

    # Static method: get posts
    @staticmethod
    def get_posts(db, user_id):
        try:
            res = db.session.query(Posts).filter(Posts.UserID == user_id)
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return False

    # Static method: get post by id
    @staticmethod
    def get_post_by_id(db, post_id):
        try:
            res = db.session.query(Posts).filter(Posts.ID == post_id).first()
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: get all posts
    @staticmethod
    def get_all_posts(db):
        try:
            res = db.session.query(Posts).order_by(desc(Posts.ID)).all()
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: get post by id
    @staticmethod
    def delete_post(db, post_id):
        try:
            post = db.session.query(Posts).filter(Posts.ID == post_id).first()
            if post:
                db.session.delete(post)
                comments = (
                    db.session.query(Comments).filter(Comments.PostID == post_id).all()
                )
                if comments:
                    for comment in comments:
                        db.session.delete(comment)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Database error: {e}")


# class Comments
class Comments(Base, db.Model):
    __tablename__ = "Comments"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    PostID = Column(Integer, ForeignKey("Posts.ID"))
    UserID = Column(String, ForeignKey("UserInfo.UserID"))
    Comment_Text = Column(String, nullable=False)
    CreateDate = Column(String, nullable=False)

    # construction
    def __init__(self, PostID, UserID, Comment_Text, CreateDate):
        # self.ID = ID
        self.PostID = PostID
        self.UserID = UserID
        self.Comment_Text = Comment_Text
        self.CreateDate = CreateDate

    # Static method: get comments by post id
    @staticmethod
    def get_comments_by_post_id(post_id, db):
        try:
            sql = """
                  SELECT *
                  FROM UserInfo
                    JOIN Comments ON Comments.UserID = UserInfo.UserID
                  WHERE 1=1 
                  AND Comments.PostID = :post_id
                  AND Comments.UserID = UserInfo.UserID;
                  """
            result = db.session.execute(text(sql), {"post_id": post_id})
            return result
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: get comments by id
    @staticmethod
    def get_comment_by_id(post_id, db):
        try:
            res = db.session.query(Comments).filter(Comments.PostID == post_id).all()
            return res if res != None else None
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: add comment
    @staticmethod
    def add_comment(post_id, user_id, comment_text, db):
        try:
            new_comment = Comments(
                PostID=post_id,
                UserID=user_id,
                Comment_Text=comment_text,
                CreateDate=datetime.now().replace(microsecond=0),
            )
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()

# class About
class About(Base):
    __tablename__ = "About"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String, ForeignKey("UserInfo.UserID"))
    AboutType = Column(String, nullable=False)
    AboutDesc = Column(String, nullable=False)

    def __init__(self, ID, AboutType, UserID, AboutDesc):
        self.ID = ID
        self.UserID = UserID
        self.AboutType = AboutType
        self.AboutDesc = AboutDesc

    # Static method: get abouts data
    @staticmethod
    def get_abouts(db):
        try:
            res = db.session.query(About).all()
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")  


# class Expense
class Expense(Base):
    __tablename__ = "Expense"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String, ForeignKey("UserInfo.UserID"), nullable=False)
    ExpenseName = Column(String, nullable=False)
    Category = Column(String, nullable=False)
    Amount = Column(Float, nullable=False)
    ExpenseDate = Column(db.DateTime, nullable=False)
    Notes = Column(String, nullable=False)
    CreateDate = Column(db.DateTime, nullable=True)
    UpdateDate = Column(db.DateTime, nullable=True)

    # construction
    def __init__(
        self,
        UserID,
        ExpenseName,
        Category,
        Amount,
        ExpenseDate,
        Notes,
        CreateDate,
        UpdateDate,
    ):
        self.UserID = UserID
        self.ExpenseName = ExpenseName
        self.Category = Category
        self.Amount = Amount
        self.ExpenseDate = ExpenseDate
        self.Notes = Notes
        self.CreateDate = CreateDate
        self.UpdateDate = UpdateDate

    # Static method: get expense by userID
    @staticmethod
    def get_expense_by_userID(user_id, db):
        try:
            res = db.session.query(Expense).filter(Expense.UserID == user_id).all()
            return res if res != None else []
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: get expenses by interval
    @staticmethod
    def get_expenses_by_interval(start_date, end_date, db):
        try:
            start_date = start_date
            end_date = end_date
            sql = """
                SELECT * FROM Expense
                WHERE ExpenseDate BETWEEN :start_date AND :end_date
                ORDER BY ExpenseDate;
                  """

            res = db.session.execute(
                text(sql), {"start_date": start_date, "end_date": end_date}
            )
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: add or update expense
    @staticmethod
    def add_update_expense(
        expense_id,
        expense_name,
        category,
        amount,
        expense_date,
        notes,
        now_time,
        user_id,
        db,
    ):
        try:
            # update data if there is expense id
            if expense_id:
                sql = """
                    UPDATE Expense
                    SET 
                        ExpenseName = :expense_name,
                        Category = :category,
                        Amount = :amount,
                        ExpenseDate = :expense_date,
                        Notes = :notes,
                        UpdateDate = :update_date
                    WHERE ID = :expense_id
                """
                params = {
                    "expense_name": expense_name,
                    "category": category,
                    "amount": amount,
                    "expense_date": expense_date,
                    "notes": notes,
                    "update_date": now_time,
                    "expense_id": expense_id,
                }
            else:
                # insert data if there is no expense id
                sql = """
                    INSERT INTO Expense (UserID, ExpenseName, Category, Amount, ExpenseDate, Notes, CreateDate, UpdateDate) 
                    VALUES (:user_id, :expense_name, :category, :amount, :expense_date, :notes, :create_date, :update_date)
                """
                params = {
                    "user_id": user_id,
                    "expense_name": expense_name,
                    "category": category,
                    "amount": amount,
                    "expense_date": expense_date,
                    "notes": notes,
                    "create_date": now_time,
                    "update_date": now_time,
                }
            db.session.execute(text(sql), params)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return False

    # Static method: get last 30 days expenses data
    @staticmethod
    def get_expenses_last_30_days(db):
        try:
            thirty_days_ago = datetime.now().date() - timedelta(days=30)
            res = (
                db.session.query(Expense)
                .filter(Expense.ExpenseDate >= thirty_days_ago)
                .order_by(Expense.ExpenseDate)
                .all()
            )
            return res
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    # Static method: delete row expense data
    @staticmethod
    def delete_expense(expense_id, db):
        try:
            # delete by ID.
            expense = db.session.query(Expense).filter(Expense.ID == expense_id).first()
            if not expense:
                return False  # If the fee does not exist, return False directly
            sql = """
               DELETE FROM Expense WHERE ID = :expense_id
                  """
            db.session.execute(text(sql), {"expense_id": expense_id})
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()  #
            return False
