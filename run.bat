@echo off
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); import os; email=os.getenv('DEFAULT_ADMIN_EMAIL','Yusufarslan@thesocialfootball.com'); password=os.getenv('DEFAULT_ADMIN_PASSWORD','thesocialfootballadmin'); U.objects.filter(email=email).exists() or U.objects.create_superuser(username=email,email=email,password=password)"
python manage.py runserver
pause
