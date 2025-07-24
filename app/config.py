import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eine-geheime-zeichenkette'
    LANGUAGES = ['de', 'en', 'es', 'cs']
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
