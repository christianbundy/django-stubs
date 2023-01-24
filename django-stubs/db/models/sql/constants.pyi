from re import Pattern
from typing import AnyStr

from typing_extensions import Final, Literal

GET_ITERATOR_CHUNK_SIZE: Final[int]

MULTI: Literal["multi"]
SINGLE: Literal["single"]
CURSOR: Literal["cursor"]
NO_RESULTS: Literal["no results"]

ORDER_PATTERN: Pattern[AnyStr]
ORDER_DIR: dict[str, tuple[str, str]]

INNER: Literal["INNER JOIN"]
LOUTER: Literal["LEFT OUTER JOIN"]
