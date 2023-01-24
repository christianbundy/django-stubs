from collections.abc import Callable
from typing import Any, Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField, RelatedField
from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel, OneToOneRel
from django.db.models.manager import RelatedManager
from django.db.models.query import QuerySet
from django.db.models.query_utils import DeferredAttribute

_T = TypeVar("_T")

class ForeignKeyDeferredAttribute(DeferredAttribute):
    field: RelatedField

class ForwardManyToOneDescriptor:
    field: ForeignKey
    def __init__(self, field_with_rel: ForeignKey) -> None: ...
    @property
    def RelatedObjectDoesNotExist(self) -> type[ObjectDoesNotExist]: ...
    def is_cached(self, instance: Model) -> bool: ...
    def get_queryset(self, **hints: Any) -> QuerySet: ...
    def get_prefetch_queryset(
        self, instances: list[Model], queryset: QuerySet | None = ...
    ) -> tuple[QuerySet, Callable[..., Any], Callable[..., Any], bool, str, bool]: ...
    def get_object(self, instance: Model) -> Model: ...
    def __get__(
        self, instance: Model | None, cls: type[Model] | None = ...
    ) -> Model | ForwardManyToOneDescriptor | None: ...
    def __set__(self, instance: Model, value: Model | None) -> None: ...
    def __reduce__(self) -> tuple[Callable[..., Any], tuple[type[Model], str]]: ...

class ForwardOneToOneDescriptor(ForwardManyToOneDescriptor):
    field: OneToOneField
    def get_object(self, instance: Model) -> Model: ...

class ReverseOneToOneDescriptor:
    related: OneToOneRel
    def __init__(self, related: OneToOneRel) -> None: ...
    @property
    def RelatedObjectDoesNotExist(self) -> type[ObjectDoesNotExist]: ...
    def is_cached(self, instance: Model) -> bool: ...
    def get_queryset(self, **hints: Any) -> QuerySet: ...
    def get_prefetch_queryset(
        self, instances: list[Model], queryset: QuerySet | None = ...
    ) -> tuple[QuerySet, Callable[..., Any], Callable[..., Any], bool, str, bool]: ...
    def __get__(self, instance: Model | None, cls: type[Model] | None = ...) -> Model | ReverseOneToOneDescriptor: ...
    def __set__(self, instance: Model, value: Model | None) -> None: ...
    def __reduce__(self) -> tuple[Callable[..., Any], tuple[type[Model], str]]: ...

class ReverseManyToOneDescriptor:
    rel: ManyToOneRel
    field: ForeignKey
    def __init__(self, rel: ManyToOneRel) -> None: ...
    @property
    def related_manager_cls(self) -> type[RelatedManager]: ...
    def __get__(self, instance: Model | None, cls: type[Model] | None = ...) -> ReverseManyToOneDescriptor: ...
    def __set__(self, instance: Model, value: list[Model]) -> Any: ...

def create_reverse_many_to_one_manager(superclass: type, rel: Any) -> type[RelatedManager]: ...

class ManyToManyDescriptor(ReverseManyToOneDescriptor):
    field: ManyToManyField  # type: ignore[assignment]
    rel: ManyToManyRel  # type: ignore[assignment]
    reverse: bool
    def __init__(self, rel: ManyToManyRel, reverse: bool = ...) -> None: ...
    @property
    def through(self) -> type[Model]: ...
    @property
    def related_manager_cls(self) -> type[Any]: ...  # ManyRelatedManager

# fake
class _ForwardManyToManyManager(Generic[_T]):
    def all(self) -> QuerySet: ...

def create_forward_many_to_many_manager(superclass: type, rel: Any, reverse: Any) -> _ForwardManyToManyManager: ...
