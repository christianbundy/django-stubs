from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any

from django.apps import AppConfig
from django.apps.registry import Apps
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.manager import Manager

class AppConfigStub(AppConfig): ...

class ModelState:
    name: str
    app_label: str
    fields: dict[str, Field[Any, Any]]
    options: dict[str, Any]
    bases: Sequence[type[Model] | str]
    managers: list[tuple[str, Manager]]
    def __init__(
        self,
        app_label: str,
        name: str,
        fields: list[tuple[str, Field[Any, Any]]] | dict[str, Field[Any, Any]],
        options: dict[str, Any] | None = ...,
        bases: Sequence[type[Model] | str] | None = ...,
        managers: list[tuple[str, Manager]] | None = ...,
    ) -> None: ...
    def clone(self) -> ModelState: ...
    def construct_managers(self) -> Iterator[tuple[str, Manager]]: ...
    @classmethod
    def from_model(cls, model: type[Model], exclude_rels: bool = ...) -> ModelState: ...
    # Removed in 3.2, but back in 4.0
    # def get_field(self, field_name: str) -> Field: ...
    @property
    def name_lower(self) -> str: ...
    def render(self, apps: Apps) -> Any: ...
    def get_index_by_name(self, name: str) -> Any: ...
    def get_constraint_by_name(self, name: str) -> Any: ...
    def __eq__(self, other: object) -> bool: ...

def get_related_models_tuples(model: type[Model]) -> set[tuple[str, str]]: ...
def get_related_models_recursive(model: type[Model]) -> set[tuple[str, str]]: ...

class ProjectState:
    is_delayed: bool
    models: dict[Any, Any]
    real_apps: list[str]
    def __init__(
        self, models: dict[tuple[str, str], ModelState] | None = ..., real_apps: list[str] | None = ...
    ) -> None: ...
    def add_model(self, model_state: ModelState) -> None: ...
    @property
    def apps(self) -> StateApps: ...
    def clear_delayed_apps_cache(self) -> None: ...
    def clone(self) -> ProjectState: ...
    @property
    def concrete_apps(self) -> StateApps: ...
    @classmethod
    def from_apps(cls, apps: Apps) -> ProjectState: ...
    def reload_model(self, app_label: str, model_name: str, delay: bool = ...) -> None: ...
    def reload_models(self, models: list[Any], delay: bool = ...) -> None: ...
    def remove_model(self, app_label: str, model_name: str) -> None: ...

class StateApps(Apps):
    real_models: list[ModelState]
    def __init__(
        self, real_apps: list[str], models: dict[tuple[str, str], ModelState], ignore_swappable: bool = ...
    ) -> None: ...
    @contextmanager
    def bulk_update(self) -> Iterator[None]: ...
    def clone(self) -> StateApps: ...
    def render_multiple(self, model_states: list[ModelState]) -> None: ...
    def register_model(self, app_label: str, model: type[Model]) -> None: ...
    def unregister_model(self, app_label: str, model_name: str) -> None: ...
