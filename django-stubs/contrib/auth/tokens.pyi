from datetime import date, datetime
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser

class PasswordResetTokenGenerator:
    key_salt: str
    secret: str | bytes
    secret_fallbacks: list[str | bytes]
    algorithm: str
    def make_token(self, user: AbstractBaseUser) -> str: ...
    def check_token(self, user: AbstractBaseUser | None, token: str | None) -> bool: ...
    def _make_token_with_timestamp(self, user: AbstractBaseUser, timestamp: int, secret: str | bool = ...) -> str: ...
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str: ...
    def _num_seconds(self, dt: datetime | date) -> int: ...
    def _now(self) -> datetime: ...

default_token_generator: Any
