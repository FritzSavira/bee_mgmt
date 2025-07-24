from flask import Flask, request, session, redirect, url_for, current_app
from flask_babel import Babel, _
from app.config import Config # Import the correct Config class

babel = Babel()

import os

def get_locale():
    print(f"DEBUG: get_locale() called. Current session lang: {session.get('lang')}")
    print(f"DEBUG: get_locale() called. Request accept languages: {request.accept_languages.best_match(current_app.config['LANGUAGES'])}")
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    babel.init_app(app, locale_selector=get_locale)
    app.jinja_env.add_extension('jinja2.ext.i18n')

    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang in app.config['LANGUAGES']:
            session['lang'] = lang
            print(f"DEBUG: set_language() called. Session lang set to: {session['lang']}")
        else:
            print(f"DEBUG: set_language() called. Invalid language: {lang}")
        return redirect(request.referrer or url_for('main.index'))

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app