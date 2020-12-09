import json
import re

from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.validators.base import BaseForm


class CreateProblemSetForm(BaseForm):
    name = StringField(validators=[DataRequired(message='Problem set name cannot be empty')])
    problem_list = StringField(validators=[DataRequired(message='Problem list cannot be empty')])
    user_list = StringField(validators=[DataRequired(message='User list cannot be empty')])
    category_id = IntegerField(validators=[DataRequired(message='category_id cannot be empty')])

    def validate_problem_list(self, value):
        try:
            self.problem_list.data = json.loads(self.problem_list.data)
            if not isinstance(self.problem_list.data, list):
                raise Exception()
        except Exception:
            raise ValidationError('Problem list must be list')
        for i in self.problem_list.data:
            if re.match('[a-z_]+-.+', i['problem']) is None:
                raise ValidationError('Problem format error')

    def validate_user_list(self, value):
        from app.models.user import User
        try:
            self.user_list.data = json.loads(self.user_list.data)
            if not isinstance(self.user_list.data, list):
                raise Exception()
        except Exception:
            raise ValidationError('User list must be list')
        for username in self.user_list.data:
            if User.get_by_id(username) is None:
                raise ValidationError(f'User {username} not found')


class ModifyProblemSetForm(BaseForm):
    name = StringField()
    problem_list = StringField()

    def validate_problem_list(self, value):
        if self.problem_list.data:
            try:
                self.problem_list.data = json.loads(self.problem_list.data)
                if not isinstance(self.problem_list.data, list):
                    raise Exception()
            except Exception:
                raise ValidationError('Problem list must be list')
            for i in self.problem_list.data:
                if re.match('[a-z_]+-.+', i['problem']) is None:
                    raise ValidationError('Problem format error')


class CreateContestForm(BaseForm):
    name = StringField(validators=[DataRequired(message='Problem set name cannot be empty')])
    contest_oj_id = IntegerField(validators=[DataRequired(message='contest_oj_id cannot be empty')])
    contest_id = StringField(validators=[DataRequired(message='ContestID cannot be empty')])
    user_list = StringField(validators=[DataRequired(message='User list cannot be empty')])
    category_id = IntegerField(validators=[DataRequired(message='category_id cannot be empty')])

    def validate_contest_oj_id(self, value):
        from app.models.oj import OJ
        try:
            self.contest_oj_id.data = int(self.contest_oj_id.data)
        except:
            raise ValidationError('Contest_oj_id must be integer')
        oj = OJ.get_by_id(self.contest_oj_id.data)
        if oj is None:
            raise ValidationError(f'Cannot find OJ:{self.contest_oj_id.data}')
        if not oj.contest_valid:
            raise ValidationError(f'OJ: {self.contest_oj_id.data} is not valid for contest')

    def validate_user_list(self, value):
        from app.models.user import User
        try:
            self.user_list.data = json.loads(self.user_list.data)
            if not isinstance(self.user_list.data, list):
                raise Exception()
        except Exception:
            raise ValidationError('User list must be list')
        for username in self.user_list.data:
            if User.get_by_id(username) is None:
                raise ValidationError(f'User {username} not found')
