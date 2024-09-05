from django.db import models

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=15)

    # Address details
    hno = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='work_experience', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    address = models.CharField(max_length=255)

class Qualification(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='qualifications', on_delete=models.CASCADE)
    qualification_name = models.CharField(max_length=255)
    percentage = models.FloatField()

class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.TextField()  # Base64 image data stored as text
