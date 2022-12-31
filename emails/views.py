from django.shortcuts import render
from emails.models import Profile
from django.shortcuts import redirect
from django.core.mail import send_mail, send_mass_mail
# Create your views here.
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from emails.models import User, Content
from django.contrib.auth.decorators import login_required
from emails.forms import ContentForm
from django.contrib import messages


def getSubscriptionConfirmed(req, subscriber_id):

    context = {}
    name = req.session.get('name', None)
    email = req.session.get("email", None)
    confirmation_code = req.session.get('confirmation_code', None)

    if (name and email and confirmation_code):
        context = {
            "name": name,
            "email": email
        }
    else:
        return render(req, "notFound.html", context)

    del req.session["name"]
    del req.session["email"]
    del req.session['confirmation_code']

    if (not confirmation_code or not confirmation_code == subscriber_id):
        return render(req, "emails/subscription_denied.html", context)

    try:
        # create the user
        profile = Profile.objects.create(
            email=email,
            name=name
        )
    except Exception as ex:
        print("Something went wrong")
        print(ex)
        return render(req, "emails/subscription_denied.html", context)

    context["path"] = req.path
    return render(req, "emails/subscription_confirmed.html", context)


def subscribeUser(req):
    context = {}
    if (req.POST):
        email = req.POST.get('email', "")
        name = req.POST.get('name', "")

        if (email and name):
            try:

                # checking if the email already exists
                profile = Profile.objects.filter(email=email)
                if (profile):
                    return render(req, "alreadyRegistered.html", context)

                confirmation_code = f"{email}{uuid.uuid4()}{uuid.uuid4()}{datetime.now()}"
                emailUrl = f"http://localhost:8000/confirm-subscription/{confirmation_code}"

                context = {
                    "name": name,
                    "email": email,
                    "email_url": emailUrl
                }

                subject = "Important : confirm your subscription"
                html_message = render_to_string(
                    'emails/confirmation_mail.html', context)
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    html_message=html_message,
                    fail_silently=False
                )

                req.session['confirmation_code'] = confirmation_code
                req.session["name"] = name
                req.session["email"] = email

            except Exception as e:
                print(e)

    context["path"] = req.path
    return render(req, "emails/homepage.html", context)


def loginAdmin(req):
    context = {
        "path" : req.path
    }

    if (req.user.is_authenticated):
        return redirect("admin-dashboard")

    if (req.method == "POST"):
        email = req.POST['email']
        password = req.POST['password']
        try:
            user = User.objects.get(email=email)
        except Exception as ex:
            print(ex)
            print("email doesn't exist")
            return redirect('admin-login')

        user = authenticate(req, email=email, password=password)

        if (user is not None):
            login(req, user)
            messages.success(req,"😎 Admin logged in successfully")
            return redirect('admin-dashboard')
        else:
            messages.error(req,"😣 username or password is incorrect")
            return redirect('admin-login')


    return render(req, 'emails/admin/login.html', context)


@login_required(login_url='admin-login')
def adminDashboard(req):
   
    context = {}

    try:
        content = Content.objects.all()
        context = {
            "content": content
        }
    except Exception as ex:
        print(ex)

    context["path"] = req.path
    return render(req, 'emails/admin/dashboard.html', context)


@login_required(login_url='admin-login')
def getSingleContent(req, pk):
       
    context = {}
    content = None
    try:
        content = Content.objects.get(id=pk)
        print(content.coverImage)
    except:
        return render(req, "notFound.html",context)


    
    if (req.method == "POST"):
        try:
            form = ContentForm(req.POST, req.FILES, instance=content)

            if (form.is_valid()):
                form.save()
                return redirect(f"/me/dashboard/{content.id}/")
            else:
                content.description = content.description.strip()
        except:
            print("something went wrong")

    context = {
        "content": content
    }

    context["path"] = req.path
    return render(req, 'emails/admin/single-content.html', context)


@login_required(login_url='admin-login')
def createContent(req):
       
    context = {}

    if (req.method == "POST"):
        try:
            form = ContentForm(req.POST, req.FILES)
            if (form.is_valid()):
                content = form.save(commit=False)
                content.save()
                return redirect('admin-dashboard')

        except Exception as ex:
            print(ex)
    context["path"] = req.path
    return render(req, 'emails/admin/create_content.html', context)

@login_required(login_url='admin-login')
def deleteContent(req,pk):
       
    context = {}
    try:
        content = Content.objects.get(id = pk)
    except:
        return render(req, "notFound.html", context)
    print(content)

    context = {
        "content":content
    }

    if(req.method == "POST"):
        try:
            content.delete()
            return redirect("admin-dashboard")
        except Exception as ex:
            print(ex)
    context["path"] = req.path
    return render(req, 'delete.html', context)

@login_required(login_url='admin-login')
def sendMailContent(req,pk):  
    context = {}
    
    try:
        content = Content.objects.get(id = pk)
        content.coverImage = f"http://localhost:8000/images/{content.coverImage}"
        context = {"content":content}
    except:
        return render(req, "notFound.html", context)

    if(req.method == "POST"):
        try:
        
            context["current_time"] = datetime.now()
            subject = "Hey there, check out the new one!!!"
            html_message = render_to_string(
                    'emails/content_emails/sending_content.html', context)
            plain_message = strip_tags(html_message)


            profiles = Profile.objects.all()
          
            for profile in profiles:
                send_mail(
                    subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [profile.email],
                    fail_silently=False,
                    html_message=html_message
                )

            # messages =tuple(messages)

            # send_mass_mail(
            #     messages,
            #     fail_silently=False
            # )

  

            # message = EmailMultiAlternatives(subject,plain_message, settings.EMAIL_HOST_USER, emails)
            # message.attach_alternative(html_message,"text/html")
            # message.send()




            # send_mail(
            #     subject,
            #     plain_message,
            #     settings.EMAIL_HOST_USER,
            #     [emails],
            #     html_message=html_message,
            #     fail_silently=False
            # )

#             to_be_sent = (subject,plain_message, settings.EMAIL_HOST_USER,emails)
# 
#             send_mass_mail(
#                 ((subject, plain_message,settings.EMAIL_HOST_USER, emails, html_message )),
#                 fail_silently=False
#             )

            
            return redirect("admin-dashboard")
        except Exception as ex:
            print(ex)

    context["path"] = req.path
    context["current_time"] = datetime.now()
    return render(req, 'send_mail.html', context)

@login_required(login_url='admin-login')
def getAllSubscribers(req):
    context = {}
    
    try:
        subscribers = Profile.objects.all()
        context = {
            "subscribers":subscribers,
            "total_subscribers":subscribers.count()
        }
    except Exception as ex:
        pass

    context["path"] = req.path
    return render(req, 'emails/admin/subscribers.html', context)

def logoutAdmin(req):
    logout(req)
    messages.success(req, "User was successfully logged out")
    return redirect('admin-login')