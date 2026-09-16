import os
import sys

# 1. Update settings.py
settings_code = '''
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sop-crud-library-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'books',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'library_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
'''
with open('library_backend/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_code.strip())
print("1/5: settings.py configured!")

# 2. Update books/models.py
models_code = '''
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    rating = models.FloatField(default=4.0)

    def __str__(self):
        return self.title
'''
with open('books/models.py', 'w', encoding='utf-8') as f:
    f.write(models_code.strip())
print("2/5: models.py configured!")

# 3. Create books/serializers.py
serializers_code = '''
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
'''
with open('books/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_code.strip())
print("3/5: serializers.py configured!")

# 4. Create books/views.py & books/urls.py
views_code = '''
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
'''
with open('books/views.py', 'w', encoding='utf-8') as f:
    f.write(views_code.strip())

books_urls_code = '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
'''
with open('books/urls.py', 'w', encoding='utf-8') as f:
    f.write(books_urls_code.strip())

# 5. Update library_backend/urls.py
main_urls_code = '''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
]
'''
with open('library_backend/urls.py', 'w', encoding='utf-8') as f:
    f.write(main_urls_code.strip())
print("4/5: Views & REST API URLs configured!")

# 6. Database Migrations
os.system(f'{sys.executable} manage.py makemigrations books')
os.system(f'{sys.executable} manage.py migrate')

# 7. Seed 78 Books Data into SQLite Database
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()
from books.models import Book

if Book.objects.count() == 0:
    books_data = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "description": "A legendary fantasy adventure about Bilbo Baggins.", "rating": 4.8},
        {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "description": "An orphan boy discovers he is a wizard.", "rating": 4.9},
        {"title": "A Game of Thrones", "author": "George R.R. Martin", "genre": "Fantasy", "description": "Several noble families fight for the Iron Throne.", "rating": 4.7},
        {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "description": "Set on the desert planet Arrakis.", "rating": 4.7},
        {"title": "The Martian", "author": "Andy Weir", "genre": "Sci-Fi", "description": "An astronaut is stranded alone on Mars.", "rating": 4.8},
        {"title": "Project Hail Mary", "author": "Andy Weir", "genre": "Sci-Fi", "description": "A lone astronaut solves an extinction threat.", "rating": 4.9},
        {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "Mystery", "description": "Decoding symbols hidden in Leonardo da Vinci paintings.", "rating": 4.6},
        {"title": "Gone Girl", "author": "Gillian Flynn", "genre": "Thriller", "description": "A husband becomes suspect in his wife disappearance.", "rating": 4.5},
        {"title": "The Silent Patient", "author": "Alex Michaelides", "genre": "Thriller", "description": "A painter shoots her husband and never speaks.", "rating": 4.6},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "description": "Classic romance of Elizabeth Bennet and Darcy.", "rating": 4.8},
        {"title": "Atomic Habits", "author": "James Clear", "genre": "Self-Help", "description": "Tiny changes, remarkable results.", "rating": 4.9},
        {"title": "The Psychology of Money", "author": "Morgan Housel", "genre": "Finance", "description": "Strange ways people think about wealth.", "rating": 4.8},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classics", "description": "Tragic story of Jay Gatsby in the roaring twenties.", "rating": 4.4},
        {"title": "1984", "author": "George Orwell", "genre": "Classics", "description": "Totalitarian regime ruled by Big Brother.", "rating": 4.8}
    ]
    for b in books_data:
        Book.objects.create(**b)
    print(f"5/5: Sample Books added to SQLite DB successfully! Total books: {Book.objects.count()}")
else:
    print("Database already has data!")

print("\\nALL BACKEND SETUP COMPLETED SUCCESSFULLY!")