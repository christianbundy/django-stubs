from argparse import ArgumentParser, HelpFormatter, Namespace
from collections.abc import Callable, Iterable, Sequence
from io import TextIOBase
from typing import Any, TextIO

from django.apps.config import AppConfig
from django.core.management.color import Style
from django.utils.datastructures import _ListOrTuple
from typing_extensions import Literal

class CommandError(Exception):
    def __init__(self, *args: Any, returncode: int = ..., **kwargs: Any) -> None: ...

class SystemCheckError(CommandError): ...

class CommandParser(ArgumentParser):
    missing_args_message: str | None
    called_from_command_line: bool | None
    def __init__(
        self, *, missing_args_message: str | None = ..., called_from_command_line: bool | None = ..., **kwargs: Any
    ) -> None: ...
    def error(self, message: str) -> Any: ...

def handle_default_options(options: Namespace) -> None: ...
def no_translations(handle_func: Callable[..., Any]) -> Callable[..., Any]: ...

class DjangoHelpFormatter(HelpFormatter):
    show_last: set[str]
    def add_usage(self, usage: str | None, actions: Iterable[Any], *args: Any, **kwargs: Any) -> Any: ...
    def add_arguments(self, actions: Any) -> Any: ...

class OutputWrapper(TextIOBase):
    @property
    def style_func(self) -> Callable[[str], str]: ...
    @style_func.setter
    def style_func(self, style_func: Callable[[str], str] | None) -> None: ...
    ending: str
    def __init__(self, out: TextIO, ending: str = ...) -> None: ...
    def __getattr__(self, name: str) -> Callable[..., Any]: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def write(  # type: ignore[override]
        self, msg: str = ..., style_func: Callable[[str], str] | None = ..., ending: str | None = ...
    ) -> None: ...

class BaseCommand:
    help: str
    output_transaction: bool
    requires_migrations_checks: bool
    requires_system_checks: _ListOrTuple[str] | Literal["__all__"]
    base_stealth_options: tuple[str, ...]
    stealth_options: tuple[str, ...]
    stdout: OutputWrapper
    stderr: OutputWrapper
    style: Style
    def __init__(
        self,
        stdout: TextIO | None = ...,
        stderr: TextIO | None = ...,
        no_color: bool = ...,
        force_color: bool = ...,
    ) -> None: ...
    def get_version(self) -> str: ...
    def create_parser(self, prog_name: str, subcommand: str, **kwargs: Any) -> CommandParser: ...
    def add_arguments(self, parser: CommandParser) -> None: ...
    def print_help(self, prog_name: str, subcommand: str) -> None: ...
    def run_from_argv(self, argv: list[str]) -> None: ...
    def execute(self, *args: Any, **options: Any) -> str | None: ...
    def check(
        self,
        app_configs: Sequence[AppConfig] | None = ...,
        tags: Sequence[str] | None = ...,
        display_num_errors: bool = ...,
        include_deployment_checks: bool = ...,
        fail_level: int = ...,
        databases: Sequence[str] | None = ...,
    ) -> None: ...
    def check_migrations(self) -> None: ...
    def handle(self, *args: Any, **options: Any) -> str | None: ...

class AppCommand(BaseCommand):
    missing_args_message: str
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, *app_labels: str, **options: Any) -> str | None: ...
    def handle_app_config(self, app_config: Any, **options: Any) -> str | None: ...

class LabelCommand(BaseCommand):
    label: str
    missing_args_message: Any
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, *labels: str, **options: Any) -> str | None: ...
    def handle_label(self, label: str, **options: Any) -> str | None: ...
