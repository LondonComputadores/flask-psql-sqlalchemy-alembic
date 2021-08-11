from flask import Flask, redirect
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_migrate import Migrate
from app.database.db import db
from app.database.ma import ma
from flask_login import LoginManager, current_user
login_manager = LoginManager()
import logging
import logging.config


from app.models.user import UserModel
from app.routes.user import UserLogin, UserLogout, UserList, ListUserById, MyProfile, CreateUser

from app.routes.organization import ListOrganizations, ListOrganizationById
from app.models.organization import OrganizationModel

from app.routes.acts import ListActs, Act
from app.models.act import ActModel

from app.routes.audits import ListAudits, ListAuditById, FinalizeAuditById
from app.models.audit import AuditModel

from app.routes.sites import ListSites, SiteById

from app.routes.incidents import ListIncidents, IncidentById, CreateIncident
from app.routes.answers import ListAnswersById

from app.routes.statistics import Stats

from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, supports_credentials=True)
api = Api(app)
ma.init_app(app)


login_manager.init_app(app)

#   Load environment specific settings
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

api = swagger.docs(Api(app), apiVersion='0.1', description = "CMMC API")

migrate = Migrate(app, db)
db.init_app(app)

# API Routes
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogout, "/api/logout")

api.add_resource(MyProfile, '/api/my-profile')

#ACTS
api.add_resource(ListActs, "/api/acts")
api.add_resource(Act, "/api/acts/<int:_id>")

#ORGANIZATIONS
api.add_resource(ListOrganizations, "/api/organizations")
api.add_resource(ListOrganizationById, "/api/organizations/<int:_id>")

#AUDITS
api.add_resource(ListAudits, "/api/audits")
api.add_resource(ListAuditById, "/api/audit/<int:_id>")
api.add_resource(FinalizeAuditById, "/api/audit/finalize/<int:_id>")

#USERS
api.add_resource(UserList, "/api/users")
api.add_resource(ListUserById, "/api/user/<int:_id>")
api.add_resource(CreateUser,  "/api/user")

#SITES
api.add_resource(ListSites, "/api/sites")
api.add_resource(SiteById, "/api/site/<int:_id>")

#INCIDENTS
api.add_resource(ListIncidents, "/api/incidents")
api.add_resource(IncidentById, "/api/incident/<int:_id>")
api.add_resource(CreateIncident, "/api/incident")

#ANSWERS
api.add_resource(ListAnswersById, "/api/answer/<int:_id>")

#STATISTICS
api.add_resource(Stats, "/api/stats/all")


@login_manager.user_loader
def get_user(user_id):
    return UserModel.find_by_id(int(user_id))

@login_manager.unauthorized_handler
def unauth_handler():
    return {'message': "Session has expired"}, 401


# Swagger documentation
@app.route('/docs')
def getIndexPage():
    return redirect("/api/spec.html#!/spec", code=302)
