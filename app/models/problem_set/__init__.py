from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.problem_set.series import Series


class ProblemSet(Base):
    __tablename__ = 'problem_set'

    fields = ['id', 'name', 'series_id']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    series_id = Column(Integer, ForeignKey(Series.id))

    @property
    def problem_list(self):
        from app.models.problem import Problem
        from app.models.problem_set.problem_relationship import ProblemRelationship
        r = list()
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            p = Problem.get_by_id(i.problem_id)
            p.difficulty = i.difficulty
            fields = Problem.fields.copy()
            fields.append('difficulty')
            p.fields = fields
            r.append(p)
        return r

    @property
    def user_list(self):
        from app.models.user import User
        from app.models.problem_set.user_relationship import UserRelationship
        r = []
        for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            user = User.get_by_id(i.username)
            r.append(user)
        return r

    @property
    def detail(self):
        from app.models.base import db
        from app.models.accept_problem import AcceptProblem
        from app.models.user import User
        user_list = self.user_list
        query_res = db.session.query(User, AcceptProblem). \
            filter(User.username.in_([i.username for i in user_list])). \
            filter(AcceptProblem.username == User.username). \
            filter(AcceptProblem.problem_id.in_([i.id for i in self.problem_list])).all()
        res = {}
        for user in user_list:
            res.setdefault(user, [])
        for user, acp in query_res:
            res[user].append(acp)
        res = [{'user': i[0], 'data': i[1]} for i in res.items()]
        return res

    @classmethod
    def create(cls, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_set.problem_relationship import ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        problem_set = super().create(**kwargs)
        for i in kwargs.get('problem_list', []):
            oj_name, problem_pid = i['problem'].split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=problem_set.id, difficulty=i['difficulty'])
        for i in kwargs['user_list']:
            UserRelationship.create(problem_set_id=problem_set.id, username=i)

    def modify(self, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_set.problem_relationship import ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        super().modify(**kwargs)
        if kwargs.get('problem_list', None):
            for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
                i.delete()
            for i in kwargs['problem_list']:
                oj_name, problem_pid = i['problem'].split('-', 1)
                oj = OJ.get_by_name(oj_name)
                problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
                ProblemRelationship.create(problem_id=problem.id, problem_set_id=self.id, difficulty=i['difficulty'])
        if kwargs.get('user_list', None):
            for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
                i.delete()
            for i in kwargs['user_list']:
                UserRelationship.create(problem_set_id=self.id, username=i)

    def delete(self):
        from app.models.problem_set.problem_relationship import ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        super().delete()
