# 🧩 SoftDesk - Issue Tracking API

SoftDesk is a RESTful API developed in Python with Django REST Framework. It allows users to create collaborative projects, manage issues (issues), track progress and communicate through comments. It integrates a system of permissions based on the role of contributors and respects the rules of protection of personal data (GDPR).

---

## 🚀 main features

- 🔐 Authentication avec JWT
- 🧑 User management (registration, deletion, GDPR preferences)
- 📁 Project creation and management
- 👥 Adding and removing contributors to a project
- 🐞 Creating and tracking tasks (issues)
- 💬 Adding comments to issues
- 📅 Timestamp of each resource
- 📄 Automatic pagination of lists
- 🔒 Strict permissions: only authors can edit/delete their content

---

## 🛠️ Technologies used

- Python 3.12.1
- Django 5.1.8
- Django REST Framework 3.15.2
- SimpleJWT 
- SQLite3 (by default)
- Postman (for test)

---

## 📦 Installation

### prerequisite
Python must be installed beforehand.

If you work in a Linux or MacOS environment: Python is normally already installed. To check, open your terminal and type:
```bash
python --version
```
or
```bash
python3 --version
```
If Python is not installed, you can download it at the following address: [Download Python3](https://www.python.org/downloads)

You will also need the pip Python package installer which is included by default if you have a Python version >= 3.4. You can check that it is available through your command line, by entering:
```bash
pip --version
```
You will also need Git to clone the application on your computer. Check your installation by typing
```bash
git --version Otherwise
```
choose and download the version of Git that corresponds to your installation: MacOS, Windows or Linux/Unix by clicking on the following link:  [Download git](https://git-scm.com/downloads) Then run the file you just downloaded. Press Next at each window and then Install. During installation, leave all the default options as they work well. Git Bash is the interface for using Git on the command line.

### 1. Clone the Repository
First, open the command prompt in the folder where you want to drop the clone.
Clone this repository to your local machine.
```bash
git clone https://github.com/Mikael2983/OC_P10_Create_secure_RESTful_API.git
```
```bash
cd OC_P10_Create_secure_RESTful_API
```

### 2. Create Virtual Environment
To create virtual environment, install virtualenv package of python and activate it by following command on terminal:
```bash
python -m venv env
```
then with windows : 
```bash
env/Scripts/activate
```
or with Mac or linux 
```bash
source env/bin/activate 
```

### 3. Requirements
To install required python packages, copy requirements.txt file and then run following command on terminal:
```bash
pip install -r requirements.txt
```

### 4. initalize database
To initialize the database, first, create new migrations
```bash
python manage.py makemigrations authenticated projectManagement
```
Then, apply migrations.
```bash
python manage.py migrate
```
To properly view application functionality load data from dump_08_04.json file
```bash
python manage.py loaddata dump_08_04.json
```

### 5. Start Server
On the terminal enter following command to start the server:

```bash
python manage.py runserver
```

### 6. Start the admin console
To start the admin console on localhost, enter following URL in the web browser: http://127.0.0.1:8000/admin 
login with :

```bash
username : admin
password : password-oc
```
---

## 🔑 Authentication

The system uses JSON Web Tokens (JWT).  
To obtain a token:

- **POST** `/api/token/` → Authentication
- **POST** `/api/token/refresh/` → renewal

Include access token in headers:

```
Authorization: Bearer <your_token>
```

---

## 📂 Main endpoints

| Resource       | methods available        | URL example                                     |
|----------------|--------------------------|-------------------------------------------------|
| Users          | GET, POST, PATCH, DELETE | `/api/v1/users/`, `api/v1/users/{id}/`          |
| Authentication | POST                     | `/api/v1/token/`, `/api/v1/token/refresh/`      |
| Projects       | GET, POST, PATCH, DELETE | `/api/v1/projects/`, `/api/v1/projects/{id}/`   |
| Contributors   | POST                     | `/api/v1/projects/{id}/add_contributor/`        |
| Contributors   | DELETE                   | `/api/v1/projects/{id}/del_contributor/`        |
| Issues         | GET, POST, PATCH, DELETE | `/api/v1/issues/`, `/api/v1/issues/{id}/`       |
| Comments       | GET, POST, PATCH, DELETE | `/api/v1/comments/`, `/api/v1/comments/{uuid}/` |

---

## 👮 permission management

- Only authenticated users can access resources.
- Only contributors to a project can access its issues and comments.
- Only the author of a resource can modify or delete it.

---


### 📖 Use ReadtheDocs documentation

the full documentation is available on the [ReadtheDocs website](https://softdesk-support-api.readthedocs.io/en/latest/)


