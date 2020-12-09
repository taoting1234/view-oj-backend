from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base
from app.models.problem_set.category import Category


class Series(Base):
    __tablename__ = 'series'

    fields = ['id', 'name', 'problem_sets']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10000), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))

    @property
    def problem_sets(self):
        from app.models.problem_set import ProblemSet
        return ProblemSet.search(series_id=self.id, page_size=-1)['data']
