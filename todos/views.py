# views define how the application interacts with the user requests.
# views handle data processing, rendering templates, and responding to actions.

# generics provides pre-built generic views for common operations 
# from rest_framework import generics
# from .models import Task
# TaskSerializer to handle serialization and the deserialization of Task objects to/from JSON
# from .serializers import TaskSerializer
# IsAuthenticated is a permission class that restricts access to authenticated users only
# from rest_framework.permissions import IsAuthenticated

# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Task
# from .serializers import TaskSerializer

# from .forms import TaskForm

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def list_tasks(request):
#   tasks = Task.objects.filter(Q(created_by=request.user))
#   serializer = TaskSerializer(tasks, many=True)   
#   return Response(serializer.data)

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def task_operations(request, task_id=None):
"""
    Unified endpoint for task operations:
    - GET: Retrieve a specific task
    - POST: Create a new task
    - PUT: Update an existing task
    - DELETE: Remove a task
"""



# handling listing and creating Task objects
# operations handled - GET (list all Task objects) and POST (create a new Task object)
# class TaskListCreateView(generics.ListCreateAPIView):
  # queryset defines the set of task objects to work with
  # queryset = Task.objects.all() # retrieves all Task instances from the database.
  # specifying the serializer to transform Task objects into JSON (for responses) and JSON data into Task objects (for requests)
  # serializer_class = TaskSerializer
  # permission_classes = [IsAuthenticated] # unauthenticated users will receive 403 Forbidden

  # def get_queryset(self):
  #   return Task.objects.filter(created_by=self.request.user)

  # def perform_create(self, serializer):
    # setting the authenticated user as created_by
    # serializer.save(created_by=self.request.user)

# handles retrieving, updating, and deleting individual Task objects.
# operations handled - GET (retrieves a single task by its primary key), PUT/PATCH (updates a Task object completely/partially), DELETE (deletes a Task object by its primary key)
# class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  # specifies that all tasks are available for retrieval, update, or delete
  # queryset = Task.objects.all()
  # serializer_class = TaskSerializer
  # permission_classes = [IsAuthenticated]

# generics.ListCreateAPIView and generics.RetrieveUpdateDestroyAPIView are generic views that automatically handle common logic for CRUD operations
# these views abstract away repetitive tasks like database queries, validation, and response handling

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import ToDoList, Task
from .tasks import send_task_creation_email, send_list_creation_email

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def todo_list_operations(request):
  if request.method == "GET":
    todo_lists = ToDoList.objects.filter(owner=request.user)
    lists_data = []
    for lst in todo_lists:
      tasks = []
      for task in lst.tasks.all():
        tasks.append({
          'id': task.id,
          'title': task.title,
          'status': task.status,
          'priority': task.priority
        })
      lists_data.append({
        'id': lst.id,
        'title': lst.title,
        'description': lst.description,
        'tasks': tasks
      })
    return JsonResponse({"todo_lists": lists_data})
  
  elif request.method == "POST":
    try:
      data = json.loads(request.body)
      print("DATA:", data)
      title = data.get('title')
      description = data.get('description', '')
      if not title:
        return JsonResponse({"error": "Title is required"}, status=400)
      todo_list = ToDoList.create_list(
        user=request.user,
        title=title,
        description=description
      )
      
      send_list_creation_email.delay(
        list_title=title,
        user_email=request.user.email
      )

      return JsonResponse({
        "message": "To Do List created",
        "id": todo_list.id
      }, status=201)

    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON"})
    
  elif request.method == "DELETE":
    try:
      data = json.loads(request.body)
      list_id = data.get('id')
      todo_list = ToDoList.objects.get(id=list_id, owner=request.user)
      todo_list.delete()
      return JsonResponse({"error": "To Do List deleted"}, status=200)
    except ToDoList.DoesNotExist:
      return JsonResponse({"error": "List not found"}, status=404)
    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON"}, status=400)
  else:
    return JsonResponse({"error": "Invalid Method"})
  
@csrf_exempt
@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_operations(request, todo_list_id, task_id=None):
  try:
    todo_list = ToDoList.objects.get(id=todo_list_id, owner=request.user)
  except ToDoList.DoesNotExist:
    return JsonResponse({"error": "ToDo List not found"}, status=404)
  
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      title = data.get("title")
      description = data.get("description", "")
      priority = data.get("priority", "MEDIUM")
      status = data.get("status", "TODO")

      if not title:
        return JsonResponse({"error": "Title is required"})
      
      try:
        task = Task.create_task(
          user=request.user,
          todo_list=todo_list,
          title=title,
          description=description,
          priority=priority,
          status=status
        )

        send_task_creation_email.delay(
          task_title=title,
          user_email=request.user.email
        )

        return JsonResponse({
          "message": "Task Created",
          "id": task.id
        }, status=201)
      except (ValueError, PermissionError) as e:
        return JsonResponse({"error": str(e)})
    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON"})
    
  elif request.method in ["PUT", "DELETE"]:
    try:
      task = Task.objects.get(id=task_id, todo_list=todo_list)
    except:
      return JsonResponse({"error": "Task not found"}, status=404)
    if request.method == "PUT":
      try:
        data = json.loads(request.body)
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.priority = data.get("priority", task.priority)
        task.status = data.get("status", task.status)
        task.save()
        return JsonResponse({"message": "Task Updated"})
      except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"})
    
    elif request.method == "DELETE":
      task.delete()
      return JsonResponse({"message": "Task Deleted"})
  
  return JsonResponse({"error": "Method not allowed"}, status=405)
