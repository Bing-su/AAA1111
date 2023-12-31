import base64
import io
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Union

import orjson
import pyjson5
import rtoml
from aiofile import async_open
from beartype import beartype
from PIL import Image, PngImagePlugin
from ruamel.yaml import YAML
from ulid import ULID

ImageType = Union[str, Path, Image.Image]  # prevent circular import
PathType = Union[str, Path]

FILE_EXT = (".toml", ".yaml", ".yml", ".json", ".json5")
available_extensions = Image.registered_extensions()


@beartype
def pil_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    # 1. png
    if "parameters" in img.info:
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", img.info["parameters"])
        img.save(buf, format="png", pnginfo=pnginfo)
    # 2. else
    else:
        img.save(buf, format="webp", lossless=True, exif=img.getexif())
    value = buf.getvalue()
    return base64.b64encode(value).decode("utf-8")


@beartype
def image_to_base64(img: ImageType) -> str:
    if isinstance(img, Image.Image):
        return pil_to_base64(img)

    if isinstance(img, str) and not Path(img).is_file():
        # expect img is base64 string
        return img
    with open(img, "rb") as f:
        value = f.read()
    return base64.b64encode(value).decode("utf-8")


@beartype
async def aimage_to_base64(img: ImageType) -> str:
    if isinstance(img, Image.Image):
        return pil_to_base64(img)

    if isinstance(img, str) and not Path(img).is_file():
        # expect img is base64 string
        return img
    async with async_open(img, "rb") as f:
        value = await f.read()
    return base64.b64encode(value).decode("utf-8")


@beartype
def base64_to_image(s: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(s)))


def is_image(obj: Any) -> bool:
    if isinstance(obj, (str, Path)) and (p := Path(obj)).is_file():
        return p.suffix.lower() in available_extensions
    return isinstance(obj, Image.Image)


def _recursive_read_image(item: Any):
    if not isinstance(item, str) and isinstance(item, Sequence):
        return [
            image_to_base64(v) if is_image(v) else _recursive_read_image(v)
            for v in item
        ]
    if isinstance(item, Mapping):
        return {
            k: image_to_base64(v) if is_image(v) else _recursive_read_image(v)
            for k, v in item.items()
        }
    return item


def recursive_read_image(item: Mapping[str, Any]) -> Dict[str, Any]:
    return _recursive_read_image(item)


async def _arecursive_read_image(item: Any):
    if not isinstance(item, str) and isinstance(item, Sequence):
        return [
            (await aimage_to_base64(v))
            if is_image(v)
            else (await _arecursive_read_image(v))
            for v in item
        ]
    if isinstance(item, Mapping):
        return {
            k: (await aimage_to_base64(v))
            if is_image(v)
            else (await _arecursive_read_image(v))
            for k, v in item.items()
        }
    return item


async def arecursive_read_image(item: Mapping[str, Any]) -> Dict[str, Any]:
    return await _arecursive_read_image(item)


@beartype
def is_valid_file(file: PathType) -> bool:
    ext = Path(file).suffix.lower()
    return ext in FILE_EXT


@beartype
def load_from_file(file: PathType) -> Dict[str, Any]:
    if not is_valid_file(file):
        msg = f"Unsupported file extension: {file!r}"
        raise ValueError(msg)
    ext = Path(file).suffix.lower()

    with open(file, encoding="utf-8") as raw:
        if ext == ".toml":
            return rtoml.load(raw)
        if ext == ".json":
            return orjson.loads(raw.read())
        if ext == ".json5":
            return pyjson5.decode_io(raw)
        return dict(YAML().load(raw))


@beartype
async def aload_from_file(file: PathType) -> Dict[str, Any]:
    if not is_valid_file(file):
        msg = f"Unsupported file extension: {file!r}"
        raise ValueError(msg)
    ext = Path(file).suffix.lower()

    async with async_open(file, encoding="utf-8") as raw:
        data = await raw.read()
        if ext == ".toml":
            return rtoml.loads(data)
        if ext == ".json":
            return orjson.loads(data)
        if ext == ".json5":
            return pyjson5.decode(data)
        return dict(YAML().load(data))


def save_image(
    image: Image.Image,
    save_dir: Path,
    infotext: Optional[str] = None,
    ext: str = "png",
    quality: int = 95,
    lossless: bool = True,
) -> Path:
    if not ext.startswith("."):
        ext = "." + ext
    path = save_dir.joinpath(str(ULID())).with_suffix(ext)

    if not infotext:
        image.save(path, quality=quality, lossless=lossless)

    elif ext.lower().endswith("png"):
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", infotext)
        image.save(path, pnginfo=pnginfo, quality=quality)

    else:
        exif = image.getexif()
        # https://github.com/python-pillow/Pillow/issues/4935#issuecomment-698027721
        exif[0x9286] = infotext
        image.save(path, quality=quality, lossless=lossless, exif=exif)

    return path
