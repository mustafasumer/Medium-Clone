from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from slugify import slugify

from .models import Profile
from .forms import ProfileModelForm
from blog.models import BlogPost


@login_required(login_url='user:login_view')
def user_fav_view(request):
    ids = request.user.userpostfav_set.filter(is_deleted=False).values_list('post_id', flat=True).order_by('-updated_at')
    context = dict(
        title="Favorilerim",
        favs=BlogPost.objects.filter(id__in=ids, is_active=True), 
    )
    return render(request, 'blog/post_list.html', context)



@login_required(login_url='user:login_view')
def profile_edit_view(request):
    user = request.user
    initial_data = dict(
        first_name = user.first_name,
        last_name = user.last_name,
    )
    form = ProfileModelForm(instance=user.profile, initial=initial_data)

    if request.method == "POST":
        form = ProfileModelForm(
            request.POST or None,
            request.FILES or None,
            instance=user.profile
        )
        if form.is_valid():
            f = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            f.save()
            messages.success(request, 'Profiliniz Guncellendi..')
            return redirect('user:profile_edit_view')

    title = "Profili Duzenle: "
    context = dict(
        form=form,
        title=title,
    )
    return render(request, 'common_components/form.html', context)


def login_view(request):
    # login olan kullanici direkt olarak ana sayfaya gitsin..
    if request.user.is_authenticated:
        # zaten login olmussun :)
        messages.info(request, f'{request.user.username} Daha Once Login Olmussun :)')
        return redirect('home_view')

    context = dict()
    if request.method == "POST":
        # print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if len(username) < 6 or len(password) <6:
            messages.warning(request, f'Lutfen Kullanici Adi ve Sifreyi Dogru Giriniz.. 6 Karakterden Kucuk Olmamali..')
            return redirect('user_profile:login_view')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # login oldugunu kullaniciya belli edelim!
            messages.success(request, f'{request.user.username} Login Oldun')
            return redirect('home_view')
    return render(request, 'user_profile/login.html', context)


def logout_view(request):
    messages.info(request, f'{request.user.username} Oturumun Kapatildi')
    logout(request)
    return redirect('home_view')


def register_view(request):
    context = dict()
    if request.method == "POST":
        post_info = request.POST
        email = post_info.get('email')
        email_confirm = post_info.get('email_confirm')
        first_name = post_info.get('first_name')
        last_name = post_info.get('last_name')
        password = post_info.get('password')
        password_confirm = post_info.get('password_confirm')
        instagram = post_info.get('instagram')

        if len(first_name) < 3 or len(last_name) < 3 or len(email) < 3 or len(password) < 3:
            messages.warning(request, "Bilgiler en az 3 karakterden olusmali..")
            return redirect('user_profile:register_view')

        if email != email_confirm:
            messages.warning(request, "Lutfen Email Bilgisini Dogru Giriniz..")
            return redirect('user_profile:register_view')
        
        if password != password_confirm:
            messages.warning(request, "Lutfen Sifre Bilgisini Dogru Giriniz..")
            return redirect('user_profile:register_view')
        
        user, created = User.objects.get_or_create(username=email)
        # Eger Kullanici Created Degilse Kullanici Daha Once Sisteme Kayitlidir..
        if not created:
            user_login = authenticate(request, username=email, password=password)
            if user is not None:
                messages.success(request, "Daha once kayit olmussunuz.. Ana Sayfaya Yonlendirildiniz..")
                # Kullanici Login Oldu :)
                login(request, user_login)
                return redirect('home_view')
            messages.warning(request, f'{email} adresi sistemde kayitli ama Login olamadiniz.. Login Sayfasina Yonlendiriliyorsunuz')
            return redirect('user_profile:login_view')
        user.mail = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)

        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.instagram = instagram
        profile.slug = slugify(f"{first_name}-{last_name}")
        user.save()
        profile.save()

        messages.success(request, f'{user.first_name} Sisteme Kaydedildiniz..')
        user_login = authenticate(request, username=email, password=password)
        login(request, user_login)
        return redirect('home_view')

    return render(request, 'user_profile/register.html', context)
