from collections.abc import Iterable, Mapping
from typing import Any, Generic, TypeVar

from _typeshed import Self
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Expression, Func
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType, _ParamT
from django.utils.datastructures import OrderedSet
from typing_extensions import Literal

_T = TypeVar("_T")

class Lookup(Generic[_T]):
    lookup_name: str
    prepare_rhs: bool
    can_use_none_as_rhs: bool
    lhs: Any
    rhs: Any
    bilateral_transforms: list[type[Transform]]
    def __init__(self, lhs: Any, rhs: Any) -> None: ...
    def apply_bilateral_transforms(self, value: Expression) -> Expression: ...
    def batch_process_rhs(
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, rhs: OrderedSet | None = ...
    ) -> tuple[list[str], list[str]]: ...
    def get_source_expressions(self) -> list[Expression]: ...
    def set_source_expressions(self, new_exprs: list[Expression]) -> None: ...
    def get_prep_lookup(self) -> Any: ...
    def get_db_prep_lookup(self, value: _ParamT, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def process_lhs(
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, lhs: Expression | None = ...
    ) -> _AsSqlType: ...
    def process_rhs(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def rhs_is_direct_value(self) -> bool: ...
    def relabeled_clone(self: Self, relabels: Mapping[str, str]) -> Self: ...
    def get_group_by_cols(self, alias: str | None = ...) -> list[Expression]: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    @property
    def contains_aggregate(self) -> bool: ...
    @property
    def contains_over_clause(self) -> bool: ...
    @property
    def is_summary(self) -> bool: ...
    @property
    def identity(self) -> tuple[type[Lookup[Any]], Any, Any]: ...

class Transform(RegisterLookupMixin, Func):
    bilateral: bool
    @property
    def lhs(self) -> Expression: ...
    def get_bilateral_transforms(self) -> list[type[Transform]]: ...

class BuiltinLookup(Lookup[_T]):
    def process_lhs(
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, lhs: Expression | None = ...
    ) -> _AsSqlType: ...
    def get_rhs_op(self, connection: BaseDatabaseWrapper, rhs: str) -> str: ...

class FieldGetDbPrepValueMixin:
    get_db_prep_lookup_value_is_iterable: bool
    def get_db_prep_lookup(self, value: _ParamT, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class FieldGetDbPrepValueIterableMixin(FieldGetDbPrepValueMixin):
    get_db_prep_lookup_value_is_iterable: Literal[True]
    def get_prep_lookup(self) -> Iterable[Any]: ...
    def resolve_expression_parameter(
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, sql: str, param: Any
    ) -> _AsSqlType: ...

class PostgresOperatorLookup(FieldGetDbPrepValueMixin, Lookup[_T]):
    postgres_operator: str
    def as_postgresql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class Exact(FieldGetDbPrepValueMixin, BuiltinLookup[_T]): ...
class IExact(BuiltinLookup[_T]): ...
class GreaterThan(FieldGetDbPrepValueMixin, BuiltinLookup[_T]): ...
class GreaterThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup[_T]): ...
class LessThan(FieldGetDbPrepValueMixin, BuiltinLookup[_T]): ...
class LessThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup[_T]): ...

class IntegerFieldFloatRounding:
    rhs: Any
    def get_prep_lookup(self) -> Any: ...

class IntegerGreaterThanOrEqual(IntegerFieldFloatRounding, GreaterThanOrEqual[int | float]): ...
class IntegerLessThan(IntegerFieldFloatRounding, LessThan[int | float]): ...

class In(FieldGetDbPrepValueIterableMixin, BuiltinLookup):
    def split_parameter_list_as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> Any: ...

class PatternLookup(BuiltinLookup[str]):
    param_pattern: str

class Contains(PatternLookup): ...
class IContains(Contains): ...
class StartsWith(PatternLookup): ...
class IStartsWith(StartsWith): ...
class EndsWith(PatternLookup): ...
class IEndsWith(EndsWith): ...
class Range(FieldGetDbPrepValueIterableMixin, BuiltinLookup[_T]): ...
class IsNull(BuiltinLookup[bool]): ...
class Regex(BuiltinLookup[str]): ...
class IRegex(Regex): ...

class YearLookup(Lookup[Any]):
    def year_lookup_bounds(self, connection: BaseDatabaseWrapper, year: int) -> list[str]: ...
    def get_direct_rhs_sql(self, connection: BaseDatabaseWrapper, rhs: str) -> str: ...
    def get_bound_params(self, start: Any, finish: Any) -> Any: ...

class YearExact(YearLookup, Exact[_T]):
    def get_bound_params(self, start: Any, finish: Any) -> tuple[Any, Any]: ...

class YearGt(YearLookup, GreaterThan[_T]):
    def get_bound_params(self, start: Any, finish: Any) -> tuple[Any]: ...

class YearGte(YearLookup, GreaterThanOrEqual[_T]):
    def get_bound_params(self, start: Any, finish: Any) -> tuple[Any]: ...

class YearLt(YearLookup, LessThan[_T]):
    def get_bound_params(self, start: Any, finish: Any) -> tuple[Any]: ...

class YearLte(YearLookup, LessThanOrEqual[_T]):
    def get_bound_params(self, start: Any, finish: Any) -> tuple[Any]: ...

class UUIDTextMixin:
    rhs: Any
    def process_rhs(self, qn: Any, connection: BaseDatabaseWrapper) -> Any: ...

class UUIDIExact(UUIDTextMixin, IExact[_T]): ...
class UUIDContains(UUIDTextMixin, Contains): ...
class UUIDIContains(UUIDTextMixin, IContains): ...
class UUIDStartsWith(UUIDTextMixin, StartsWith): ...
class UUIDIStartsWith(UUIDTextMixin, IStartsWith): ...
class UUIDEndsWith(UUIDTextMixin, EndsWith): ...
class UUIDIEndsWith(UUIDTextMixin, IEndsWith): ...
