from django.db import models

# Create your models here.



class Contact(models.Model):
    cname = models.CharField(max_length=300)
    cemail = models.CharField(max_length=300)
    cmessage = models.TextField()
class Applications(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    phone = models.IntegerField()
    token =models.CharField(max_length=300, unique=True)
    gender= models.CharField(max_length=300)
    marital = models.CharField(max_length=300)
    dateOfBirth = models.CharField(max_length=300)
    courseName = models.CharField(max_length=300)
    primaryName = models.CharField(max_length=300)
    pcompletionYear = models.IntegerField()
    secondaryName = models.CharField(max_length=300)
    scompletionYear = models.IntegerField()
    examType = models.CharField(max_length=300)
    examYear = models.IntegerField()
    english = models.CharField(max_length=300)
    mathematics = models.CharField(max_length=300)
    biology = models.CharField(max_length=300)
    chemistry = models.CharField(max_length=300)
    physics = models.CharField(max_length=300)
    passport = models.ImageField(upload_to='application/')

class AddStudents(models.Model):
    name = models.CharField(max_length=300)
    regNo = models.CharField(max_length=300, primary_key = True )
    department = models.CharField(max_length=300)
    session = models.CharField(max_length=300)

    def __str__(self):
        return self.regNo
class Customize(models.Model):
    current_session = models.CharField(max_length=300, null =True)
    app_id_prefix = models.IntegerField(null=True)
    interview_schedule_text = models.CharField(max_length=300, null =True)

class Register(models.Model):
    username = models.ForeignKey(AddStudents,null = True, on_delete =models.SET_NULL)
    email = models.EmailField(max_length=300)
    password = models.CharField(max_length=300)
    cpassword = models.CharField(max_length=300)
class news(models.Model):
    heading = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    picture = models.ImageField(upload_to='pics')
    content = models.TextField()
    date =models.DateField()
class Students(models.Model):
    regNo = models.CharField(max_length=300, primary_key = True)
    email = models.EmailField(max_length=300,default='user@email.com', null=True)
    address = models.CharField(max_length=300, null=True)
    phone = models.IntegerField(null=True, default=0000000000000)
    gender= models.CharField(max_length=300, null=True)
    marital = models.CharField(max_length=300, null=True)
    dateOfBirth = models.DateField( null=True)
    passport = models.ImageField(upload_to='students_passport/', default= 'students_passport/default.jpg')
    status =models.CharField(max_length=300, null=True)
    adm_reference =models.CharField(max_length=300, null=True)
    nationality =models.CharField(max_length=300, null=True)
    home_town =models.CharField(max_length=300, null=True)
    place_of_birth =models.CharField(max_length=300, null=True)
    state =models.CharField(max_length=300, null=True)
    lga =models.CharField(max_length=300, null=True)
    program_type =models.CharField(max_length=300, null=True)
    n_name=models.CharField(max_length=300, null=True)
    n_address=models.CharField(max_length=300, null=True)
    n_phone=models.IntegerField(null=True, default=0000000000000)
    n_email=models.EmailField(null=True, default='user@email.com')
    n_relationship=models.CharField(max_length=300, null=True)
    disability=models.CharField(max_length=300, null=True)
    blood_grp=models.CharField(max_length=300, null=True)
    genotype=models.CharField(max_length=300, null=True)
    sponsor=models.CharField(max_length=300, null=True)
    sponsor_name=models.CharField(max_length=300, null=True)
    sport=models.CharField(max_length=300, null=True)
    extra_activities=models.CharField(max_length=300, null=True)
class TokenUser(models.Model):
    username =models.CharField(max_length=300)
    password =models.CharField(max_length=300)
class GenToken(models.Model):
    tokenNo =models.IntegerField()
    date =models.DateTimeField()
class Payments(models.Model):
    lv = (
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
    )
    students = models.ForeignKey(AddStudents, null = True, on_delete =models.SET_NULL)
    level = models.CharField(max_length=300, choices=lv, default ='100')
    amount = models.IntegerField()
    balance = models.IntegerField(null = True, default=0)
    description =models.CharField(max_length=300)
    date = models.DateTimeField()
    def __str__(self):
        return self.students.regNo
class Courses(models.Model):
    lv = (
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
    )
    pr = (
        ('PHARMACY HEALTH TECHNICIAN', 'PHARMACY HEALTH TECHNICIAN'),
        ('MEDICAL LABORATORY TECHNICIAN', 'MEDICAL LABORATORY TECHNICIAN'),
        ('COMMUNITY HEALTH', 'COMMUNITY HEALTH'),
        ('HEALTH INFORMATION MANAGEMENT', 'HEALTH INFORMATION MANAGEMENT'),
        ('PUBLIC HEALTH TECHNOLOGY', 'PUBLIC HEALTH TECHNOLOGY'),
        ('ENVIRONMENTAL HEALTH TECHNOLOGY', 'ENVIRONMENTAL HEALTH TECHNOLOGY'),
        ('EPIDEMIOLOGY AND DISEASE CONTROL', 'EPIDEMIOLOGY AND DISEASE CONTROL'),
    )
    sm = (
        ('FIRST', 'FIRST'),
        ('SECOND', 'SECOND'),
    )
    courseName =models.CharField(max_length=300)
    courseCode =models.CharField(max_length=300)
    courseUnit =models.IntegerField() 
    program = models.CharField(max_length=300, choices=pr, default ='PHARMACY HEALTH TECHNICIAN')
    level = models.CharField(max_length=300, choices=lv, default ='100')
    semester = models.CharField(max_length=300, choices=sm, default ='FIRST')

    def __str__(self):
        return self.courseName

class CourseRegistration(models.Model):
    students = models.ForeignKey(Students, null = True, on_delete =models.SET_NULL)
    program = models.CharField(max_length=300, choices=Courses.pr, default ='PHARMACY HEALTH TECHNICIAN')
    level = models.CharField(max_length=300, choices=Courses.lv, default ='100')
    semester = models.CharField(max_length=300, choices=Courses.sm, default ='FIRST')

    def __str__(self):
        return self.students.regNo
    def save(self, *args, **kwargs):
        self.students.regNo = self.students.regNo.upper()
        self.program = self.program.upper()
        self.level = self.level.upper()
        self.semester = self.semester.upper()
        super().save(*args, **kwargs)
class SourceTable(models.Model):
    lv = (
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),)
    name = models.CharField(max_length=100)
    session = models.CharField(max_length=100, choices=lv)
    score = models.IntegerField()

    def __str__(self):
        return self.name
class DestinationTable(models.Model):
    name = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    score = models.IntegerField()
    namet = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name


    

   