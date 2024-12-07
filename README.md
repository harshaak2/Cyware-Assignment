# To-Do List using DRF

This demo project of to-do list is built using Django REST Framework for API, PostgreSQL as database and Celery for task reminders. This project features user registration and authentication, CRUD operations on to-do items, and email alerts on a list or task creation.

## Key Features

- User registration and JWT based login
- Task ownership 
- CRUD operations for tasks 
- Task creation alert mails using Celery

## API Endpoints
- POST /api/auth/register/ : registering a new user
- POST /api/auth/login/ : user login (generates an access token)
- GET /api/todo-lists/ : get all the lists for the authenticated user
- POST /api/todo-lists/ : create a new list
- DELETE /api/todo-lists/ : delete an entire list based on id
- POST /api/todo-lists/<todo_list_id>/tasks/ : creating a new task in a list (list id is generated on creation)
- PUT /api/todo-lists/<todo_list_id>/tasks/<task_id>/ : updating a task in a list
- DELETE /api/todo-lists/<todo_list_id>/tasks/<task_id>/ : deleting a task in a list
- NOTE: add the access_token of the user (which is generated after login) in the header as "Authorization": "Bearer access_token" in all the requests

## Getting Started
To get started with the project, use the following commands
- pip install requirements.txt to install the dependencies
- start the server by "python manage.py runserver 8000"
- start the celery worker using "celery -A todo_project worker -l info"
- start the redis server by "redis-server"