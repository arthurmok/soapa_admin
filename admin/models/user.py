# -*- coding: utf-8 -*-
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from admin import db, login_manager, logger
from config import SECRET_KEY, SESSION_LIFETIME


class User(UserMixin, db.Model):
    __tablename__ = 'user_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    cname = db.Column(db.String(50))
    email = db.Column(db.String(200))
    mobile = db.Column(db.String(50))
    department = db.Column(db.String(200))
    # company = db.Column(db.String(200))
    # rid = db.Column(db.Integer)
    group_ids = db.Column(db.String(250))
    password = db.Column(db.String(100))
    scan_key = db.Column(db.String(100))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Boolean, default=True)

    def __init__(self, name, cname=None, email=None, mobile=None, department=None,
                 group_ids=None, password=None, scan_key=None, status=None):
        self.name = name
        self.cname = cname
        self.email = email
        self.mobile = mobile
        self.department = department
        # self.company = company
        # self.rid = rid
        self.group_ids = group_ids
        self.password = password
        self.scan_key = scan_key
        self.status = status

    def _to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    cname=self.cname,
                    email=self.email,
                    mobile=self.mobile,
                    department=self.department,
                    group_ids=self.group_ids,
                    status=self.status
                    )

    @staticmethod
    def _from_dict(user_dict):
        return User(name=user_dict.get('name'),
                    cname=user_dict.get('cname'),
                    email=user_dict.get('email'),
                    mobile=user_dict.get('mobile'),
                    department=user_dict.get('department'),
                    group_ids=user_dict.get('group_ids'),
                    status=user_dict.get('status')
                    )

    def gen_password_hash(self, password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def gen_auth_token(self):
        s = Serializer(SECRET_KEY, expires_in=SESSION_LIFETIME)
        return s.dumps({'name': self.name})

    def generate_auth_uuid(self):
        token = self.gen_auth_token()
        s_uuid = uuid.uuid1()
        l_uuid = str(s_uuid).split('-')
        s_uuid = ''.join(l_uuid)
        tokenMapping = TokenMapping(
            uuid=s_uuid,
            token=token,
        )
        db.session.add(tokenMapping)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(e)

        return s_uuid


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


class Role(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    cname = db.Column(db.String(30))

    def __init__(self, role_id, name, cname=None):
        self.id = role_id
        self.name = name
        self.cname = cname

    @staticmethod
    def _get_name(role_id):
        role = db.session.query(Role).filter(Role.id == role_id).first()
        return role.cname


class Group(db.Model):
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    cname = db.Column(db.String(100))
    selectors = db.Column(db.Text)

    def __init__(self, name, cname=None, selectors=None):
        self.name = name
        self.cname = cname
        self.selectors = selectors

    def _to_dict(self):
        return {col.name: getattr(self, col.name, None) for col in self.__table__.columns}

    @staticmethod
    def _from_dict(group_dict):
        return Group(
            name=group_dict.get('name'),
            cname=group_dict.get('cname'),
            selectors=group_dict.get('selectors')
        )


class Selector(db.Model):
    __tablename__ = 'user_selector'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    cname = db.Column(db.String(50))
    kind = db.Column(db.String(50))

    def __init__(self, name, cname, kind):
        self.name = name
        self.cname = cname
        self.kind = kind

    def _to_dict(self):
        return {col.name: getattr(self, col.name, None) for col in self.__table__.columns}

    @staticmethod
    def _from_dict(selector_dict):
        return Selector(name=selector_dict.get('name'),
                        cname=selector_dict.get('cname'),
                        kind=selector_dict.get('kind')
                        )


class TokenMapping(db.Model):
    __tablename__ = "user_token_mapping"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = db.Column(db.String(40), nullable=False)
    token = db.Column(db.String(250), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, uuid, token):
        self.uuid = uuid
        self.token = token
