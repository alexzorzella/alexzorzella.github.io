import datetime
from dataclasses import dataclass, field
from pathlib import Path

from assetwiththumbnail import AssetWithThumbnail
from webtools import create_element

@dataclass(frozen=True)
class MtgCard:
    id: str
    name: str
    created_at: datetime.datetime

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

    def render(self):
        data_search = self.front.commentary
        asset_path = self.front.asset_path.as_posix()

        front_image_path = self.front.get_visual()

        is_double_faced = self.back is not None

        if is_double_faced:
            data_search = self.back.commentary  # Back alt name contains front alt name

            back_image_path = self.back.get_visual()

            children = [create_element(
                "a",
                {"href": f"/{self.linked_page.as_posix()}" if self.linked_page is not None else asset_path},
                children=[
                    create_element("img", {"src": f"/{front_image_path}", "alt": data_search, "class": "flip__card-front"}, self_closing=True),
                    create_element("img", {"src": f"/{back_image_path}", "alt": data_search, "class": "flip__card-back"}, self_closing=True)
                ]
            )]
        else:
            children = [create_element(
                "a",
                {"href": f"{self.linked_page.as_posix()}" if self.linked_page is not None else asset_path},
                children=[
                    create_element("img", {"src": f"/{front_image_path}", "alt": data_search}, self_closing=True)
                ]
            )]

        return create_element(
            tag_name='li',
            attributes={"data-search": data_search, "class": self.li_class,
                        "data-card-type": "double_faced" if is_double_faced else None,
                        "title": self.front.commentary},
            children=children)