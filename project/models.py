from datetime import datetime
from uuid import uuid4

from websauna.system.model.columns import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from project import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Wedding(db.Model):
    __tablename__ = 'weddings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wife = db.Column(db.String, nullable=False)
    husband = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4)

    def __init__(self, wife: str, husband: str, city: str, date: db.Date):
        self.wife = wife
        self.husband = husband
        self.city = city
        self.date = date

    def __repr__(self):
        return f'<Wedding: {self.id}, {self.wife}, {self.husband}, {self.city}, {self.date}>'

    def get_id(self):
        return str(self.id)

    def get_wife(self):
        return str(self.wife)

    def get_husband(self):
        return str(self.husband)

    def get_city(self):
        return str(self.city)

    def get_uuid(self):
        return str(self.uuid)

    def get_date(self):
        return str(self.date.strftime('%d.%m.%Y'))


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String, nullable=False)
    wedding_id = db.Column(db.Integer, db.ForeignKey(Wedding.id))
    guest_name = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    wedding = db.relationship('Wedding', foreign_keys='File.wedding_id')

    def __init__(self, path: str, wedding_id: int, guest_name: str):
        self.path = secure_filename(path)
        self.wedding_id = wedding_id
        self.guest_name = guest_name
        self.created_on = datetime.now()

    def __repr__(self):
        return f'<File: {self.path}>'

    def get_id(self):
        return str(self.id)

    def get_path(self):
        return str(self.path)

    def get_guest_name(self):
        return str(self.guest_name)

    def get_wedding_id(self):
        return str(self.wedding_id)


class UserWedding(db.Model):
    __tablename__ = 'users_weddings'

    wedding_id = db.Column(db.Integer, db.ForeignKey(Wedding.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    wedding = db.relationship('Wedding', foreign_keys='UserWedding.wedding_id')
    user = db.relationship('User', foreign_keys='UserWedding.user_id')

    def __init__(self, wedding_id: int, user_id: int):
        self.wedding_id = wedding_id
        self.user_id = user_id

    def __repr__(self):
        return f'<User_Wedding: {self.wedding_id}, {self.user_id}>'

    def get_wedding_id(self):
        return str(self.wedding_id)

    def get_user_id(self):
        return str(self.user_id)
