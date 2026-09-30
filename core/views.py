from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Post, Category, Profile
from django.contrib.auth import logout
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# صفحه شروع
def landing(request):
    # گرفتن تمام دسته‌بندی‌ها
    categories = Category.objects.all()
    top_posts = []

    # پیدا کردن پرامتیازترین پیام برای هر دسته‌بندی
    for cat in categories:
        top_post = Post.objects.filter(category=cat).order_by('-score').first()
        if top_post:
            top_posts.append(top_post)

    return render(request, 'landing.html', {'top_posts': top_posts})

# صفحه نوشتن پیام
@login_required(login_url='login')
def write_post(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        text = request.POST.get('text')

        if category_id and text:
            category = Category.objects.get(id=category_id)

            # در اینجا، علاوه بر دسته‌بندی و متن، فیلد author را هم با کاربری که
            # الان لاگین است (request.user) پر می‌کنیم.
            Post.objects.create(
                author=request.user,
                category=category,
                text=text
            )
            return redirect('landing')

    categories = Category.objects.all()
    return render(request, 'write.html', {'categories': categories})
# صفحه انتخاب دسته‌بندی برای خواندن
def choose_category(request):
    categories = Category.objects.all()
    return render(request, 'choose_category.html', {'categories': categories})

# صفحه خواندن پیام‌های یک دسته‌بندی خاص (همان کارت‌های ورق‌خوردنی)
def read_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    return render(request, 'read.html', {'posts': posts, 'category': category})

# تابع لایک کردن
def upvote(request, post_id):
    if request.method == 'POST':
        if 'voted_posts' not in request.session:
            request.session['voted_posts'] = []

        voted_posts = request.session['voted_posts']
        if post_id not in voted_posts:
            post = get_object_or_404(Post, id=post_id)
            post.score += 1
            post.save()
            voted_posts.append(post_id)
            request.session.modified = True

    # کاربر را به همان صفحه‌ای که بود برمی‌گرداند
    return redirect(request.META.get('HTTP_REFERER', 'landing'))

def signup(request):
    if request.method == 'POST':
        # دریافت اطلاعات فرم
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        avatar_choice = request.POST.get('avatar')

        # بررسی اینکه آیا این نام کاربری از قبل وجود دارد؟
        if User.objects.filter(username=user_name).exists():
            return render(request, 'signup.html', {'error': 'Username already exists. Please choose another.'})

        # ۱. ساخت کاربر جدید در دیتابیس امن جنگو
        user = User.objects.create_user(username=user_name, password=pass_word)

        # ۲. ساخت پروفایل برای ذخیره آواتار انتخابی
        Profile.objects.create(user=user, avatar=avatar_choice)

        # ۳. ورود خودکار کاربر به سایت پس از ثبت‌نام
        login(request, user)
        return redirect('landing')

    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

def login_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        # بررسی صحت نام کاربری و رمز عبور
        user = authenticate(request, username=user_name, password=pass_word)

        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')