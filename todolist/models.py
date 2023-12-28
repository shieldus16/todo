from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user_id = models.CharField(max_length=15, primary_key=True)
    user_password = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    user_color = models.CharField(max_length=7, blank=True)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_id = models.AutoField(primary_key=True)
    todo_content = models.TextField()
    todo_date = models.DateField()
    todo_flag = models.IntegerField()