from typing import Any

from _typeshed import Self
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.gdal.geometries import OGRGeometry
from django.contrib.gis.geometry import hex_regex as hex_regex  # noqa: F401
from django.contrib.gis.geometry import wkt_regex as wkt_regex
from django.contrib.gis.geos.base import GEOSBase
from django.contrib.gis.geos.coordseq import GEOSCoordSeq
from django.contrib.gis.geos.mutable_list import ListMixin
from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos.prepared import PreparedGeometry

class GEOSGeometryBase(GEOSBase):
    ptr_type: Any
    destructor: Any
    has_cs: bool
    def __init__(self, ptr: Any, cls: Any) -> None: ...
    def __copy__(self: Self) -> Self: ...
    def __deepcopy__(self: Self, memodict: Any) -> Self: ...
    @staticmethod
    def from_ewkt(ewkt: str) -> GEOSGeometry: ...
    @classmethod
    def from_gml(cls, gml_string: str) -> GEOSGeometry: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __or__(self, other: GEOSGeometry) -> GEOSGeometry: ...
    def __and__(self, other: GEOSGeometry) -> GEOSGeometry: ...
    def __sub__(self, other: GEOSGeometry) -> GEOSGeometry: ...
    def __xor__(self, other: GEOSGeometry) -> GEOSGeometry: ...
    @property
    def coord_seq(self) -> GEOSCoordSeq | None: ...
    @property
    def geom_type(self) -> str: ...
    @property
    def geom_typeid(self) -> int: ...
    @property
    def num_geom(self) -> int: ...
    @property
    def num_coords(self) -> int: ...
    @property
    def num_points(self) -> int: ...
    @property
    def dims(self) -> int: ...
    def normalize(self) -> None: ...
    @property
    def empty(self) -> bool: ...
    @property
    def hasz(self) -> bool: ...
    @property
    def ring(self) -> bool: ...
    @property
    def simple(self) -> bool: ...
    @property
    def valid(self) -> bool: ...
    @property
    def valid_reason(self) -> str: ...
    def contains(self, other: GEOSGeometry) -> bool: ...
    def covers(self, other: GEOSGeometry) -> bool: ...
    def crosses(self, other: GEOSGeometry) -> bool: ...
    def disjoint(self, other: GEOSGeometry) -> bool: ...
    def equals(self, other: GEOSGeometry) -> bool: ...
    def equals_exact(self, other: GEOSGeometry, tolerance: float = ...) -> bool: ...
    def intersects(self, other: GEOSGeometry) -> bool: ...
    def overlaps(self, other: GEOSGeometry) -> bool: ...
    def relate_pattern(self, other: GEOSGeometry, pattern: str) -> bool: ...
    def touches(self, other: GEOSGeometry) -> bool: ...
    def within(self, other: GEOSGeometry) -> bool: ...
    @property
    def srid(self) -> int | None: ...
    @srid.setter
    def srid(self, srid: int | None) -> None: ...
    @property
    def ewkt(self) -> str: ...
    @property
    def wkt(self) -> str: ...
    @property
    def hex(self) -> bytes: ...
    @property
    def hexewkb(self) -> bytes: ...
    @property
    def json(self) -> str: ...
    geojson: str
    @property
    def wkb(self) -> memoryview: ...
    @property
    def ewkb(self) -> memoryview: ...
    @property
    def kml(self) -> str: ...
    @property
    def prepared(self) -> PreparedGeometry: ...
    @property
    def ogr(self) -> OGRGeometry: ...
    @property
    def srs(self) -> SpatialReference | None: ...
    @property
    def crs(self) -> SpatialReference | None: ...
    ptr: Any
    def transform(self, ct: CoordTransform | SpatialReference | str | int, clone: bool = ...) -> GEOSGeometry: ...
    @property
    def boundary(self) -> GEOSGeometry: ...
    def buffer(self, width: float, quadsegs: int = ...) -> GEOSGeometry: ...
    def buffer_with_style(
        self,
        width: float,
        quadsegs: int = ...,
        end_cap_style: int = ...,
        join_style: int = ...,
        mitre_limit: float = ...,
    ) -> GEOSGeometry: ...
    @property
    def centroid(self) -> Point: ...
    @property
    def convex_hull(self) -> GEOSGeometry: ...
    def difference(self, other: GEOSGeometry) -> GEOSGeometry: ...
    @property
    def envelope(self) -> GEOSGeometry: ...
    def intersection(self, other: GEOSGeometry) -> GEOSGeometry: ...
    @property
    def point_on_surface(self) -> Point: ...
    def relate(self, other: GEOSGeometry) -> str: ...
    def simplify(self, tolerance: float = ..., preserve_topology: bool = ...) -> GEOSGeometry: ...
    def sym_difference(self, other: GEOSGeometry) -> GEOSGeometry: ...
    @property
    def unary_union(self) -> GEOSGeometry: ...
    def union(self, other: GEOSGeometry) -> GEOSGeometry: ...
    @property
    def area(self) -> float: ...
    def distance(self, other: GEOSGeometry) -> float: ...
    @property
    def extent(self) -> tuple[float, float, float, float]: ...
    @property
    def length(self) -> float: ...
    def clone(self: Self) -> Self: ...

class LinearGeometryMixin:
    def interpolate(self, distance: float) -> Point: ...
    def interpolate_normalized(self, distance: float) -> Point: ...
    def project(self, point: Point) -> float: ...
    def project_normalized(self, point: Point) -> float: ...
    @property
    def merged(self) -> GEOSGeometry: ...
    @property
    def closed(self) -> bool: ...

class GEOSGeometry(GEOSGeometryBase, ListMixin):
    def __init__(self, geo_input: Any, srid: int | None = ...) -> None: ...
