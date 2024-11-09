from django.core.management.base import BaseCommand
from project_management.models import Project, Task
from random import randint
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add sample data for testing purposes'

    def handle(self, *args, **kwargs):
        # Delete any existing projects and tasks to avoid duplicates
        Project.objects.all().delete()
        Task.objects.all().delete()

        # Sample Persian titles and descriptions
        project_names = [
            "پروژه توسعه نرم‌افزار پزشکی",
            "پروژه بهبود رابط کاربری",
            "پروژه تحلیل داده‌های سلامت",
            "پروژه یادگیری ماشین",
            "پروژه توسعه پایگاه داده",
        ]
        
        project_descriptions = [
            "این پروژه به منظور توسعه نرم‌افزارهای پزشکی انجام می‌شود و شامل تحلیل نیازمندی‌ها و برنامه‌ریزی اولیه است.",
            "در این پروژه به بهبود رابط کاربری و طراحی تجربه کاربری پرداخته می‌شود تا کاربران راحت‌تر بتوانند از نرم‌افزار استفاده کنند.",
            "هدف این پروژه تحلیل داده‌های پزشکی و سلامت با استفاده از ابزارهای تحلیل داده است.",
            "در این پروژه از روش‌های یادگیری ماشین برای پیش‌بینی و طبقه‌بندی استفاده می‌شود.",
            "پروژه توسعه پایگاه داده شامل طراحی، ساخت و نگهداری یک پایگاه داده بزرگ برای ذخیره اطلاعات پزشکی است.",
        ]
        
        task_titles = [
            "تجزیه و تحلیل نیازمندی‌ها",
            "طراحی اولیه",
            "پیاده‌سازی رابط کاربری",
            "تست واحد",
            "بهبود عملکرد سیستم",
            "مستندسازی پروژه",
            "تحلیل داده‌ها",
            "برنامه‌ریزی و زمان‌بندی",
            "بررسی امنیت",
            "مدیریت داده‌ها",
        ]
        
        task_descriptions = [
            "این وظیفه شامل بررسی نیازمندی‌های مشتریان و مستندسازی آنها است.",
            "وظیفه طراحی اولیه شامل ایجاد طرح‌های اولیه و نمودارها است.",
            "پیاده‌سازی رابط کاربری برای فراهم کردن تجربه کاربری بهتر برای کاربران.",
            "اجرای تست‌های واحد به منظور شناسایی مشکلات و بهبود کیفیت نرم‌افزار.",
            "بهبود عملکرد سیستم با بهینه‌سازی کدها و به‌روزرسانی‌ها.",
            "مستندسازی پروژه به منظور حفظ اطلاعات برای تیم و آینده پروژه.",
            "تحلیل داده‌ها با استفاده از ابزارهای مدرن و گزارش نتایج.",
            "برنامه‌ریزی و زمان‌بندی به منظور مدیریت بهتر زمان و منابع.",
            "بررسی امنیت و حفاظت از اطلاعات حساس کاربران.",
            "مدیریت و نگهداری داده‌های پزشکی در پایگاه داده پروژه.",
        ]

        # Create sample projects
        for i in range(len(project_names)):
            project = Project.objects.create(
                name=project_names[i],
                description=project_descriptions[i],
            )
            
            # Create 5-10 sample tasks for each project with random difficulty levels
            for j in range(randint(5, 10)):
                Task.objects.create(
                    project=project,
                    title=task_titles[j % len(task_titles)],
                    description=task_descriptions[j % len(task_descriptions)],
                    difficulty=randint(1, 10),
                )

        print("Sample data added successfully!")

