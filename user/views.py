from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from home.models import UserProfile
from house.models import Category, Comment, House, Images
from user.forms import UserUpdateForm, ProfileUpdateForm, HouseForm
from user.models import HouseImageForm

def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user)
    context = {'category': category,
               'profile': profile}
    return render(request, 'user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form}
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category})


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user)
    context = {'category': category,
               'comments': comments}
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user).delete()
    messages.error(request, 'Comment Deleted...')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def houses(request):
    category = Category.objects.all()
    current_user = request.user
    house = House.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'house': house}
    return render(request, 'user_houses.html', context)


@login_required(login_url='/login')
def addhouse(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = House()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.category = form.cleaned_data['category']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.slug = form.cleaned_data['slug']
            data.image = form.cleaned_data['image']
            data.rent = form.cleaned_data['rent']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.area = form.cleaned_data['area']
            data.location = form.cleaned_data['location']
            data.room = form.cleaned_data['room']
            data.buildingFloor = form.cleaned_data['buildingFloor']
            data.floorLocation = form.cleaned_data['floorLocation']
            data.furnished = form.cleaned_data['furnished']
            data.balconied = form.cleaned_data['balconied']
            data.heating = form.cleaned_data['heating']
            data.withintheSite = form.cleaned_data['withintheSite']
            data.fromWho = form.cleaned_data['fromWho']
            data.save()
            messages.success(request, 'Your house added successfully!')
            return HttpResponseRedirect('/user/houses')
        else:
            messages.success(request, 'Your form error! :' + str(form.errors))
            return HttpResponseRedirect('/user/addhouse')
    else:
        category = Category.objects.all()
        form = HouseForm()
        context = {'category': category,
                   'form': form}
        return render(request, 'user_addhouse.html', context)


@login_required(login_url='/login')
def edithouse(request, id):
    house = House.objects.get(id=id)
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your house updated successfully!')
            return HttpResponseRedirect('/user/houses')
        else:
            messages.success(request, 'Your form error! :' + str(form.errors))
            return HttpResponseRedirect('/user/edithouse/')
    else:
        category = Category.objects.all()
        form = HouseForm(instance=house)
        context = {'category': category,
                   'form': form}
        return render(request, 'user_addhouse.html', context)


@login_required(login_url='/login')
def deletehouse(request, id):
    current_user = request.user
    House.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your house deleted successfully!')
    return HttpResponseRedirect('/user/houses')


def houseaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = HouseImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.house_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded!')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        house = House.objects.get(id=id)
        images = Images.objects.filter(house_id=id)
        form = HouseImageForm()
        context = {
            'house': house,
            'images': images,
            'form': form
        }
        return render(request, 'house_gallery.html', context)
