import abc

from mongoengine import Document, DoesNotExist, MultipleObjectsReturned, QuerySet

from domain.exceptions.exceptions import AlreadyCreatedError

"""
Repository module

For design pattern of this application, I followed a Repository Patter.
This allows to a simplifying abstraction over data storage, allowing us 
to decouple our model layer from the data layer. 

We present an abstract repository class and a repository model class,
from which specific repositories for different models will be inherited.

In this Base Class we define the common methods that will interact with
out database, for all repositories within the application.

"""


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_attr(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, *args, **kwargs):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    def __init__(self, model: Document):
        self.model: Document = model

    def get_by_attr(self, **kwargs) -> QuerySet:
        try:
            return self.model.objects.get(**kwargs)
        except DoesNotExist:
            return None
        except MultipleObjectsReturned as e:
            raise AlreadyCreatedError(str(e))

    def get_all(self) -> QuerySet:
        return self.model.objects

    def _persist(self, obj: Document) -> Document:
        return obj.save()

    def create(self, **kwargs):
        obj: Document = self.model(**kwargs)
        obj.save()

    def save(self, obj: Document) -> Document:
        self._persist(obj)
        return obj.refresh_from_db()

    def delete(self, obj: Document) -> Document:
        return obj.delete()
