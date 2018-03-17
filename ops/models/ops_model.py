# --*-- coding: utf-8 --*--

from ops import db


class SecurityField(db.Model):
    __tablename__ = 'ops_security_field'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.String(250), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)

    def __init__(self, field_name, field_type):
        self.field_name = field_name
        self.field_type = field_type

    def _to_dict(self):
        return {col.name: getattr(self, col.name, None) for col in self.__table__.cloumns}

    def _to_tuple(self):
        return self.field_type, self.field_name


class SecurityExpert(db.Model):
    __tablename__ = 'ops_security_export'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    resume = db.Column(db.Text, nullable=False)

    def __init__(self, name, phone, email, resume):
        self.name = name
        self.phone = phone
        self.email = email
        self.resume = resume


ops_export_field_rela = db.Table('ops_export_field_rela',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('export_id', db.Integer, db.ForeignKey('ops_security_export.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('ops_security_field.id')),
)


class SecuritySolution(db.Model):
    __tablename__ = 'ops_security_solution'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    solution_info = db.Column(db.Text, nullable=False)
    describe = db.Column(db.Text, nullable=True)
    solution_files = db.relationship('SolutionFiles', backref='solution')

    def __int__(self, solution_info, describe=None):
        self.solution_info = solution_info
        self.describe = describe


class SolutionFiles(db.Model):
    __tablename__ = 'ops_solution_files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('ops_security_solution.id'))
    file_name = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.Text, nullable=True)

    def __init__(self, file_name, solution_id, file_url=None):
        self.file_name = file_name
        self.solution_id = solution_id
        self.file_url = file_url
