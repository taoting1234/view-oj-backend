from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Category(Base):
    __tablename__ = 'category'

    fields = ['id', 'name', 'series']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10000), nullable=False)

    @property
    def series(self):
        from app.models.problem_set.series import Series
        return Series.search(category_id=self.id, page_size=-1)['data']
