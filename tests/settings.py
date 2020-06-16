import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "django_address"))

SECRET_KEY = "NOTREALLY"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3"),}}

INSTALLED_APPS = ["django.contrib.contenttypes", "django_address", "example.order", ]
