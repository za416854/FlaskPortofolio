# CMT120 Coursework 2 - Forum Website

Username: c24045684

Link to website: https://forumdemo-c24045684cmt120forum.apps.containers.cs.cf.ac.uk

## Project Overview

This is a forum website built with Flask. It allows users to create posts, comment on posts, and interact with other users. Also it allows users to to expense record, to help you recollect how much you've spent. It includes features such as user authentication, database storage, and a simple, clean UI.

### References - Source Code:

- Bootstrap implementation 1 (https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- Bootstrap implementation 2 (https://www.w3schools.com/bootstrap5/)
- Werkzeug implementation on Docs (https://werkzeug.palletsprojects.com/en/stable/utils/)
- flask_login implementation on (https://flask-login.readthedocs.io/en/0.6.3/)
- Fetch syntax on(https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- Handling Application Errors(https://flask.palletsprojects.com/en/stable/errorhandling/?utm_source=chatgpt.com)
- How to use Python Requests(https://www.w3schools.com/python/module_requests.asp)
- News API(https://newsapi.org/)
---
## Prerequisites

- Python 3.x 

Ensure you have Python 3.x installed. You can verify by running:
```bash
python --version
```
## Instructions (Local Deployment - Empty Site)

For **Windows (NT)**, you can set up the virtual environment with the following commands:

```bash
python3 -m venv venv
.\venv\Scripts\activate
```
For **macOS** or **Linux**, you can use:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies after activating the virtual environment:
```bash
pip install -r requirements.txt
```

The programme will distinguish whether the database is created, if no it will create a new database with appointed tables, the schema is inside the following file.

```
create_tables.sql
```

And next, we run the following Flask prompt to run my web application:

```
flask --app wsgi run 
```

Alternatively, you can use:

```
flask run
```

This will start the Flask server locally, and you can visit the website in your browser at http://localhost:5000.

