# --*-- coding: utf-8 --*--

from ops import db


class SecurityFieldType(db.Model):
    __tablename__ = 'ops_security_field_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(250), nullable=False)
    fields = db.relationship('SecurityField', backref='field_type')

    def __init__(self, type_name):
        self.type_name = type_name

    def _to_dict(self):
        return {
            "id": self.id,
            "type_name": self.type_name,
            "fields": [ field._to_dict_for_type() for field in self.fields]
        }


ops_expert_field_rela = db.Table('ops_expert_field_rela',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('expert_id', db.Integer, db.ForeignKey('ops_security_expert.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('ops_security_field.id')),
)


class SecurityField(db.Model):
    __tablename__ = 'ops_security_field'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.String(250), nullable=False)
    field_type_id = db.Column(db.Integer, db.ForeignKey('ops_security_field_type.id'))

    def __init__(self, field_name, field_type_id):
        self.field_name = field_name
        self.field_type_id = field_type_id

    def _to_dict(self):
        return {
            "id": self.id,
            "field_name": self.field_name,
            "field_type": {"id": self.field_type.id, "type_name": self.field_type.type_name}
            }

    def _to_dict_for_type(self):
        return {
            "id": self.id,
            "field_name": self.field_name
        }


class SecurityExpert(db.Model):
    __tablename__ = 'ops_security_expert'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    resume = db.Column(db.Text, nullable=False)
    fields = db.relationship('SecurityField', secondary=ops_expert_field_rela,
                            backref=db.backref('experts', lazy='dynamic'),
                            lazy='dynamic')

    def __init__(self, name, phone, email, resume):
        self.name = name
        self.phone = phone
        self.email = email
        self.resume = resume

    def _to_dict(self):
        expert_dict = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'resume': self.resume,
            'fields': [expert_field._to_dict_for_type() for expert_field in self.fields]
        }
        return expert_dict


class SecurityExpertRuleRela(db.Model):
    __tablename__ = 'ops_expert_rule_rela'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expert_id = db.Column(db.Integer, nullable=False)
    rule_id = db.Column(db.Integer, nullable=False)

    def __init__(self, expert_id, rule_id):
        self.expert_id = expert_id
        self.rule_id = rule_id


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
