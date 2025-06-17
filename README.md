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

8. Delete and Create Database:
### for Deleting Existing Database
```bash
py manage.py obliterate
```
or
```bash
python manage.py obliterate
```

### for Creating Database
```bash
py manage.py createdb
```
or
```bash
py manage.py createdb
```

9. Make migrations of your models to your sql:
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

10. Seed categories and products to database:
```bash
py manage.py seed
```
```bash
python manage.py seed
```

11. Create superuser:
```bash
py manage.py createsuperuser
```
or
```bash
python manage.py createsuperuser
```

12. Run django server:
```bash
py manage.py runserver
```
or
```bash
python  manage.py runserver
```

# No need sql setup, this django setup seeds all data needed.