# Django Task Management Project

This is a Django project for task management using MySQL as the database.

## Clone the Repository

```
git clone https://github.com/Neo-Ayush-jha/task.git
cd task
```
## Activate enviroment using this command

myenv\Scripts\activate



## Install Dependencies
`` pip install django ``
`` pip install -r requirements.txt ``


## Apply Migrations
`` python manage.py makemigrations task_management_app ``
`` python manage.py migrate ``

## Create Database in your MySQL database

    1. Make sure you have MySQL installed on your system.

    2. Create a MySQL database for the project. You can use a MySQL client like MySQL Workbench or the command line:

    ## DATABASE NAME = task_management
    3. Update the settings.py file in the task directory with your MySQL database configuration. Modify the DATABASES setting:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'task_management',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }


## Run the Development Server us this code

`` python manage.py runserver ``


Visit http://localhost:8000/api/task/ in your web browser to access the application.



## Postman Collection Documentation

Explore the API endpoints and functionalities using our Postman collection documentation: 
https://documenter.getpostman.com/view/22737106/2s9YkjB4E6
