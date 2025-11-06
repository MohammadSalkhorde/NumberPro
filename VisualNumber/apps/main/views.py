from django.shortcuts import render
from django.conf import settings

def media_admin(request):
    return {'media':settings.MEDIA_URL,}

def index(request):
    context={
        
    }
    return render(request, 'main/index.html', context)


def about_us(request):
    return render(request, 'main/about-us.html')

def contact(request):
    return render(request, 'main/contact.html')

def test_payment_view(request):
    return render(request, 'main/test.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:index')  # اگر وارد شده بود، نره دوباره صفحه ورود

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'👋 {user.username} عزیز، خوش آمدید!')
            return redirect('main:index')  # بعد از لاگین برو به صفحه اصلی
        else:
            messages.error(request, '❌ نام کاربری یا رمز عبور اشتباه است.')
            return redirect('login')

    return render(request, 'main/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '👋 با موفقیت از حساب خارج شدید.')
    return redirect('main:index')
