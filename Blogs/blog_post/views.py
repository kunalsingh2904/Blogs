from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from .models import Blogpost, Querysearch, Commentsblog
from .forms import Contactform, Blogform, Blogmodelform, Userform
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_random():
    num = random.randrange(100001, 999998)
    return num


def send_mail_register(to_email, number):
    with open('file.txt', 'r') as f:
        from_id = f.readline()
        pass_word = f.readline()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    msg = MIMEMultipart()
    msg['From'] = from_id
    msg['To'] = to_email
    msg['Subject'] = "OTP for registration on Blogs"
    body = "OTP to register your account on Blogs is " + str(number)
    body1 = "please enter this otp on website to confirm your account."
    body2 = "Thank You for using Blogs."
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body1, 'plain'))
    msg.attach(MIMEText(body2, 'plain'))
    text = msg.as_string()
    server.login(from_id, pass_word)
    server.sendmail(from_id, to_email, text)
    server.quit()


'''
def blog_details_id(request, post_id):
    try:
        obj1 = Blogpost.objects.get(id=post_id)
    except:
        raise Http404

    # obj1 = get_object_or_404(Blogpost, id = post_id)         # this can also be used

    return render(request, "blog_post/index.html", {'obj': [obj1]})
'''


def blog_details_idd(request, slug):
    obj1 = get_object_or_404(Blogpost, slug=slug)
    return render(request, "blog_post/index.html", {'obj': [obj1]})


def blog_post_list(request):
    # list out object // could be searched
    qs = Blogpost.objects.all()
    if len(qs) <= 0:
        qs = None
    temp_name = "blog_post/list.html"
    content = {'context': qs}
    return render(request, temp_name, content)


'''
def blog_post_create(request):                # using Blogform
    # create object using a form
    form = Blogform(request.POST or None)
    if form.is_valid():
        obj = Blogpost.objects.create(**form.cleaned_data)          # automatic save to database
        form = Blogform()
    temp_name = 'blog_post/create.html'
    content = {'form': form}
    return render(request, temp_name, content)

'''


# these two can be used to prevent any user to view this views. any one can also be used
@login_required      # LOGIN_URL has been added to settings.py
# @staff_member_required
def blog_post_create(request):                # using Blogform
    # create object using a form
    form = Blogmodelform(request.POST or None, request.FILES or None)    # 2nd argument for image field
    if form.is_valid():
        # form.save()          # automatic save to database
        # manupulating data
        obj = form.save(commit=False)
        # count = len(Blogpost.objects.all())
        obj.title = form.cleaned_data.get('title') #+ str(count + 1)   # here edit details of form
        obj.user = request.user
        obj.save()                          # good method

        form = Blogmodelform()
        return redirect('/blog')
    temp_name = 'blog_post/create.html'
    content = {'form': form}
    return render(request, temp_name, content)


@login_required
# @staff_member_required
def blog_post_delete(request, slug):
    obj = get_object_or_404(Blogpost, slug=slug)
    temp_name = "blog_post/delete.html"
    if request.method == "POST":
        obj.delete()
        return redirect('/blog')
    content = {'obj': obj}
    return render(request, temp_name, content)


@staff_member_required
def blog_comm_delete(request, del_slug, del_id):
    kk = get_object_or_404(Blogpost, slug=del_slug)
    obj = get_object_or_404(Commentsblog, blogs=kk, id=del_id)
    obj.delete()
    return redirect('/blog/{}/detail'.format(del_slug))


@login_required
# @staff_member_required
def blog_post_update(request, slug):
    # create object using a form
    obj = get_object_or_404(Blogpost, slug=slug)
    temp_name = 'blog_post/update.html'
    form = Blogmodelform(request.POST or None, request.FILES or None, instance=obj)   # instance send the data to form
    if form.is_valid():
        form.save()
        return redirect('/blog')
    content = {'form': form, 'title': f"update {obj.title}"}
    return render(request, temp_name, content)


def blog_post_detail(request, slug):
    #  1 object -> details

    temp_name = "blog_post/index.html"
    obj = get_object_or_404(Blogpost, slug=slug)
    types = False
    if request.user.is_authenticated:
        if obj.user.username == request.user.username:
            types = True
    comment = Commentsblog.objects.filter(blogs=obj)
    content = {'item': obj, 'comment': comment, 'types': types}
    return render(request, temp_name, content)


def contact_page(request):
    form = Contactform(request.POST or None)
    obj = None
    if form.is_valid():
        obj = form.cleaned_data
        form = Contactform()
    return render(request, 'blog_post/fform.html', {'title': "contact us", 'form': form, 'obj': obj})


def search_blog(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    content = {"query": query}
    if query is not None:

        # query = str(query)
        Querysearch.objects.create(user=user, query=query)
        blog_list = Blogpost.objects.filter(Q(title__contains=query) | Q(user__username__icontains=query))

        content['blog_list'] = blog_list
    return render(request, 'blog_post/search.html', content)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']  # we are using <input> type as we have no database in models for login/logout
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/blog')

        else:
            return render(request, 'blog_post/login.html', {'message': "Invalid login"})
    return render(request, 'blog_post/login.html')


def register_user(request):
    form = Userform(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # email = form.cleaned_data['email']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/blog')
    content = {'form': form}
    return render(request, 'blog_post/register.html', content)


'''


def register_user(request):
    form = Userform(request.POST or None)
    if form.is_valid():
        # user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        number = str(generate_random())
        send_mail_register(email, number)
        content = {'username': username, 'password': password, 'email': email, 'number': number}
        return render(request, 'blog_post/reg_otp.html', content)
    content = {'form': form}
    return render(request, 'blog_post/register.html', content)


def match_reg_otp(request, username, number, password, email):
    enter_otp = request.GET.get('num', None)
    if str(enter_otp) == str(number):
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.save()
        userr = authenticate(username=username, password=password)
        #if userr is not None:
            # if userr.is_active:                # something problem here
        login(request, userr)
        return redirect('/blog')
    else:
        message = "OTP does not matched. Enter again or click try again to register"
        content = {'username': username, 'password': password, 'email': email, 'number': number, 'message': message}
        return render(request, 'blog_post/reg_otp.html', content)
'''

def logout_user(request):
    logout(request)
    return redirect('/')


def add_comment(request, slug):
    to_post = request.GET.get('comm', None)
    blog_temp = get_object_or_404(Blogpost, slug=slug)
    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = "unknown"
    if to_post is not None:
        Commentsblog.objects.create(blogs=blog_temp, comment=to_post, user=user)
    return redirect('/blog/' + slug + '/detail')









