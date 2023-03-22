from django.contrib import admin
from .models import Student, Mentor, Course, Lesson

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    exclude = ("last_login", "groups", "user_permissions")
    list_display = ("username", "current_profession", "preference")
    list_filter = ("current_profession", "preference")

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    exclude = ("last_login", "groups", "user_permissions")
    list_display = ("username", "profession")
    list_filter = ("profession",) 
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "mentor", "short_description", "price")
    list_filter = ("mentor", "price")
    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "duration")
    list_filter = ("course", "duration") 