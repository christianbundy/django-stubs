from collections.abc import Callable
from typing import Any

NONE_ID: Any
NO_RECEIVERS: Any

class Signal:
    receivers: Any
    providing_args: Any
    lock: Any
    use_caching: Any
    sender_receivers_cache: Any
    def __init__(self, providing_args: list[str] = ..., use_caching: bool = ...) -> None: ...
    def connect(
        self,
        receiver: Callable[..., Any],
        sender: object | None = ...,
        weak: bool = ...,
        dispatch_uid: str | None = ...,
    ) -> None: ...
    def disconnect(
        self, receiver: Callable[..., Any] | None = ..., sender: object | None = ..., dispatch_uid: str | None = ...
    ) -> bool: ...
    def has_listeners(self, sender: Any = ...) -> bool: ...
    def send(self, sender: Any, **named: Any) -> list[tuple[Callable[..., Any], str | None]]: ...
    def send_robust(self, sender: Any, **named: Any) -> list[tuple[Callable[..., Any], Exception | str]]: ...

def receiver(signal: list[Signal] | Signal, **kwargs: Any) -> Callable[..., Any]: ...
