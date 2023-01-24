from collections import namedtuple
from collections.abc import Iterator
from typing import Any

from django.db.migrations.state import ModelState, ProjectState
from django.db.models import Field, Model
from typing_extensions import Literal

def resolve_relation(
    model: str | type[Model], app_label: str | None = ..., model_name: str | None = ...
) -> tuple[str, str]: ...

FieldReference = namedtuple("FieldReference", ["to", "through"])

def field_references(
    model_tuple: tuple[str, str],
    field: Field[Any, Any],
    reference_model_tuple: tuple[str, str],
    reference_field_name: str | None = ...,
    reference_field: Field[Any, Any] | None = ...,
) -> Literal[False] | FieldReference: ...
def get_references(
    state: ProjectState,
    model_tuple: tuple[str, str],
    field_tuple: tuple[()] | tuple[str, Field[Any, Any]] = ...,
) -> Iterator[tuple[ModelState, str, Field[Any, Any], FieldReference]]: ...
def field_is_referenced(
    state: ProjectState, model_tuple: tuple[str, str], field_tuple: tuple[str, Field[Any, Any]]
) -> bool: ...
