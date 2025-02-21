from datetime import datetime
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash
import os
from forum.database import db, Base

# init database
def init_db(app, db):
    # init DB and exec schema for database, tables and data
    try:
        # create DB
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        engine = create_engine(db_uri)

        # create DB if not existed
        if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cmt120_cw2.db')):
            print("Database does not exist, creating it now...")
            create_database_from_sql(engine, app)
        else:
            print("Database exists!")
        # init SQLAlchemy connection
        db.init_app(app)
    except Exception as e:
        print(f"Exception caught for initializing the database: {e}")
        
# exec create_db.sql to create db
def create_database_from_sql(engine, app):
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        sql_file_path = os.path.join(base_dir, 'create_tables.sql')
        # Confirm whether the database already exists, create it if not
        with open(sql_file_path, "r") as sql_file:
            sql_commands = sql_file.read()
        
        # Use engine to execute SQL scripts
        with engine.connect() as connection:
            for command in sql_commands.split(';'):
                if command.strip():
                    connection.execute(text(command))
            hashed_password = generate_password_hash('1')
            connection.execute(text(f"INSERT INTO UserInfo ('UserID', 'Password', 'FirstName', 'LastName', 'Email', 'BirthDate', 'Mobile') VALUES ('admin', '{hashed_password}', 'Wen-Hsuan', 'Hu', 'huw10@cardiff.ac.uk', '1994/07/10', '07542618279');"))
            
            add_post('Financial Service Consultant, Aug 2020 - Aug 2021', 'After my internship, I started my role of financial advisor, the job was a bit different with my internship, I had to offer personalised investment and financial advice to my clients based on their financial situations and risk tolerance. So, I normally had to customise investment portfolios to my clients and provided ideal support to help them achieve their financial objectives.\nDuring my time at E.Sun Bank, I gained a lot of valuable experience in both banking and financial sectors, and I have understood the importance of how to build up strong relationships with clients.', os.path.join('forum','static', 'img', 'esun.jpg'), connection)
            add_post('Coding Bootcamp, Aug 2021 - Dec 2021', 'During these months of coding bootcamp, I have been pursuing a programming course to expand my skillset. During this time, I have acquired knowledge of various technologies including C#, OOP, javaScript, SQL, .net framework., .net webform, .net core MVC, ADO.NET, entity framework, ASP.NET, css, html, and vue.js.\nI have gained expertise in both front-end and back-end web development using these technologies. Specifically, I have learned to use CSS and HTML to create visually appealing and responsive web pages, as well as JavaScript and Vue.js for client-side scripting. On the back-end, I have worked with C#, .NET framework, .NET webform, .NET core MVC, and ADO.NET for server-side scripting, data access, and creating dynamic web applications.\nDuring the course, I have completed three web development projects using different technologies: a shopping website using .NET webform, an employee attendance management system using .NET webform, and a travel guide website using .NET core MVC. These projects have allowed me to apply my knowledge and gain hands-on experience in web development.\nOverall, I am excited to continue learning and growing as a programmer, and I am eager to contribute my skills to a dynamic and challenging team.', os.path.join('forum','static', 'img', 'bootscamp.jpg'), connection)
            add_post('Software Engineer, Jan 2022 - Mar 2024', 'In this job I developed two web applications, the first one was called Credit Card Retrieval and Chargeback Management System, I Developed a Windows Service to automate routine tasks such as SFTP file transfers and complex database operations. Utilized multi-threading to manage scheduled tasks, ensuring smooth execution by limiting thread timeouts. This automation improved operational efficiency by 15%–20%, reducing manual efforts within the credit card chargeback process.\nThe second web application was called Real Estate Management System & Financial Project Development, I basically did the front-end of a real estate management system using Angular, integrating Angular CLI, Dependency Injection, and Component Lifecycle Hooks. Also, I learnt NgRx and RxJS for responsive data flows, which assisted me to do backend debugging, SQL maintenance, and log monitoring.', os.path.join('forum','static', 'img', 'rstn.jpg'), connection)
            add_post('Software Engineer, Apr 2024 - Sep 2024', 'In this job I did two projects, the first one was called Real Estate Delinquency Management System Refactor, which I had to refactor a real estate delinquency management system. It was originally built with .NET and Silverlight, but I helped to move it to a decoupled MVC architecture. The front-end part I used were HTML, CSS, JavaScript, and jQuery, and the back-end was .NET API with asynchronous AJAX to do request.\nThe second project I did was Real Estate Loan Application System Enhancement, this application is for processing mortgage applications. The job I was appointed was to refactor some programme logics and added new features based on user requests. I improved the database store procedure by replacing slow SELECT queries with JOIN operations, which made the system more efficient to let user use.', os.path.join('forum','static', 'img', 'yuanta.jpg'), connection)
            
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Description', 'As a student with a bachelor degree in economics, I never thought that my life would have anything to do with programming, until one day I accidentally came into freecodecamp introduced by a friend and started with simple HTML, my programming interest trigger was activated. Then few months later I resign my financial consulting job at a bank and participated in a four-month coding bootscamp. The process was full of disappointments and difficulties, but I did really enjoy the time when seeing myself with progress. After completing the training, I found a job and started my journey as a .Net developer.');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Description', 'With my full-end development experience, such as .NET and Angular framework skills, I like to face and overcome the difficulties encountered in the development process, as well as optimize the overall application performance and user experience.');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Description', 'My focus technical skills are .NET Core, C#, ASP.NET, Angular, TypeScript, HTML, CSS, SQL Server, DeVop, and so on. I continually seek new challenges and opportunities to learn and grow, and am committed to delivering high-quality solutions that meet business goals and exceed user requirements.');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Description', 'In the fall term of Cardiff University, which starts in September 2025, I started to try python programming and perform back-end development in Fundamentals of Programming learning to develop controller, model and database by using the Flask framework and SQL Alchemy. For the front-end part, with Jinja syntax, I can quickly put back-end data for rendering into HTML. For some parts are more suitable for asynchronous processing, I chose to use jQuery with the fetch syntax to call the backend, and the Promise object handles the backend message to return success or error JSON objects.');"))
            
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'Python');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'Java');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'C#');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'HTML');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'CSS');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'Javascript');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Languages', 'Typescript');"))
            
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', '.Net Framework Webform');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', '.Net Core MVC');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', '.Net Core WebAPI');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', 'jQuery');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', 'Angular');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Frameworks', 'React');"))
            
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Database', 'MS SQL Server');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Database', 'My SQL');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Database', 'Sqlite');"))
            
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Education', 'Cardiff University - MSc Computing');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Education', 'Ming Chuan University - BSc Economics');"))
           
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Others', 'Git');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Others', 'SVN');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Others', 'CI/CD');"))
            connection.execute(text("INSERT INTO About ('UserID', 'AboutType', 'AboutDesc') VALUES('admin', 'Others', 'Docker');"))
            
            connection.commit()   
            print("Database and tables created successfully!")
    except Exception as e:
        print(f"Exception caught for Error executing SQL script: {e}")

# Convert photo file to binary format
def convert_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

# delay import
def add_post(title, content, photo_path, connection):
    try:
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = text("""
            INSERT INTO Posts (UserID, Title, Content, Photo, CreateDate)
            VALUES (:user_id, :title, :content, :photo, :create_date)
        """)
        photo = convert_to_blob(photo_path)
        connection.execute(query, {
                'user_id': 'admin',
                'title': title,
                'content': content,
                'photo': photo,
                'create_date': now_time
            })
    except Exception as e:
        print(f"Exception caught for Error executing SQL script: {e}")