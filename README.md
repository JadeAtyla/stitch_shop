# Follow Steps to Run Backend

1. Go to your command prompt in vscode, and redirect to backend folder:
```bash
cd backend
```

2. Install env folder for environment storage:
```bash
python -m venv env
```

3. Activate environment:
```bash
env\Scripts\activate
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

5. Redirect to stitch_backend folder:
```bash
cd stitch_backend
```

6. Creat an ".env":
```bash
# this is a root directory
.\stitch_backend\.env
```

7. Open the .env and input this necessary data:
```bash
DJANGO_SECRET_KEY='django-insecure-n3gy^vi6+dqu5%bqk2jqryk&&9n&sw*#$e(!q&!3!3)+nkus1i'
DATABASE_NAME='stitchshop'
DATABASE_USER='YOUR_DB_USER' # change this
DATABASE_PASSWORD='YOUR_DB_PASS' # and this
DATABASE_HOST='localhost'
DATABASE_PORT='3306'
DEBUG='True'
```

8. Make migrations of your models to your sql:
```bash
py manage.py makemigrations
```
or
```bash
python manage.py makemigrations
```

9. Then migrate your models:
```bash
py manage.py migrate
```
or
```bash
python manage.py migrate
```

10. Create superuser:
```bash
py manage.py createsuperuser
```
or
```bash
python manage.py createsuperuser
```

11. Run django server:
```bash
py manage.py runserver
```
or
```bash
python  manage.py runserver
```

# Setup your Database First
1. Open your mysql
2. Open a query tab and use *stitchshop*:
```bash
USE stitchshop;
```
3. Copy and paste the content from *backend/insert_products.txt* to the query tab:
```bash
USE stitchshop;
# put here the copied insert data query
```
4. Reload django server:
```bash
py manage.py runserver
```
or
```bash
python  manage.py runserver
```