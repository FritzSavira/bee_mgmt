from flask import Flask, request, session, redirect, url_for
from flask_babel import Babel, _

babel = Babel()

import os

class Config:
    LANGUAGES = ['de', 'en', 'es', 'cs']
    SECRET_KEY = 'your_secret_key' # This should be a strong, random key in a real application
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'translations')

def get_locale():
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(Config.LANGUAGES)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    babel.init_app(app, locale_selector=get_locale)
    app.jinja_env.add_extension('jinja2.ext.i18n')

    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang in app.config['LANGUAGES']:
            session['lang'] = lang
        return redirect(request.referrer or url_for('main.index'))

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
