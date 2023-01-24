import datetime
from collections.abc import Callable, Iterable, Sequence
from typing import Any, overload
from uuid import UUID

from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models.base import Model
from django.db.models.deletion import Collector
from django.db.models.fields import Field, reverse_related
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.forms.formsets import BaseFormSet
from django.http.request import HttpRequest
from django.utils.datastructures import _IndexableCollection
from typing_extensions import Literal, TypedDict

class FieldIsAForeignKeyColumnName(Exception): ...

def lookup_needs_distinct(opts: Options, lookup_path: str) -> bool: ...
def prepare_lookup_value(key: str, value: datetime.datetime | str) -> bool | datetime.datetime | str: ...
def quote(s: int | str | UUID) -> str: ...
def unquote(s: str) -> str: ...
def flatten(fields: Any) -> list[Callable[..., Any] | str]: ...
def flatten_fieldsets(fieldsets: Any) -> list[Callable[..., Any] | str]: ...
def get_deleted_objects(
    objs: Sequence[Model | None] | QuerySet[Model], request: HttpRequest, admin_site: AdminSite
) -> tuple[list[Model], dict[str, int], set[str], list[str]]: ...

class NestedObjects(Collector):
    data: dict[str, Any]
    dependencies: dict[Any, Any]
    fast_deletes: list[Any]
    field_updates: dict[Any, Any]
    using: str
    edges: Any
    protected: Any
    model_objs: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def add_edge(self, source: Model | None, target: Model) -> None: ...
    def related_objects(
        self, related_model: type[Model], related_fields: Iterable[Field[Any, Any]], objs: _IndexableCollection[Model]
    ) -> QuerySet[Model]: ...
    def nested(self, format_callback: Callable[..., Any] = ...) -> list[Any]: ...
    def can_fast_delete(self, *args: Any, **kwargs: Any) -> bool: ...

class _ModelFormatDict(TypedDict):
    verbose_name: str
    verbose_name_plural: str

def model_format_dict(obj: Model | type[Model] | QuerySet[Model] | Options[Model]) -> _ModelFormatDict: ...
def model_ngettext(obj: Options | QuerySet[Model], n: int | None = ...) -> str: ...
def lookup_field(
    name: Callable[..., Any] | str, obj: Model, model_admin: BaseModelAdmin | None = ...
) -> tuple[Field[Any, Any] | None, str | None, Any]: ...
@overload
def label_for_field(  # type: ignore
    name: Callable[..., Any] | str,
    model: type[Model],
    model_admin: BaseModelAdmin | None = ...,
    return_attr: Literal[True] = ...,
    form: BaseForm | None = ...,
) -> tuple[str, Callable[..., Any] | str | None]: ...
@overload
def label_for_field(
    name: Callable[..., Any] | str,
    model: type[Model],
    model_admin: BaseModelAdmin | None = ...,
    return_attr: Literal[False] = ...,
    form: BaseForm | None = ...,
) -> str: ...
def help_text_for_field(name: str, model: type[Model]) -> str: ...
def display_for_field(value: Any, field: Field[Any, Any], empty_value_display: str) -> str: ...
def display_for_value(value: Any, empty_value_display: str, boolean: bool = ...) -> str: ...

class NotRelationField(Exception): ...

def get_model_from_relation(field: Field[Any, Any] | reverse_related.ForeignObjectRel) -> type[Model]: ...
def reverse_field_path(model: type[Model], path: str) -> tuple[type[Model], str]: ...
def get_fields_from_path(model: type[Model], path: str) -> list[Field[Any, Any]]: ...
def construct_change_message(
    form: AdminPasswordChangeForm, formsets: Iterable[BaseFormSet], add: bool
) -> list[dict[str, dict[str, list[str]]]]: ...
