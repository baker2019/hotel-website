import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile, Faq
from house.models import House, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    slider_data = House.objects.all()[:3]
    category = Category.objects.all()
    random_houses = House.objects.all()[:6]
    last_houses = House.objects.all().order_by('-id')[:6]
    context = {'setting': setting,
               'slider_data': slider_data,
               'page': 'home',
               'category': category,
               'random_houses': random_houses,
               'last_houses': last_houses,
               }
    return render(request, 'index.html', context)



def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarıyla gönderilmiştir.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form}
    return render(request, 'iletisim.html', context)


def category_houses(request, id, slug):
    houses = House.objects.filter(category_id=id)
    category = Category.objects.all()
    categoryData = Category.objects.get(pk=id)
    context = {'houses': houses, 'category': category, 'categoryData': categoryData}
    return render(request, 'houses.html', context)


def house_detail(request, id, slug):
    category = Category.objects.all()
    house = House.objects.get(pk=id)
    images = Images.objects.filter(house_id=id)
    comments = Comment.objects.filter(house_id=id, status='True')
    context = {'house': house,
               'category': category,
               'images': images,
               'comments': comments}
    return render(request, 'house_detail.html', context)


def house_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            houses = House.objects.filter(title__icontains=query)
            context = {'houses': houses,
                       'category': category,
                       }
            return render(request, 'house_search.html', context)
    return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "Login Hatası! Kullanıcı adı veya şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.jpg"
            data.save()
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form}
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = Faq.objects.all().order_by('orderNumber')
    context = {'category': category,
               'faq': faq
               }
    return render(request, 'sss.html', context)

