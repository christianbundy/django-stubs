from collections.abc import Callable
from typing import Any

def sensitive_variables(*variables: Any) -> Callable[..., Any]: ...
def sensitive_post_parameters(*parameters: Any) -> Callable[..., Any]: ...
