from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    roll_number = models.CharField(max_length=20, unique=True, null = True, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    class_name = models.CharField(max_length=50, blank=True)  

    def __str__(self):
        return self.username

# Question model
class Question(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

# Option model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

# Exam model
class Exam(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_exams')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='qustion_exams')
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='exam_option')
    is_release = models.BooleanField(default=True, blank = True)
    
    def is_correct(self):   
        return self.selected_option.is_correct      

    def is_release(self):
        return self.is_release
    
    def __str__(self):
        return f"{self.student.username} - {self.question.text}"

