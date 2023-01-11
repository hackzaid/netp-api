import sentry_sdk
from flask import Flask, redirect, url_for, request, g
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from apifairy import APIFairy

from configs.config import BaseConfig, ProdConfig
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_authorize import Authorize
from flask_login import current_user


def my_current_user(user):
    return g.user


db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()

authorize = Authorize(current_user=my_current_user)


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # extensions
    from api import models

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    if app.config['USE_CORS']:  # pragma: no branch
        cors.init_app(app)
    mail.init_app(app)
    apifairy.init_app(app)
    authorize.init_app(app)

    # blueprints
    from api.errors import errors
    from api.tokens import tokens
    from api.views.administration.adminViews import users

    from api.views.members.memberViews import members
    from api.views.products.productViews import product
    from api.views.inspection.inspectionViews import inspection

    app.register_blueprint(errors)
    app.register_blueprint(tokens, url_prefix='/api')
    app.register_blueprint(users, url_prefix='/api')

    app.register_blueprint(members, url_prefix='/api')
    app.register_blueprint(product, url_prefix='/api')
    app.register_blueprint(inspection, url_prefix='/api')

    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))

    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    sentry_sdk.init(
        dsn="https://c19fa798951c45d08f0f870aa26094a7@o4504089491537920.ingest.sentry.io/4504297885597696",
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
    )

    return app
