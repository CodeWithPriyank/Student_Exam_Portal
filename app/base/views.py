from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, Option, Exam, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import QuestionForm, OptionForm
from django.contrib import messages
from .forms import StudentRegisterForm, TeacherRegisterForm
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

# Admin View
@login_required
def admin_dashboard(request):
    print("admin method------",request.user)
    print("method-----", request.method)
    teachers = User.objects.filter(role = 'teacher')
    students = User.objects.filter(role = 'student')
    return render(request, 'admin_dashboard.html', {'teachers': teachers, 'students': students})


#manage teacher view
@login_required
def manage_teacher(request):
    # if request.user.role != 'admin':
    #     return JsonResponse({'error': 'Unauthorized'}, status=403)
    print(request.method,"-----")
    if request.method == 'POST':
        print("in post methodd", request.method)
        username = request.POST['username']
        password = request.POST['password']
        subject = request.POST['subject']
        user = User.objects.create_user(username=username, password=password, subject = subject, role='teacher')
        # User.objects.create(user=user, subject=subject)
        user.save()
        return redirect('admin_dashboard')
    return render(request, 'manage_teacher.html')

#manage student where admin role also there
# @login_required
# def manage_student(request):
#     print("into the manage student function")
#     if request.user.role == 'admin':
#         print("into the admin if condition")
#         # return JsonResponse({'error': 'Unauthorized'}, status=403)
#         if request.method == 'POST':
#             print("into the admin post method")
#             username = request.POST['username']
#             # password = request.POST['password']
#             # roll_number = request.POST['roll_number']
#             # class_name = request.POST['class_name']
#             user = User.objects.create_user(username=username, role='teacher')
#             # Student.objects.create(user=user, roll_number=roll_number, class_name=class_name)
#             User.objects.create(user=user)
#             return redirect('admin_dashboard')
        
#     elif request.user.role == 'teacher':
#         print("into the teacher if condition")
#         # return JsonResponse({'error': 'Unauthorized'}, status=403)
#         if request.method == 'POST':
#             print("into the teacher post method")
#             username = request.POST['username']
#             # password = request.POST['password']
#             roll_number = request.POST['roll_number']
#             # class_name = request.POST['class_name']
#             user = User.objects.create_user(username=username,  role='student')
#             # Student.objects.create(user=user, roll_number=roll_number, class_name=class_name)
#             User.objects.create(user=user, roll_number=roll_number)
#             return redirect('teacher_dashboard')
#     return render(request, 'manage_student.html') 

@login_required
def manage_student(request):
    if request.method == 'POST':
        print("method-----", request.method)
        username = request.POST.get('username')
        email = request.POST.get('email')
        roll_number = request.POST.get('roll_number') 
        password = request.POST.get('password')  


        if username and email and roll_number and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            else:
                user = User(
                    username=username,
                    email=email,
                    role='student',
                    roll_number=roll_number,
                    password=make_password(password)  
                )
                user.save()
                messages.success(request, 'Student added successfully!')

    students = User.objects.filter(role='student')  

    return render(request, 'manage_student.html', {'students': students})

# Teacher View
@login_required
def teacher_dashboard(request):
    print("teacher dashboard-----")
    print("method-----", request.method)
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    questions = Question.objects.filter(teacher = request.user)
    students = User.objects.filter(role = 'student')
    return render(request, 'teacher_dashboard.html', 
                {'questions': questions, 'students': students})

