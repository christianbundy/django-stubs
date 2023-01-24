from collections.abc import Sequence
from typing import Any

from django.apps.config import AppConfig
from django.contrib.admin.options import BaseModelAdmin
from django.core.checks.messages import CheckMessage, Error
from django.db.models import Model

def check_admin_app(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> list[CheckMessage]: ...
def check_dependencies(**kwargs: Any) -> list[CheckMessage]: ...

class BaseModelAdminChecks:
    def check(self, admin_obj: BaseModelAdmin[Model], **kwargs: Any) -> list[CheckMessage]: ...

class ModelAdminChecks(BaseModelAdminChecks):
    def check(self, admin_obj: BaseModelAdmin[Model], **kwargs: Any) -> list[CheckMessage]: ...

class InlineModelAdminChecks(BaseModelAdminChecks):
    def check(self, inline_obj: BaseModelAdmin, **kwargs: Any) -> list[CheckMessage]: ...  # type: ignore

def must_be(type: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
def must_inherit_from(parent: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
def refer_to_missing_field(field: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
