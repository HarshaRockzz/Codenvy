from re import template
from statistics import mode
from unicodedata import name
from django.db import models

class User(models.Model):
    username = models.CharField(primary_key=True,max_length=122)
    name = models.CharField(max_length=122)
    email = models.CharField(unique=True,max_length=122)
    password = models.CharField(max_length=32)
    problems_solved = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=122)
    type = models.CharField(max_length=50)
    difficuilty = models.CharField(max_length=10)
    statement = models.TextField()
    task = models.TextField(null=True)
    time_complexity = models.CharField(max_length=50,null=True)
    space_complexity = models.CharField(max_length=50,null=True)
    constraints = models.CharField(max_length=122,null=True)
    example = models.TextField(null=True)
    
    def __str__(self) -> str:
        return self.name

class Submission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    code = models.TextField(null=True)
    verdict = models.CharField(max_length=255)
    time = models.DateTimeField()

class TestCases(models.Model):
    input = models.TextField()
    output = models.TextField()
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE,null=True)
