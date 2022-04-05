import hashlib

from django.contrib.auth import hashers
from django.db import models


class user(models.Model):

    """
    Description: user model represents user table
    """

    genders = [
        ('SELECT', ''),
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('TRANSGENDER', 'Transgender')
    ]

    profile = models.URLField(null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=11, null=True, choices=genders)
    birth_date = models.DateField(null=True)
    joining_date = models.DateField(auto_now=True, null=False)
    address = models.TextField(null=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username


class organisationDetails(models.Model):

    """
    Description: organisation modal represents organisation table
    """

    organisationName = models.CharField(max_length=255)
    officeAddress = models.CharField(max_length=255)
    organisationSize = models.CharField(max_length=255)

    class Meta:
        db_table = 'organisationDetails'

    def __str__(self):
        return self.organisationName


class jobDetails(models.Model):

    """
    :Description: job Details class represents job details table
    """

    organisation_id = models.PositiveBigIntegerField()
    jobType = models.CharField(max_length=255)
    jobProfile = models.CharField(max_length=255)
    jobLocation = models.CharField(max_length=255)
    offeringSalary = models.CharField(max_length=255, null=True)
    postedDate = models.DateTimeField(auto_now_add=True)
    validUpto = models.DateTimeField()
    user_id = models.PositiveBigIntegerField()
    postedBy = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'jobDetails'

    def __str__(self):
        return self.jobProfile


class applicantList(models.Model):

    """
    Description: applicantList model represents applicant table
    """

    user_id = models.BigIntegerField()
    job_id = models.BigIntegerField()
    appliedDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applicant'
