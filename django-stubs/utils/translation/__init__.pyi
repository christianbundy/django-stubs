import functools
from collections.abc import Callable
from contextlib import ContextDecorator
from types import TracebackType
from typing import Any

from django.http.request import HttpRequest
from django.utils.functional import _StrPromise

LANGUAGE_SESSION_KEY: str

class TranslatorCommentWarning(SyntaxWarning): ...

class Trans:
    activate: Callable[..., Any]
    check_for_language: functools._lru_cache_wrapper[Any]
    deactivate: Callable[..., Any]
    deactivate_all: Callable[..., Any]
    get_language: Callable[..., Any]
    get_language_bidi: Callable[..., Any]
    get_language_from_path: Callable[..., Any]
    get_language_from_request: Callable[..., Any]
    gettext: Callable[..., Any]
    gettext_noop: Callable[..., Any]
    ngettext: Callable[..., Any]
    npgettext: Callable[..., Any]
    pgettext: Callable[..., Any]
    def __getattr__(self, real_name: Any) -> Any: ...

def gettext_noop(message: str) -> str: ...
def gettext(message: str) -> str: ...
def ngettext(singular: str, plural: str, number: float) -> str: ...
def pgettext(context: str, message: str) -> str: ...
def npgettext(context: str, singular: str, plural: str, number: int) -> str: ...

# lazy evaluated translation functions
def gettext_lazy(message: str) -> _StrPromise: ...
def pgettext_lazy(context: str, message: str) -> _StrPromise: ...
def ngettext_lazy(singular: str, plural: str, number: int | str | None = ...) -> _StrPromise: ...
def npgettext_lazy(context: str, singular: str, plural: str, number: int | str | None = ...) -> _StrPromise: ...

# NOTE: These translation functions are deprecated and removed in Django 4.0. We should remove them when we drop
# support for 3.2
def ugettext_noop(message: str) -> str: ...
def ugettext(message: str) -> str: ...
def ungettext(singular: str, plural: str, number: float) -> str: ...

ugettext_lazy = gettext_lazy

ungettext_lazy = ngettext_lazy

def activate(language: str) -> None: ...
def deactivate() -> None: ...

class override(ContextDecorator):
    language: str | None
    deactivate: bool
    def __init__(self, language: str | None, deactivate: bool = ...) -> None: ...
    old_language: str | None
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

def get_language() -> str: ...
def get_language_from_path(path: str) -> str | None: ...
def get_language_bidi() -> bool: ...
def check_for_language(lang_code: str | None) -> bool: ...
def to_language(locale: str) -> str: ...
def to_locale(language: str) -> str: ...
def get_language_from_request(request: HttpRequest, check_path: bool = ...) -> str: ...
def templatize(src: str, **kwargs: Any) -> str: ...
def deactivate_all() -> None: ...
def get_supported_language_variant(lang_code: str, *, strict: bool = ...) -> str: ...
def get_language_info(lang_code: str) -> Any: ...
def trim_whitespace(s: str) -> str: ...
def round_away_from_one(value: int) -> int: ...
