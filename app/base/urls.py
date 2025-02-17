from django.urls import path, include
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # Admin views
    path('name/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('name/manage_teacher/', views.manage_teacher, name='manage_teacher'),
    path('name/manage_student/', views.manage_student, name='manage_student'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('update_teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),

    # Teacher views
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/create_question/', views.create_question, name='create_question'),
    path('teacher/add_option/<int:question_id>/', views.add_option, name='add_option'),
    path('delete_student/<int:student_id>/', views.delete_student, name = 'delete_student'),
    path('delete_question/<int:question_id>/', views.delete_question, name = 'delete_question'),
    path('update_question/<int:question_id>/', views.update_question, name = 'update_question'),

    # Student views
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/take_exam/', views.take_exam, name='take_exam'),
    path('resultPage/', views.resultPage, name='resultPage'),
    
]