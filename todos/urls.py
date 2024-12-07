from django.urls import path
from . import views

# urlpatterns contains the URL routes that map specific URLs to corresponding views
urlpatterns = [
  # as_view() method is used to convert the class-based view into a callable function that Django can use to process HTTP requests
  # a unique name is given to a route which can be used to reference the URL elsewhere in the code
  path('todo-lists/', views.todo_list_operations, name='todo-list-operations'),
  path('todo-lists/<int:todo_list_id>/tasks/', views.task_operations, name='task-create'),
  path('todo-lists/<int:todo_list_id>/tasks/<int:task_id>/', views.task_operations, name='task-operations')
]

# when a request matches the URL pattern, Django calls the corresponding view 