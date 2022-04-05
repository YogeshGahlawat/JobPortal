import datetime
import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import hashers
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from authentication.models import user, organisationDetails, jobDetails, applicantList
from CODES import *


def renderRegister(request):
    """
    :Description: view to render register page
    :param request:
    :return:
    """

    if request.method == 'POST':
        if ' ' in request.POST['name']:
            first_name, last_name = request.POST['name'].split()
            first_name, last_name = first_name.capitalize(), last_name.capitalize()
        else:
            first_name, last_name = request.POST['name'].capitalize(), None
        email = request.POST['email']
        password = hashers.make_password(request.POST['password1'])

        try:
            user.objects.get(email=email)
            messages.warning(request, f'already have an account with this {email}')
            return redirect('login')
        except user.DoesNotExist:
            if email.find('@gmail.com'):
                username = email.removesuffix('@gmail.com')
            elif email.find('@yahoo.com'):
                username = email.removesuffix('@yahoo.com')
            elif email.find('@outlook.com'):
                username = email.removesuffix('@outlook.com')
            elif email.find('@hotmail.com'):
                username = email.removesuffix('@hotmail.com')
            newuser = user(first_name=first_name, last_name=last_name, username=username,
                           email=email, password=password)
            newuser.save()
            messages.success(request, 'Thanks for registering with us')
            return redirect('login')

    return render(request, 'authentication/register.html', context={'title': 'Registration'})


def renderLogin(request):
    """
    :Description: view to render login
    :param request:
    :return:
    """

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            userdata = user.objects.get(email=email)
            if userdata and hashers.check_password(password, user.objects.get(email=email).password):
                username = userdata.username
            else:
                raise user.DoesNotExist
            response = redirect('dashboard')
            response.set_signed_cookie('username', username, salt='username')
            return response
        except user.DoesNotExist:
            messages.warning(request, 'User doesn\'t exist')
            return redirect('register')

    return render(request, 'authentication/login.html', context={'title': 'Login'})


