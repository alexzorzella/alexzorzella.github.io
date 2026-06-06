from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AssetWithThumbnail:
    thumbnail_path: Path | None
    asset_path: Path
    commentary: str | None

    def get_visual(self):
        return self.thumbnail_path.as_posix() if self.thumbnail_path is not None else self.asset_path.as_posix()