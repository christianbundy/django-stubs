from collections.abc import Callable
from typing import Any, TypeVar, overload

from _typeshed import Self
from typing_extensions import TypeAlias

_SD = TypeVar("_SD", bound=SafeData)

class SafeData:
    def __html__(self: Self) -> Self: ...

class SafeString(str, SafeData):
    @overload
    def __add__(self, rhs: SafeString) -> SafeString: ...
    @overload
    def __add__(self, rhs: str) -> str: ...

SafeText: TypeAlias = SafeString

_C = TypeVar("_C", bound=Callable[..., Any])

@overload
def mark_safe(s: _SD) -> _SD: ...
@overload
def mark_safe(s: _C) -> _C: ...
@overload
def mark_safe(s: Any) -> SafeString: ...