def renderDashboard(request):
    """
    :Description: view to render user dashboard
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'Session has expired')
        return redirect('login')

    return render(request, 'authentication/dashboard.html',
                  {'title': 'Dashboard', 'username': request.get_signed_cookie('username', salt='username')})


def renderLogout(request):
    """
    :Description: view to log out the user
    :param request:
    :return:
    """

    if 'username' in request.COOKIES:
        response = redirect('login')
        response.delete_cookie('username')
        return response
    return redirect('login')


@csrf_exempt
def userProfile(request):
    """
    :Description: view function to display user profile information
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning('session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            try:
                userObject = user.objects.filter(username=username)
                userdata = json.loads(serializers.serialize('json', userObject))
                return JsonResponse({
                    'data': userdata
                })
            except user.DoesNotExist:
                pass


@csrf_exempt
def postJob(request):
    """
    :Description: view function to post new job
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':

            organisationName = request.POST['organisationName']
            organisationScale = request.POST['organisationScale']
            officeAddress = request.POST['officeAddress']
            jobProfile = request.POST['jobProfile']
            jobType = request.POST['jobType']
            jobDescription = request.POST['jobDescription']
            jobLocation = request.POST['jobLocation'].capitalize()
            offeringSalary = request.POST['offeringSalary']
            offerValidUpto = request.POST['offerValidUpto']
            postedBy = request.POST['postedBy'].upper()
            contactNumber = request.POST['contactNumber']
            emailAddress = request.POST['emailAddress'].lower()

            try:
                user_id = user.objects.get(username=request.get_signed_cookie('username', salt='username')).id

                organisation_id = None
                organisation = organisationDetails.objects.filter(organisationName=organisationName).first()
                if organisation is not None:
                    organisation_id = organisation.id
                else:
                    organisation = organisationDetails(organisationName=organisationName,
                                                       officeAddress=officeAddress,
                                                       organisationSize=organisationScale)
                    organisation.save()
                    organisation_id = organisation.id

                job = jobDetails(organisation_id=organisation_id, jobType=jobType, jobProfile=jobProfile,
                                 jobLocation=jobLocation, description=jobDescription, offeringSalary=offeringSalary,
                                 validUpto=offerValidUpto, user_id=user_id, postedBy=postedBy, mobile=contactNumber,
                                 email=emailAddress)
                job.save()
                message = 'Job posted successfully'
                message_tag = 'success'

            except (user.DoesNotExist, organisationDetails.DoesNotExist, jobDetails.DoesNotExist, Exception) as e:
                message = 'Job posting fails'
                message_tag = 'warning'
                print(e)

            return JsonResponse({
                'message': message,
                'message_tag': message_tag
            })
    return render(request, 'authentication/postJob.html',
                  {'title': 'Post Job', 'username': request.get_signed_cookie('username', salt='username')})


@csrf_exempt
def postedJobs(request):
    """
    Description: view list of posted jobs
    :param request:
    :return:
    """
    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            try:
                user_id = user.objects.get(username=username).id
                postedjobs = jobDetails.objects.filter(user_id=user_id)
                serialixed_data = serializers.serialize('json', postedjobs)
                data = json.loads(serialixed_data)
                for count in range(len(data)):
                    if data[count]['fields']['jobType'] == '1':
                        data[count]['fields']['jobType'] = JOB_TYPE[0]
                    elif data[count]['fields']['jobType'] == '2':
                        data[count]['fields']['jobType'] = JOB_TYPE[1]
                    elif data[count]['fields']['jobType'] == '3':
                        data[count]['fields']['jobType'] = JOB_TYPE[2]

                    if data[count]['fields']['jobProfile'] == '1':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[0]
                    elif data[count]['fields']['jobProfile'] == '2':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[1]
                    elif data[count]['fields']['jobProfile'] == '3':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[2]
                    elif data[count]['fields']['jobProfile'] == '4':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[3]
                    elif data[count]['fields']['jobProfile'] == '5':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[4]

                    data[count]['fields']['postedDate'] = parse_datetime(data[count]['fields']['postedDate']).strftime(
                        "%d %b %Y")
                    data[count]['fields']['validUpto'] = parse_datetime(data[count]['fields']['validUpto']).strftime(
                        "%d %b %Y")
                    organisation = organisationDetails.objects.get(id=data[count]['fields']['organisation_id'])
                    data[count]['fields']['organisation_name'] = organisation.organisationName

                return JsonResponse({
                    'data': data
                })
            except (user.DoesNotExist, jobDetails.DoesNotExist) as e:
                pass


@csrf_exempt
def removeJob(request):
    """
    Description: view function to delete a job
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            job_id = request.POST['job_id']

            try:
                jobDetails.objects.get(id=job_id).delete()
                return JsonResponse({
                    'message': 'Job removed Successfully'
                })
            except jobDetails.DoesNotExist as e:
                pass


@csrf_exempt
def candidateList(request):

    """
    Description: view function to list applied candidates list
    :param request:
    :return:
    """

    user_list = []
    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            jobProfile = request.POST['jobProfile']
            jobType = request.POST['jobType']
            try:
                user_id = user.objects.get(username=username).id
                postedJobs = jobDetails.objects.filter(user_id=user_id, jobProfile= jobProfile, jobType= jobType)
                postedJobs = json.loads(serializers.serialize('json', postedJobs))
                for i in range(len(postedJobs)):
                    if applicantList.objects.filter(job_id=postedJobs[i]['pk']).exists():
                        user_id = applicantList.objects.filter(job_id=postedJobs[i]['pk'])
                        user_id = json.loads(serializers.serialize('json', user_id))
                        for j in range(len(user_id)):
                            if user.objects.filter(id=user_id[j]['fields']['user_id']).exists():
                                userdata = user.objects.filter(id=user_id[j]['fields']['user_id'])
                                user_list.append(json.loads(serializers.serialize('json', userdata)))
                return JsonResponse({
                    'status_code': 200,
                    'data': user_list
                })
            except user.DoesNotExist as e:
                return JsonResponse({
                    'status_code': 404,
                    'message': e
                })

    return render(request, 'authentication/candidate_list.html',
                  {'title': 'Candidates List', 'username': request.get_signed_cookie('username', salt='username')})


@csrf_exempt
def searchJob(request):

    """
    :Description: view function to post new job
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            jobProfile = request.POST['jobProfile']
            jobType = request.POST['jobType']
            try:
                jobs = jobDetails.objects.filter(jobProfile=jobProfile, jobType=jobType,
                                                 validUpto__gte=datetime.datetime.now())
                data = serializers.serialize('json', jobs)
                data = json.loads(data)
                for count in range(len(data)):
                    if data[count]['fields']['jobType'] == '1':
                        data[count]['fields']['jobType'] = JOB_TYPE[0]
                    elif data[count]['fields']['jobType'] == '2':
                        data[count]['fields']['jobType'] = JOB_TYPE[1]
                    elif data[count]['fields']['jobType'] == '3':
                        data[count]['fields']['jobType'] = JOB_TYPE[2]

                    if data[count]['fields']['jobProfile'] == '1':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[0]
                    elif data[count]['fields']['jobProfile'] == '2':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[1]
                    elif data[count]['fields']['jobProfile'] == '3':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[2]
                    elif data[count]['fields']['jobProfile'] == '4':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[3]
                    elif data[count]['fields']['jobProfile'] == '5':
                        data[count]['fields']['jobProfile'] = JOB_PROFILE[4]

                    data[count]['fields']['postedDate'] = parse_datetime(data[count]['fields']['postedDate']).strftime(
                        "%d %b %Y")
                    data[count]['fields']['validUpto'] = parse_datetime(data[count]['fields']['validUpto']).strftime(
                        "%d %b %Y")
                    organisation = organisationDetails.objects.get(id=data[count]['fields']['organisation_id'])
                    data[count]['fields']['organisation_name'] = organisation.organisationName
                return JsonResponse({
                    'status_code': 200,
                    'data': data
                })
            except (jobDetails.DoesNotExist, organisationDetails.DoesNotExist) as e:
                return JsonResponse({
                    'status_code': 404,
                    'message': e,
                    'message_tag': 'warning'
                })

    return render(request, 'authentication/searchJobs.html',
                  {'title': 'Search for Job', 'username': request.get_signed_cookie('username', salt='username')})


@csrf_exempt
def applyJob(request):
    """
    Description: view function to apply for a job
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            job_id = request.POST['job_id']
            print(username, job_id)
            try:
                user_id = user.objects.get(username=username).id
                applicant = applicantList.objects.filter(user_id=user_id, job_id=job_id).exists()
                if applicant:
                    message = 'You have already applied'
                else:
                    applicantList(user_id=user_id, job_id=job_id, appliedDate=datetime.datetime.now()).save()
                    message = 'You applied successfully'
                return JsonResponse({
                    'message': message,
                    'message_tag': 'success'
                })
            except (user.DoesNotExist, applicantList.DoesNotExist, jobDetails.DoesNotExist) as e:
                return JsonResponse({
                    'message': e,
                    'message_tag': 'warning'
                })


@csrf_exempt
def appliedJobs(request):
    """
    Description: view function to list applied jobs
    :param request:
    :return:
    """

    appliedList = []
    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            try:
                user_id = user.objects.get(username=username).id
                job_ids = applicantList.objects.filter(user_id=user_id)
                job_ids = serializers.serialize('json', job_ids)
                job_ids = json.loads(job_ids)
                for i in range(len(job_ids)):
                    job_id = job_ids[i]['fields']['job_id']
                    jobs = jobDetails.objects.filter(id=job_id)
                    data = serializers.serialize('json', jobs)
                    data = json.loads(data)
                    for count in range(len(data)):
                        if data[count]['fields']['jobType'] == '1':
                            data[count]['fields']['jobType'] = JOB_TYPE[0]
                        elif data[count]['fields']['jobType'] == '2':
                            data[count]['fields']['jobType'] = JOB_TYPE[1]
                        elif data[count]['fields']['jobType'] == '3':
                            data[count]['fields']['jobType'] = JOB_TYPE[2]

                        if data[count]['fields']['jobProfile'] == '1':
                            data[count]['fields']['jobProfile'] = JOB_PROFILE[0]
                        elif data[count]['fields']['jobProfile'] == '2':
                            data[count]['fields']['jobProfile'] = JOB_PROFILE[1]
                        elif data[count]['fields']['jobProfile'] == '3':
                            data[count]['fields']['jobProfile'] = JOB_PROFILE[2]
                        elif data[count]['fields']['jobProfile'] == '4':
                            data[count]['fields']['jobProfile'] = JOB_PROFILE[3]
                        elif data[count]['fields']['jobProfile'] == '5':
                            data[count]['fields']['jobProfile'] = JOB_PROFILE[4]

                        data[count]['fields']['postedDate'] = parse_datetime(
                            data[count]['fields']['postedDate']).strftime(
                            "%d %b %Y")
                        data[count]['fields']['validUpto'] = parse_datetime(
                            data[count]['fields']['validUpto']).strftime(
                            "%d %b %Y")
                        organisation = organisationDetails.objects.get(id=data[count]['fields']['organisation_id'])
                        data[count]['fields']['organisation_name'] = organisation.organisationName
                        appliedList.append(data)
                return JsonResponse({
                    'data': appliedList
                })
            except (user.DoesNotExist, jobDetails.DoesNotExist, organisationDetails.DoesNotExist,
                    applicantList.DoesNotExist) as e:
                return JsonResponse({
                    'message': e
                })


@csrf_exempt
def withdrawApplication(request):
    """
    Description: view function to withdraw the application
    :param request:
    :return:
    """

    if 'username' not in request.COOKIES:
        messages.warning(request, 'session has expired')
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            job_id = request.POST['job_id']

            try:
                user_id = user.objects.get(username=username).id
                applicantList.objects.get(job_id=job_id, user_id=user_id).delete()
                return JsonResponse({
                    'message': 'Your application withdrawal successfully completed',
                    'message_tag': 'success'
                })
            except (user.DoesNotExist, applicantList.DoesNotExist) as e:
                return JsonResponse({
                    'message': 'Your application withdrawal failed',
                    'message_tag': 'warning'
                })
