from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import User

class Student(User):   
    
    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    
    profession_choices = (
    ("10th pass", "10th pass"),
    ("12th pass", "12th pass"),
    ("Dropper", "Dropper"),
    ("Cadet", "Cadet"),
    ("Other", "Other"),
)
    
    preference_choices = (
    ("Army", "Army"),
    ("Navy", "Navy"),
    ("Air Force", "Air Force"),
    ("Other", "Other"),
)
     
    bio = models.TextField(max_length=900)
    
    dob = models.DateField()
    mobile_no = models.IntegerField()
    preference = models.CharField(choices = preference_choices, default = "Other", max_length=20)
    current_profession = models.CharField(choices = profession_choices, default = "Male", max_length=20)
    address = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=100)
    
    followers = models.ManyToManyField('Mentor', related_name='students_following', default=0)
    
    gender = models.CharField(choices = gender_choices, default = "Male", max_length=20)
    
    profile = models.ImageField(upload_to="profile", null=True, blank=True)

    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Students"
        verbose_name = "Student"
    
class Mentor(User):
    
    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    
    field_choices = (
    ("Army", "Army"),
    ("Navy", "Navy"),
    ("Air Force", "Air Force"),
    ("Other", "Other"),
)
    
    post_choices = [
    ('Army', (
        ('General', 'General'),
        ('Colonel', 'Colonel'),
        ('Major', 'Major'),
        ('Captain', 'Captain'),
        ('Lieutenant', 'Lieutenant'),
    )),
    ('Navy', (
        ('Admiral', 'Admiral'),
        ('Commander', 'Commander'),
        ('Lieutenant Commander', 'Lieutenant Commander'),
        ('Lieutenant', 'Lieutenant'),
        ('Ensign', 'Ensign'),
    )),
    ('Air Force', (
        ('Air Marshal', 'Air Marshal'),
        ('Air Commodore', 'Air Commodore'),
        ('Group Captain', 'Group Captain'),
        ('Wing Commander', 'Wing Commander'),
        ('Squadron Leader', 'Squadron Leader'),
    )),
]

    
    bio = models.TextField(max_length=900)
    dob = models.DateField()
    
    join_date = models.DateField()
    retired_date = models.DateField()
    
    work_experience = models.IntegerField()

    profession = models.CharField(choices = field_choices, default = "Other", max_length=20)
    
    post = models.CharField(max_length=20, choices=post_choices)

    
    gender = models.CharField(choices = gender_choices, default = "Male", max_length=20)
    
    followers = models.ManyToManyField('Student', related_name='mentors_following', blank=True, null=True)

    profile = models.FileField(upload_to="profile", null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Mentors"
        verbose_name = "Mentor"

# ========================================== courses ======================================

class Course(models.Model):
    title = models.CharField(max_length=200)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True, auto_created=False)
    short_description = models.TextField(blank=False, max_length=60)
    description = models.TextField(blank=False)
    
    total_enrollment = models.IntegerField(default=0)
    price = models.FloatField(validators=[MinValueValidator(9.99)])
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_url = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    duration = models.FloatField(validators=[MinValueValidator(0.30), MaxValueValidator(30.00)])
    video_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
