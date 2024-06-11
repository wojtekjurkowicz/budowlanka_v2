1. First clone repository: git clone https://github.com/wojtekjurkowicz/budowlanka.git
2. Then create virtual environment: py -m venv name_of_venv
3. Activate your virtual environment: source venv/bin/activate or venv/Scripts/activate
4. Install requirements: pip install -r requirements.txt
5. Create .env file and inside of it enter:
    EMAIL_HOST_USER="your_email"
    EMAIL_HOST_PASSWORD="your_password_or_app_password"
6. And last step is launching server on your localhost: py manage.py runserver