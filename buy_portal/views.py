from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import UserForm,ItemForm,AdvertiseForm
from .models import Item

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'buy_portal/login.html')
    else:
        recent_objects = Item.objects.order_by('-datetime')[:5]
        book_objects = Item.objects.filter(category='Book')[:5]
        instruments_objects = Item.objects.filter(category='Instrument')[:5]
        projects_objects = Item.objects.filter(category='Project')[:5]
        other_objects = Item.objects.filter(category='Other')[:5]
        context = {
            'recent_objects': recent_objects,
            'book_objects':book_objects,
            'instruments_objects':instruments_objects,
            'projects_objects':projects_objects,
            'other_objects':other_objects
        }
        return render(request, 'buy_portal/Home.html',context)

def item_detail(request,item_id):
    if not request.user.is_authenticated():
        return render(request, 'buy_portal/login.html')
    else:
        item=Item.objects.get(pk=item_id)
        context={
            'item':item,
        }
        return render(request, 'buy_portal/item_detail.html', context)


def sell(request):
    if not request.user.is_authenticated():
        return render(request, 'buy_portal/login.html')
    else:
        form = ItemForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            item = form.save(commit=False)
            item.user=request.user
            item.image = request.FILES['image']
            file_type = item.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/sell.html', context)
            item.save()
            return render(request, 'buy_portal/success.html')
        context={
            'form':form,
        }
        return render(request, 'buy_portal/sell.html',context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'buy_portal/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('buy_portal:index')  # redirect() accepts a view name as parameter
            else:
                return render(request, 'buy_portal/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'buy_portal/login.html', {'error_message': 'Invalid login'})
    return render(request, 'buy_portal/login.html')


def create_new_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect('buy_portal:index')
    context = {
             "form": form,
    }
    return render(request, 'buy_portal/create_new_user.html', context)

def advertise(request):
    if not request.user.is_authenticated():
        return render(request, 'buy_portal/login.html')
    else:
        form = AdvertiseForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            adv = form.save(commit=False)
            adv.user=request.user
            adv.image = request.FILES['image']
            file_type = adv.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/advertise.html', context)
            adv.save()
            return render(request, 'buy_portal/success.html')
        context={
            'form':form,
        }
        return render(request, 'buy_portal/advertise.html',context)

def requirement(request):
    if not request.user.is_authenticated():
        return render(request, 'buy_portal/login.html')
    else:
        form = AdvertiseForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            adv = form.save(commit=False)
            adv.user=request.user
            adv.image = request.FILES['image']
            file_type = adv.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/advertise.html', context)
            adv.save()
            return render(request, 'buy_portal/success.html')
        context={
            'form':form,
        }
        return render(request, 'buy_portal/advertise.html',context)