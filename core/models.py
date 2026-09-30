from django.db import models
from django.contrib.auth.models import User

# ۱. جدول جدید: پروفایل کاربران برای ذخیره آواتار
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=50, default='avatar1', verbose_name="آواتار")

    def __str__(self):
        return f"{self.user.username} Profile"

# ۲. جدول دسته‌بندی‌ها
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام دسته")
    is_angel = models.BooleanField(default=False, verbose_name="آیا مربوط به حالت فرشته است؟")

    def __str__(self):
        mode_name = "Angel" if self.is_angel else "Devil"
        return f"{self.name} ({mode_name})"

# ۳. جدول پیام‌ها
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="نویسنده")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی پیام")
    text = models.TextField(max_length=280, verbose_name="متن پیام")
    score = models.IntegerField(default=0, verbose_name="امتیاز کاربران")
    is_pinned = models.BooleanField(default=False, verbose_name="آیا برترین پست ماه است؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان انتشار")

    def __str__(self):
        return f"{self.category.name}: {self.text[:30]}..."