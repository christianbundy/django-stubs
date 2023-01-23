from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Generic, Optional, TypeVar, Union  # noqa: Y037  # https://github.com/python/mypy/issues/12211

from django import forms
from django.contrib.admin.filters import FieldListFilter, ListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.core.checks.messages import CheckMessage
from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey, ManyToManyField, RelatedField
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.forms.fields import Field as FormField
from django.forms.fields import TypedChoiceField
from django.forms.formsets import BaseFormSet
from django.forms.models import (
    BaseInlineFormSet,
    BaseModelFormSet,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.widgets import Media
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.template.response import _TemplateForResponseT
from django.urls.resolvers import URLPattern
from django.utils.datastructures import _ListOrTuple
from django.utils.functional import _StrOrPromise
from django.utils.safestring import SafeString
from typing_extensions import Literal, TypeAlias, TypedDict

IS_POPUP_VAR: str
TO_FIELD_VAR: str
HORIZONTAL: Literal[1]
VERTICAL: Literal[2]

_Direction: TypeAlias = Literal[1, 2]

def get_content_type_for_model(obj: type[Model] | Model) -> ContentType: ...
def get_ul_class(radio_style: int) -> str: ...

class IncorrectLookupParameters(Exception): ...

FORMFIELD_FOR_DBFIELD_DEFAULTS: Any
csrf_protect_m: Any

_FieldGroups: TypeAlias = Sequence[str | Sequence[str]]

class _OptionalFieldOpts(TypedDict, total=False):
    classes: Sequence[str]
    description: _StrOrPromise

class _FieldOpts(_OptionalFieldOpts, total=True):
    fields: _FieldGroups

# Workaround for mypy issue, a Sequence type should be preferred here.
# https://github.com/python/mypy/issues/8921
# _FieldsetSpec = Sequence[Tuple[Optional[str], _FieldOpts]]
_FieldsetSpec: TypeAlias = _ListOrTuple[tuple[_StrOrPromise | None, _FieldOpts]]
# https://github.com/python/mypy/issues/12211
_ListFilterT: TypeAlias = Union[
    type[ListFilter],
    Field,
    str,
    tuple[Field | str, type[FieldListFilter]],
    list[Field | str | type[FieldListFilter]],
]

# Generic type specifically for models, for use in BaseModelAdmin and subclasses
# https://github.com/typeddjango/django-stubs/issues/482
_ModelT = TypeVar("_ModelT", bound=Model)

class BaseModelAdmin(Generic[_ModelT]):
    autocomplete_fields: Sequence[str]
    raw_id_fields: Sequence[str]
    fields: _FieldGroups | None
    exclude: Sequence[str] | None
    fieldsets: Optional[_FieldsetSpec]
    form: type[forms.ModelForm[_ModelT]]
    filter_vertical: Sequence[str]
    filter_horizontal: Sequence[str]
    radio_fields: Mapping[str, _Direction]
    prepopulated_fields: dict[str, Sequence[str]]
    formfield_overrides: Mapping[type[Field], Mapping[str, Any]]
    readonly_fields: Sequence[str]
    ordering: Sequence[str] | None
    sortable_by: _ListOrTuple[str] | None
    view_on_site: bool | Callable[[_ModelT], str]
    show_full_result_count: bool
    checks_class: Any
    model: type[_ModelT]
    opts: Options[_ModelT]
    admin_site: AdminSite
    def __init__(self) -> None: ...
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    def formfield_for_dbfield(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> FormField | None: ...
    def formfield_for_choice_field(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> TypedChoiceField: ...
    def get_field_queryset(self, db: str | None, db_field: RelatedField, request: HttpRequest) -> QuerySet | None: ...
    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField: ...
    def formfield_for_manytomany(
        self, db_field: ManyToManyField, request: HttpRequest, **kwargs: Any
    ) -> ModelMultipleChoiceField | None: ...
    def get_autocomplete_fields(self, request: HttpRequest) -> Sequence[str]: ...
    def get_view_on_site_url(self, obj: _ModelT | None = ...) -> str | None: ...
    def get_empty_value_display(self) -> SafeString: ...
    def get_exclude(self, request: HttpRequest, obj: _ModelT | None = ...) -> Sequence[str] | None: ...
    def get_fields(self, request: HttpRequest, obj: _ModelT | None = ...) -> _FieldGroups: ...
    def get_fieldsets(self, request: HttpRequest, obj: _ModelT | None = ...) -> _FieldsetSpec: ...
    def get_inlines(self, request: HttpRequest, obj: _ModelT | None) -> list[type[InlineModelAdmin]]: ...
    def get_ordering(self, request: HttpRequest) -> Sequence[str]: ...
    def get_readonly_fields(self, request: HttpRequest, obj: _ModelT | None = ...) -> Sequence[str]: ...
    def get_prepopulated_fields(self, request: HttpRequest, obj: _ModelT | None = ...) -> dict[str, Sequence[str]]: ...
    def get_queryset(self, request: HttpRequest) -> QuerySet[_ModelT]: ...
    def get_sortable_by(self, request: HttpRequest) -> Sequence[str]: ...
    def lookup_allowed(self, lookup: str, value: str) -> bool: ...
    def to_field_allowed(self, request: HttpRequest, to_field: str) -> bool: ...
    def has_add_permission(self, request: HttpRequest) -> bool: ...
    def has_change_permission(self, request: HttpRequest, obj: _ModelT | None = ...) -> bool: ...
    def has_delete_permission(self, request: HttpRequest, obj: _ModelT | None = ...) -> bool: ...
    def has_view_permission(self, request: HttpRequest, obj: _ModelT | None = ...) -> bool: ...
    def has_view_or_change_permission(self, request: HttpRequest, obj: _ModelT | None = ...) -> bool: ...
    def has_module_permission(self, request: HttpRequest) -> bool: ...

_DisplayT: TypeAlias = _ListOrTuple[str | Callable[[_ModelT], str | bool]]
_ModelAdmin = TypeVar("_ModelAdmin", bound=ModelAdmin)
_ActionCallable: TypeAlias = Callable[[_ModelAdmin, HttpRequest, QuerySet[_ModelT]], HttpResponseBase | None]

class ModelAdmin(BaseModelAdmin[_ModelT]):
    list_display: _DisplayT
    list_display_links: _DisplayT | None
    list_filter: _ListOrTuple[_ListFilterT]
    list_select_related: bool | Sequence[str]
    list_per_page: int
    list_max_show_all: int
    list_editable: Sequence[str]
    search_fields: Sequence[str]
    date_hierarchy: str | None
    save_as: bool
    save_as_continue: bool
    save_on_top: bool
    paginator: type
    preserve_filters: bool
    inlines: Sequence[type[InlineModelAdmin]]
    add_form_template: _TemplateForResponseT | None
    change_form_template: _TemplateForResponseT | None
    change_list_template: _TemplateForResponseT | None
    delete_confirmation_template: _TemplateForResponseT | None
    delete_selected_confirmation_template: _TemplateForResponseT | None
    object_history_template: _TemplateForResponseT | None
    popup_response_template: _TemplateForResponseT | None
    actions: Sequence[_ActionCallable[Any, _ModelT] | str] | None
    action_form: Any
    actions_on_top: bool
    actions_on_bottom: bool
    actions_selection_counter: bool
    model: type[_ModelT]
    opts: Options[_ModelT]
    admin_site: AdminSite
    def __init__(self, model: type[_ModelT], admin_site: AdminSite) -> None: ...
    def get_inline_instances(self, request: HttpRequest, obj: _ModelT | None = ...) -> list[InlineModelAdmin]: ...
    def get_urls(self) -> list[URLPattern]: ...
    @property
    def urls(self) -> list[URLPattern]: ...
    @property
    def media(self) -> Media: ...
    def get_model_perms(self, request: HttpRequest) -> dict[str, bool]: ...
    def get_form(
        self, request: HttpRequest, obj: _ModelT | None = ..., change: bool = ..., **kwargs: Any
    ) -> type[forms.ModelForm[_ModelT]]: ...
    def get_changelist(self, request: HttpRequest, **kwargs: Any) -> type[ChangeList]: ...
    def get_changelist_instance(self, request: HttpRequest) -> ChangeList: ...
    def get_object(self, request: HttpRequest, object_id: str, from_field: str | None = ...) -> _ModelT | None: ...
    def get_changelist_form(self, request: HttpRequest, **kwargs: Any) -> type[ModelForm[_ModelT]]: ...
    def get_changelist_formset(
        self, request: HttpRequest, **kwargs: Any
    ) -> type[BaseModelFormSet[_ModelT, ModelForm[_ModelT]]]: ...
    def get_formsets_with_inlines(self, request: HttpRequest, obj: _ModelT | None = ...) -> Iterator[Any]: ...
    def get_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
        per_page: int,
        orphans: int = ...,
        allow_empty_first_page: bool = ...,
    ) -> Paginator: ...
    def log_addition(self, request: HttpRequest, object: _ModelT, message: Any) -> LogEntry: ...
    def log_change(self, request: HttpRequest, object: _ModelT, message: Any) -> LogEntry: ...
    def log_deletion(self, request: HttpRequest, object: _ModelT, object_repr: str) -> LogEntry: ...
    def action_checkbox(self, obj: _ModelT) -> SafeString: ...
    def get_actions(self, request: HttpRequest) -> dict[str, tuple[Callable[..., str], str, str] | None]: ...
    def get_action_choices(
        self, request: HttpRequest, default_choices: list[tuple[str, str]] = ...
    ) -> list[tuple[str, str]]: ...
    def get_action(self, action: Callable | str) -> tuple[Callable[..., str], str, str] | None: ...
    def get_list_display(self, request: HttpRequest) -> _DisplayT: ...
    def get_list_display_links(self, request: HttpRequest, list_display: _DisplayT) -> _DisplayT: ...
    def get_list_filter(self, request: HttpRequest) -> Sequence[_ListFilterT]: ...
    def get_list_select_related(self, request: HttpRequest) -> bool | Sequence[str]: ...
    def get_search_fields(self, request: HttpRequest) -> Sequence[str]: ...
    def get_search_results(
        self, request: HttpRequest, queryset: QuerySet, search_term: str
    ) -> tuple[QuerySet[_ModelT], bool]: ...
    def get_preserved_filters(self, request: HttpRequest) -> str: ...
    def _get_edited_object_pks(self, request: HttpRequest, prefix: str) -> list[str]: ...
    def _get_list_editable_queryset(self, request: HttpRequest, prefix: str) -> QuerySet[_ModelT]: ...
    def construct_change_message(
        self, request: HttpRequest, form: AdminPasswordChangeForm, formsets: Iterable[BaseFormSet], add: bool = ...
    ) -> list[dict[str, dict[str, list[str]]]]: ...
    def message_user(
        self,
        request: HttpRequest,
        message: _StrOrPromise,
        level: int | str = ...,
        extra_tags: str = ...,
        fail_silently: bool = ...,
    ) -> None: ...
    def save_form(self, request: HttpRequest, form: Any, change: Any) -> Any: ...
    def save_model(self, request: HttpRequest, obj: _ModelT, form: Any, change: Any) -> None: ...
    def delete_model(self, request: HttpRequest, obj: _ModelT) -> None: ...
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None: ...
    def save_formset(self, request: HttpRequest, form: Any, formset: Any, change: Any) -> None: ...
    def save_related(self, request: HttpRequest, form: Any, formsets: Any, change: Any) -> None: ...
    def render_change_form(
        self,
        request: HttpRequest,
        context: dict[str, Any],
        add: bool = ...,
        change: bool = ...,
        form_url: str = ...,
        obj: _ModelT | None = ...,
    ) -> HttpResponse: ...
    def response_add(self, request: HttpRequest, obj: _ModelT, post_url_continue: str | None = ...) -> HttpResponse: ...
    def response_change(self, request: HttpRequest, obj: _ModelT) -> HttpResponse: ...
    def response_post_save_add(self, request: HttpRequest, obj: _ModelT) -> HttpResponseRedirect: ...
    def response_post_save_change(self, request: HttpRequest, obj: _ModelT) -> HttpResponseRedirect: ...
    # Probably FileResponse cannot come from ModelAdmin views
    def response_action(self, request: HttpRequest, queryset: QuerySet) -> HttpResponse | None: ...
    def response_delete(self, request: HttpRequest, obj_display: str, obj_id: int) -> HttpResponse: ...
    def render_delete_form(self, request: HttpRequest, context: dict[str, Any]) -> HttpResponse: ...
    def get_inline_formsets(
        self, request: HttpRequest, formsets: list[Any], inline_instances: list[Any], obj: _ModelT | None = ...
    ) -> list[Any]: ...
    def get_changeform_initial_data(self, request: HttpRequest) -> dict[str, str | list[str]]: ...
    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = ...,
        form_url: str = ...,
        extra_context: dict[str, Any] | None = ...,
    ) -> HttpResponse: ...
    def add_view(
        self, request: HttpRequest, form_url: str = ..., extra_context: dict[str, Any] | None = ...
    ) -> HttpResponse: ...
    def change_view(
        self, request: HttpRequest, object_id: str, form_url: str = ..., extra_context: dict[str, Any] | None = ...
    ) -> HttpResponse: ...
    def changelist_view(self, request: HttpRequest, extra_context: dict[str, Any] | None = ...) -> HttpResponse: ...
    def get_deleted_objects(
        self, objs: Sequence[_ModelT] | QuerySet[_ModelT], request: HttpRequest
    ) -> tuple[list[Model], dict[str, int], set[str], list[str]]: ...
    def delete_view(
        self, request: HttpRequest, object_id: str, extra_context: dict[str, Any] | None = ...
    ) -> HttpResponse: ...
    def history_view(
        self, request: HttpRequest, object_id: str, extra_context: dict[str, Any] | None = ...
    ) -> HttpResponse: ...

_ChildModelT = TypeVar("_ChildModelT", bound=Model)
_ParentModelT = TypeVar("_ParentModelT", bound=Model)

class InlineModelAdmin(Generic[_ChildModelT, _ParentModelT], BaseModelAdmin[_ChildModelT]):
    model: type[_ChildModelT]
    fk_name: str | None
    formset: type[BaseInlineFormSet[_ChildModelT, _ParentModelT, forms.ModelForm[_ChildModelT]]]
    extra: int
    min_num: int | None
    max_num: int | None
    template: str
    verbose_name: _StrOrPromise | None
    verbose_name_plural: _StrOrPromise | None
    can_delete: bool
    show_change_link: bool
    classes: Sequence[str] | None
    admin_site: AdminSite
    parent_model: type[_ParentModelT]
    opts: Options[_ChildModelT]
    has_registered_model: bool
    def __init__(self, parent_model: type[_ParentModelT], admin_site: AdminSite) -> None: ...
    @property
    def media(self) -> Media: ...
    def get_extra(self, request: HttpRequest, obj: _ParentModelT | None = ..., **kwargs: Any) -> int: ...
    def get_min_num(self, request: HttpRequest, obj: _ParentModelT | None = ..., **kwargs: Any) -> int | None: ...
    def get_max_num(self, request: HttpRequest, obj: _ParentModelT | None = ..., **kwargs: Any) -> int | None: ...
    def get_formset(
        self, request: HttpRequest, obj: _ParentModelT | None = ..., **kwargs: Any
    ) -> type[BaseInlineFormSet[_ChildModelT, _ParentModelT, forms.ModelForm[_ChildModelT]]]: ...
    def get_queryset(self, request: HttpRequest) -> QuerySet[_ChildModelT]: ...
    def has_add_permission(self, request: HttpRequest, obj: _ParentModelT | None) -> bool: ...  # type: ignore
    def has_change_permission(self, request: HttpRequest, obj: _ParentModelT | None = ...) -> bool: ...  # type: ignore
    def has_delete_permission(self, request: HttpRequest, obj: _ParentModelT | None = ...) -> bool: ...  # type: ignore
    def has_view_permission(self, request: HttpRequest, obj: _ParentModelT | None = ...) -> bool: ...  # type: ignore

class StackedInline(InlineModelAdmin[_ChildModelT, _ParentModelT]):
    template: str

class TabularInline(InlineModelAdmin[_ChildModelT, _ParentModelT]):
    template: str
