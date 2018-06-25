from app import db
from app import lm

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Modules(db.Model):
    __tablename__ = "modules"
    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(64))
    module_title = db.Column(db.String(128))
    department = db.Column(db.String(64))
    module_description = db.Column(db.String(128))
    module_credit = db.Column(db.String(64))
    workload = db.Column(db.String(128))
    preclusion = db.Column(db.String(128))
    types = db.Column(db.String(128))
    #did not import history data for now
    history = db.Column(db.String(128))
    corequisite = db.Column(db.String(128))
    prerequisite =db.Column(db.String(128))

    def __repr__(self):
        return '<Module code {}, module title {}>'.format(self.module_code, self.module_title)

class Mapping(db.Model):
    __tablename__ = "mapping"
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(64))
    partner_uni = db.Column(db.String(128))
    #Main partner uni modules
    partner_uni_module_1 = db.Column(db.String(64))
    partner_uni_module_1_title = db.Column(db.String(128))
    partner_uni_module_1_credits = db.Column(db.String(64))
    #Second Partner Uni modules mappable
    partner_uni_module_2 = db.Column(db.String(64))
    partner_uni_module_2_title = db.Column(db.String(128))
    partner_uni_module_2_credits = db.Column(db.String(64))
    #Partner uni location
    partner_uni_country = db.Column(db.String(64))
    partner_uni_state = db.Column(db.String(64))
    partner_uni_continent= db.Column(db.String(64))
    #Partner uni images
    partner_uni_image = db.Column(db.String(64))
    #Main NUS modules
    nus_module_1 = db.Column(db.String(64))
    nus_module_1_title = db.Column(db.String(128))
    nus_module_1_credits = db.Column(db.String(64))
    #Second NUS modules mappable
    nus_module_2 = db.Column(db.String(64))
    nus_module_2_title = db.Column(db.String(128))
    nus_module_2_credits = db.Column(db.String(64))

    def __repr(self):
        return '<Partner uni {} - Module {}; NUS faculty {} - Module {}>'.format(self.partner_uni, self.partner_uni_module_1, self.faculty, self.nus_module_1)
