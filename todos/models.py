from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class   ToDoList(models.Model):
  title = models.CharField(max_length=30)
  description = models.TextField(blank=True)
  # a foreign key relationship to Django's built in User model.
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_lists')
  created_at = models.DateTimeField(auto_now_add=True)

  # the __str__ function defines the human readable string representation of the object.
  # when we call str(instance) or print(instance), __str__ method is invoked
  def __str__(self):
    return self.title
  
  # class Meta is an inner class in Django models that provides metadata about the model. This metadata does not define any fields but is used to customize the model's behavior, and set constraints or options that affect how the model interacts with the database or queries.
  # Common attributes in class Meta - ordering, verbose_name (human-readable name for the model), verbose_name_plural, db_table, unique_together (ensures that a combination of the fields is unique), abstract (specifies if the model should be abstract)
  class Meta:
    ordering = ['-created_at']

  @classmethod
  def create_list(cls, user, title, description=""):
    """creates a new list for a user"""
    todo_list = cls.objects.create(
      owner=user,
      title=title,
      description=description
    )
    return todo_list
  
  def get_tasks(self):
    return self.tasks.all()


class Task(models.Model):
  class Priority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

  class Status(models.TextChoices):
    TODO = "TODO", "To Do"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    ARCHIVED = "ARCHIVED", "Archived"
    
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  # establishing a foreign key relationship with the ToDoList model; deleting a to-do list will delete all its associated tasks
  todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name="tasks")
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
  priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
  created_by = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE, default=1)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ['-created_at']

  def mark_completed(self):
    self.status = self.Status.COMPLETED
    self.save()
  
  # the classmethod decorator allows calling the method on the class itself rather than an instance; cls represents the class itself (similar to how self represents an instance)
  @classmethod
  def create_task(cls, user, todo_list, title, description="", priority="MEDIUM", status="TODO"):
    # validating the user
    if todo_list.owner != user:
      raise PermissionError("Action not allowed")
    # validating the priority
    if priority not in dict(cls.Priority.choices):
      raise ValueError(f"Invalid Priority. Must be one of: {dict(cls.Priority.choices).keys()}")
    # validating the user
    if status not in dict(cls.Status.choices):
      raise ValueError(f"Invalid Status. Must be one of: {dict(cls.Status.choices).keys()}")
    
    # create and return the task
    task = cls.objects.create(
      title=title,
      description=description,
      todo_list=todo_list,
      priority=priority,
      status=status,
      created_by=user
    )

    return task
  
  '''
  usage example: 
    new_task = Task.create_task(
      user=current_user,
      todo_list=my_list,
      title="Complete Project",
      priority="HIGH"
    )
  '''