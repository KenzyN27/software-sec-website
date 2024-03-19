This was a project I worked on for my software security course. I had to create a simple and secure web application with a login page that could create users and allow a user to change their password, as well as submit content in a form somewhere.

The main focus was to secure the login/create account page from attacks like SQL Injection, XSS, and command injection and also use suitable authentication practices. Security for things like XSS, CSRF, the secret key, etc. are also included elsewhere due to the packages included in the website.

This is a website that uses Python and multiple Flask libraries in the backend. It uses a SQLite database for the users that is created when the app runs and does not detect a database file.

![A gif logging into the web app.](https://i.imgur.com/9OQtCCJ.gif)

# Setting up the Web App
## Python Version
This web app was created with Python 3.12.1.

Refer to the folder structure at the end for clarification in file placement.

## Installing the packages
This web app uses python and Flask packages to implement web app fuctionality and security. The required packages are listed below:
- Flask 3.0.1
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Flask-Bcrypt 1.0.1
- Flask-Talisman 1.1.0
- email_validator 2.1.1
- python_dotenv 1.0.1

I have included a txt file with all the packages and their versions when I made this web app. They can be installed by using the command below:
```
pip install -r packages.txt
```

## Environment File
The app in its current configuration needs an environment file created that contains `SECRET_KEY`, `DATABASE_URL`, and `BCRYPT_LOG_ROUNDS`, as including them in `__init__.py` is generally considered insecure. Create this file in the `software-sec-website` folder.

Example:
```
SECRET_KEY='thisisasecretkey'
DATABASE_URL='<type_of_database>:///<database file>'
BCRYPT_LOG_ROUNDS=10
```

## OpenSSL Certificate
This app uses HTTPS as part of the secure login function. Flask uses OpenSSL keys and certificates to enable HTTPS. Two files called `key.pem` and `cert.pem` are required to be created.

To create an OpenSSL key and certificate, use a command like the one below in the root folder:
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
Make sure the files are named `key.pem` and `cert.pem`, otherwise the main executable file will need to be changed to accomodate a different file name.

# Running the Web App
I have included two ways of running the web app. One way is with `main.py` in a command-line terminal, and the other is through a docker container using the included Dockerfile.

## Using Python in Command Line
Run the following command in the root folder to run the web app:
```
python main.py
```
The app should be accessible via ht<span>tps://</span>127.0.0.1:5001

## Using a Docker Container
Build the docker image using the included Dockerfile with following command:
```
docker image build -t softwaresecwebsite:latest
```

Run the docker container with the following command:
```
docker run -d -p 5001:5001 softwaresecwebsite:latest
```

**NOTE: the Dockerfile and `dockermain.py` as is have been configured to be accessed via ht<span>tps://</span>127.0.0.1:5001**

## Accessing Admin Webpage
There is one link restricted to an Admin user in this web app. To change a user to Admin, open the database file in a database editor and change the value stored in the isAdmin column to 1 to access that webpage.

# Folder Structure
```
software-sec-website
│   README.md
|   packages.txt
│   main.py
|   dockermain.py
|   Dockerfile
|   key.pem
|   cert.pem
|   .env
│
└─── instance
|   |   database file
|   
└─── Website
│   │   __init__.py
│   │   auth.py
|   |   config.py
|   |   models.py
|   |   views.py
│   │
│   └─── static
│   |   │   basestyle.css
│   |   │   formstyle.css
│   |   
│   └─── templates
│   |   │   base.html
│   |   │   change_password.html
│   |   │   contact.html
│   |   │   create_account.html
│   |   │   details.html
│   |   │   home.html
│   |   │   login.html
│   |   │   logout.html
│   |   │   submit.html
│   |   │   userlist.html
```