#question view to create question
@login_required
def create_question(request):
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == 'POST':
        print('method----', request.method)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.teacher = request.user
            question.save()
            return redirect('teacher_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})


#option view to add options in question
@login_required
def add_option(request, question_id):
    print("method-----", request.method)
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    question = get_object_or_404(Question, id=question_id, teacher=request.user)
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
            return redirect('teacher_dashboard')
    else:
        form = OptionForm()
    return render(request, 'add_option.html', {'form': form, 'question': question})

# Student View
@login_required
def student_dashboard(request):
    print("student method-----", request.method)
    if request.user.role != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    return render(request, 'student_dashboard.html')

#exam view
@login_required
def take_exam(request):
    print("take exam function called")
    print("method-----", request.method)
    if request.user.role != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    print("before questions printed --------")
    questions = Question.objects.all()
    roll_number = User.objects.get(roll_number = request.user.roll_number) 
    print(f"roll number ------- {roll_number}")
    if request.method == 'POST':
        print("in if condition ")
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(Option, id=selected_option_id)
                Exam.objects.create(student=request.user, question=question, selected_option=selected_option)
        return redirect('student_dashboard')
    return render(request, 'take_exam.html', {'questions': questions})


# @login_required
# def take_exam(request):
#     if request.user.role != 'student':
#         return JsonResponse({'error': 'Unauthorized'}, status=403)
    
#     questions = Question.objects.all()
#     print("Questions fetched:", questions)

#     if request.method == 'GET':
#         print("Processing POST request")
#         for question in questions:
#             selected_option_id = request.POST.get(f'question_{question.id}')
#             if selected_option_id:
#                 selected_option = get_object_or_404(Option, id=selected_option_id)

#                 try:
#                     Exam.objects.create(student=request.user, question=question, selected_option=selected_option)
#                 except IntegrityError:
#                     print(f"User {request.user.username} already submitted an answer for question {question.id}")

#         return redirect('student_dashboard')  


#     return render(request, 'take_exam.html', {'questions': questions})


#logout view
def logout_user(request):
    print("method-----", request.method)
    logout(request)
    return redirect('login_user')

#delete student function
@login_required
def delete_student(request, student_id):
    print("delete student method-----", request.method)
    # if request.user.role != 'teacher' or request.user.role != 'admin':
    #     return JsonResponse({'error': 'Unauthorized'}, status=403)     #error
    print(request.user,"------")
    student = get_object_or_404(User, id=student_id, role='student')  
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard') 
    else:
        return redirect('admin_dashboard')
    
@login_required
def delete_teacher(request, teacher_id):
    print("delete teacher method ------", request.method)
    teacher = get_object_or_404(User, id = teacher_id, role = 'teacher')
    teacher.delete()
    return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html')
    

@login_required
def delete_question(request, question_id):
    print("method-----", request.method)
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    question = get_object_or_404(Question, id=question_id)  
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('teacher_dashboard') 


@login_required
def update_question(request, question_id):
    print("in update question function -----")
    print("method-----", request.method)
    question = get_object_or_404(Question, id = question_id)
    
    if request.user.role != 'teacher':
        return JsonResponse({'error' : 'Unauthorized'}, status = 403)

    if request.method == "POST":
        print("in the post method-------")
        form = QuestionForm(request.POST, instance = question)
        if form.is_valid():
            form.save()
            messages.success(request, "question updated successfully!")
            return redirect('teacher_dashboard')
    else:
        form = QuestionForm(instance = question)
        
    return render(request, 'update_question.html', {'form' : form})

@login_required
def update_teacher(request, teacher_id):
    print("in the update teacher function------")
    print("teacher method----", request.method)
    teacher = get_object_or_404(User, id = teacher_id)
    
    # if request.user.role != 'teacher':
    #     return JsonResponse({'error' : 'Unauthorized'}, status = 403)

    if request.method == "POST":
        print("in the post method-------",request.method)
        form = TeacherRegisterForm(request.POST, instance = teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "teached updated successfully.....")
            return redirect('admin_dashboard')
    else:
        # form = TeacherRegisterForm(instance = teacher)
        print("in the else condition...")
        
    return render(request, 'update_teacher.html', {'form' : form})


@csrf_exempt
def login_user(request):
    print("Login function called")
    print("login method-----", request.method)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('user_password')
        role = request.POST.get('role')
        print("Getting user info")
        user = authenticate(request, username=username, password=password)
        print("User ----", user)
        
        if user is not None:
            print(f"Authentication done user found ---- {user}")
            login(request, user)
            
            if user.is_superuser and role == 'admin':
                return JsonResponse({
                    "success": True,
                    "role": role
                })
            elif user.role == role:
                return JsonResponse({
                    "success": True,
                    "role": role
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": {"role": "Invalid Role"}
                })

        return JsonResponse({"success": False, "errors": {"username": "Invalid username or password"}})
    return render(request, 'login.html')

    """
    Teacher can register but student can't.
    """
def register_user(request):
    teacher_form = TeacherRegisterForm()
    student_form = StudentRegisterForm()
    print("method-----", request.method)
    if request.method == 'POST':
        print("in the post method ------")    
        role = request.POST.get('role')

        if role == 'teacher':
            print("teacher condition is called -----")
            teacher_form = TeacherRegisterForm(request.POST)
            if teacher_form.is_valid():
                user = User(
                    username=teacher_form.cleaned_data['username'],
                    password=make_password(teacher_form.cleaned_data['password']),
                    email=teacher_form.cleaned_data['email'],
                    role='teacher',  
                    )
                user.save()  
                messages.success(request, 'Teacher registered successfully!')
                return redirect('login_user')
            else:
                print("Teacher form errors:", teacher_form.errors)  

        elif role == 'student':
            print("student condition is called -----")
            student_form = StudentRegisterForm(request.POST)
            if student_form.is_valid():
                user = User(
                    username=student_form.cleaned_data['username'],
                    password=make_password(student_form.cleaned_data['password']),
                    email=student_form.cleaned_data.get('email', ''),  
                    role='student',  # Set the role here
                    roll_number=student_form.cleaned_data['roll_number'],  
                )
                user.save()  
                messages.success(request, 'Student registered successfully!')
                return redirect('login_user')
            else:
                print("Student form errors:", student_form.errors)

    return render(request, 'register_user.html', {
        'teacher_form': teacher_form,
        'student_form': student_form,
    })




# def register_user(request):
#     print("Register user view triggered")  
#     teacher_form = TeacherRegisterForm()
#     student_form = StudentRegisterForm()

#     if request.method == 'POST':
#         print("Form submitted!")  
#         role = request.POST.get('role')
#         print(f"Role selected: {role}")

#         if role == 'teacher':
#             print("Processing teacher registration...")
#             teacher_form = TeacherRegisterForm(request.POST)
#             if teacher_form.is_valid():
#                 user = User(
#                     username=teacher_form.cleaned_data['username'],
#                     password=make_password(teacher_form.cleaned_data['password']),
#                     email=teacher_form.cleaned_data['email'],
#                     role='teacher',
#                 )
#                 user.save()
#                 messages.success(request, 'Teacher registered successfully!')
#                 return redirect('login_user')
#             else:
#                 print("Teacher form errors:", teacher_form.errors)

#         elif role == 'student':
#             print("Processing student registration...")
#             student_form = StudentRegisterForm(request.POST)
#             if student_form.is_valid():
#                 user = User(
#                     username=student_form.cleaned_data['username'],
#                     password=make_password(student_form.cleaned_data['password']),
#                     email=student_form.cleaned_data.get('email', ''),
#                     role='student',
#                     roll_number=student_form.cleaned_data['roll_number'],
#                 )
#                 user.save()
#                 messages.success(request, 'Student registered successfully!')
#                 return redirect('login_user')
#             else:
#                 print("Student form errors:", student_form.errors)  

#     return render(request, 'register_user.html', {
#         'teacher_form': teacher_form,
#         'student_form': student_form,
#     })
    
    
@login_required #error
def reset_password(request):
    context = {}
    print("In reset function -----")
    print("method-----", request.method)
    if request.method == "POST":
        old_pass = request.POST.get("old_password")
        new_pass = request.POST.get("new_password")
        confirm_pass = request.POST.get("confirm_password")
        print("In POST method------", old_pass)

        if not request.user.check_password(old_pass):
            print("Old password incorrect")
            context['result'] = "Old password is incorrect"
        elif not old_pass or not new_pass or not confirm_pass:
            print("All fields are required")
            context['result'] = "All fields are required."
        elif old_pass == new_pass:
            print("New password should be different")
            context['result'] = "New password should be different from the old password."
        elif new_pass != confirm_pass:
            print("Passwords do not match")
            context['result'] = "Confirm password doesn't match."
        elif len(new_pass) < 8 or not any(char.isdigit() for char in new_pass) or not any(char.isalpha() for char in new_pass):
            print("Weak password")
            context['result'] = "Password must be at least 8 characters long and contain both letters and numbers."
        else:
            print("Password successfully changed")
            user = request.user
            user.set_password(new_pass)
            user.save()

            # Prevent logout after password change
            # update_session_auth_hash(request, user)

            return redirect('login_user')

    return render(request, "reset_password.html", context)


# def resultPage(request):
#     print('result function called ------')
#     context = {}
#     print("result method-----", request.method)
#     if request.method == 'POST':
#         # print('GET method called')
#         username = User.objects.get(username = request.user)
#         try:
#             student = User.objects.get(username=username)
#         except User.DoesNotExist:
#             context['error'] = "User not found."
#             return render(request, 'student_dashboard.html', context=context)

#         exams = Exam.objects.filter(student=request.user)
#         total_marks = 0
#         marks = 0
#         for exam in exams:
#             total_marks += 5
#             if exam.is_correct():
#                 marks += 5  

#         percentage = (marks / total_marks) * 100 if total_marks > 0 else 0
        
#         context['student'] = student
#         context['exams'] = exams
#         context['total_marks'] = total_marks
#         context['marks'] = marks
#         context['percentage'] = round(percentage,2)

#         if total_marks - marks < total_marks/2:
#             context['status'] = "PASS"
#         else:
#             context['status'] = "KYU NAHI HO RAHI PADHAI"
            
        
#     return render(request, 'resultPage.html', context=context)




#--------------- Trying ajax JsonResponse ------------------

def resultPage(request):
    print('result function called ------')
    context = {}
    print("result method-----", request.method)
    if request.method == 'POST':
        print('POST method called-----', request.method)
        username = User.objects.get(username = request.user)
        try:
            student = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status = 404)

        exams = Exam.objects.filter(student=request.user)
        total_marks = 0
        marks = 0
        for exam in exams:
            total_marks += 5
            if exam.is_correct():
                marks += 5  

        percentage = (marks / total_marks) * 100 if total_marks > 0 else 0
        status = "WAAH BETA WAAH" if marks > total_marks / 2 else "KYU NAHI HO RAHI PADHAI!"
        # context['percentage'] = percentage
          
        # try:
        #     result_instance = Exam.objects.filter(student = student).first() #get the first result of the student.
        # except Exam.DoesNotExist:
        #     return JsonResponse({"error": "Result data not found for this user."}, status=404)
        
        return JsonResponse({
                "success" : True,
                "redirect_url": reverse('resultPage'),
                "total_marks": total_marks,
                "marks" : marks,
                "percentage" : round(percentage, 2),
                "status" : status,
        })
        # if exam.is_release():
        #     return JsonResponse({
        #         "total_marks": total_marks,
        #         "marks" : marks,
        #         "percentage" : round(percentage, 2),
        #         "status" : status
        #     })
        # else:
        #     return JsonResponse({
        #         "error" : "result nahi aaya hai bhai."
        #     })
        return JsonResponse({"success": "result shown successfully!"})

    return render(request, 'resultPage.html', context = context)