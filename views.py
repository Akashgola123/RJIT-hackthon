from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.contrib import messages
from .models import Student, Mentor, Course


def login(request):

    if request.method == "POST":
        username = request.POST.get("USERNAME")
        password = request.POST.get("PASSWORD")

        student = auth.authenticate(username=username, password=password)
        if student is not None:

            auth.login(request, student)
            return redirect("student_home")

        else:
            messages.error(request, "Invalid Credentials")

    return render(request, "login.html")


def site_logout(request):
    logout(request)
    request.session.flush()
    return redirect("/")


def signup(request):
    if request.method == 'POST':

        username = request.POST.get("USERNAME")
        
        if Student.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup")
        
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")
        
        first_name = request.POST.get("FIRST_NAME")
        last_name = request.POST.get("LAST_NAME")
        
        bio = request.POST.get("BIO")
        dob = request.POST.get("DOB")
        mobile_no = request.POST.get("MOBILE_NO")
        preference = request.POST.get("PREFERENCE")
        current_profession = request.POST.get("CURRENT_PROFESSION")
        address = request.POST.get("ADDRESS")
        linkedin = request.POST.get("LINKEDIN")
        gender = request.POST.get("GENDER")
        profile = request.FILES.get("PROFILE")

        student = Student.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            mobile_no=mobile_no,
            preference=preference,
            current_profession=current_profession,
            address=address,
            linkedin=linkedin,
            gender=gender,
            bio=bio,
            profile=profile
        )
        
        student.set_password(password)

        student.save()

        messages.success(
            request, f"{ first_name } has been registered scessfully! Login now.")

        return redirect("login")

    return render(request, 'signup.html')

# ================================ STUDENT HOME ================================

@login_required(login_url='/')
def student_home(request):
    
    student = Student.objects.get(id=request.user.id)
    
    courses = Course.objects.all()
    mentors = Mentor.objects.exclude(id__in=student.followers.all())

    parameters = {
        "user": request.user,
        "courses": courses,
        "mentors": mentors
    }
    return render(request, "student/home.html", parameters)



@login_required(login_url='/')
def profile(request, id):

    user = Student.objects.get(id=id)

    parameters = {
        "user": user,
    }

    return render(request, "student/profile.html", parameters)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def add_follower(request, id):
    mentor = Mentor.objects.get(id=id)
    student = Student.objects.get(id=request.user.id)

    mentor.followers.add(student)
    
    print("Added follower!")

    return redirect("student_home")