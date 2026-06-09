import datetime
from dataclasses import dataclass, field
from pathlib import Path

from assetwiththumbnail import AssetWithThumbnail
from webtools import create_element

@dataclass(frozen=True)
class ImageElementData:
    id: str
    name: str
    creation_date: datetime.datetime

    front: AssetWithThumbnail
    back: AssetWithThumbnail | None = None

    li_class: str | None = None
    linked_page: Path | None = None

    article_paragraphs: list[str] = field(default_factory=list)

    def get_front_asset(self):
        return self.front.asset_path.as_posix()

    def get_front_thumbnail(self):
        return self.front.thumbnail_path.as_posix() if self.front.thumbnail_path is not None else self.get_front_asset()

    def get_back_asset(self):
        return self.back.asset_path.as_posix()

    def get_back_thumbnail(self):
        return self.back.thumbnail_path.as_posix() if self.back.thumbnail_path is not None else self.get_back_asset()

    def get_front_commentary(self):
        return self.front.commentary or ""

    def get_back_commentary(self):
        return self.get_front_commentary()

    def render(self, link_to_raw_asset: bool = False, raw_image: bool = False):
        data_search = self.id
        asset_path = self.front.asset_path.as_posix()

        front_image_path = self.front.get_visual() if not raw_image else self.front.asset_path

        is_double_faced = self.back is not None

        href = f"{self.linked_page.as_posix()}" if self.linked_page is not None and not link_to_raw_asset else f"/{asset_path}"

        if is_double_faced:
            back_image_path = self.back.get_visual()

            children = [create_element(
                "a",
                {"href": href},
                children=[
                    create_element("img", {"src": f"/{front_image_path}", "alt": data_search, "class": "flip__card-front"}, self_closing=True),
                    create_element("img", {"src": f"/{back_image_path}", "alt": data_search, "class": "flip__card-back"}, self_closing=True)
                ]
            )]
        else:
            children = [create_element(
                "a",
                {"href": href},
                children=[
                    create_element("img", {"src": f"/{front_image_path}", "alt": data_search}, self_closing=True)
                ]
            )]

        attributes = {
            "data-search": data_search,
            "data-card-type": "double_faced" if is_double_faced else None,
            "title": self.front.commentary
        }

        if self.li_class is not None:
            attributes["class"] = self.li_class

        if raw_image:
            attributes["class"] = ""
            attributes["style"] = "display: flex; justify-content: center;"
            return create_element(tag_name='div', attributes=attributes, children=children)

        return create_element(tag_name='li', attributes=attributes, children=children)