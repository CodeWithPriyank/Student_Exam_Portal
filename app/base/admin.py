from django.contrib import admin
from .models import Question, Option, Exam, User

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Exam)
