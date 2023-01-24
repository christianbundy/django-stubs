from collections.abc import Iterable, Sequence
from typing import Any

from django.contrib.syndication.views import Feed as BaseFeed
from django.db.models import Model
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.utils.xmlutils import SimplerXMLGenerator

class GeoFeedMixin:
    def georss_coords(self, coords: Iterable[Sequence[float]]) -> str: ...
    def add_georss_point(self, handler: SimplerXMLGenerator, coords: Sequence[float], w3c_geo: bool = ...) -> None: ...
    def add_georss_element(self, handler: SimplerXMLGenerator, item: dict[str, Any], w3c_geo: bool = ...) -> None: ...

class GeoRSSFeed(Rss201rev2Feed, GeoFeedMixin):
    def rss_attributes(self) -> dict[str, str]: ...

class GeoAtom1Feed(Atom1Feed, GeoFeedMixin): ...

class W3CGeoFeed(Rss201rev2Feed, GeoFeedMixin):
    def rss_attributes(self) -> dict[str, str]: ...

class Feed(BaseFeed[Model, Any]): ...
