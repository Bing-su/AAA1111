import base64
import io
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Union

import filetype
import orjson
import rtoml
from aiofile import async_open
from asyncer import asyncify
from PIL import Image
from ruamel.yaml import YAML

Image_Type = Union[str, Path, Image.Image]
DICT_EXT = (".toml", ".yaml", ".yml", "json")


def image_to_base64(img: Image_Type) -> str:
    if isinstance(img, Image.Image):
        buffer = io.BytesIO()
        img.save(buffer)
        value = buffer.getvalue()
    else:
        if isinstance(img, str) and not Path(img).is_file():
            # expect img is base64 string
            return img
        with open(img, "rb") as f:
            value = f.read()
    return base64.b64encode(value).decode("utf-8")


async def aimage_to_base64(img: Image_Type) -> str:
    if isinstance(img, Image.Image):
        buffer = io.BytesIO()
        img.save(buffer)
        value = buffer.getvalue()
    else:
        if isinstance(img, str) and not Path(img).is_file():
            # expect img is base64 string
            return img
        async with async_open(img, "rb") as f:
            value = await f.read()
    return base64.b64encode(value).decode("utf-8")


def base64_to_image(s: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(s)))


abase64_to_image = asyncify(base64_to_image)


def is_image_file(obj: Any) -> bool:
    if isinstance(obj, (str, Path)) and Path(obj).is_file():
        return filetype.image_match(obj) is not None
    return False


def _recursive_read_image(item: Any):
    if not isinstance(item, str) and isinstance(item, Sequence):
        return [
            image_to_base64(v) if is_image_file(v) else _recursive_read_image(v)
            for v in item
        ]
    if isinstance(item, Mapping):
        return {
            k: image_to_base64(v) if is_image_file(v) else _recursive_read_image(v)
            for k, v in item.items()
        }
    return item


def recursive_read_image(item: Mapping[str, Any]) -> Dict[str, Any]:
    return _recursive_read_image(item)


async def _arecursive_read_image(item: Any):
    if not isinstance(item, str) and isinstance(item, Sequence):
        return [
            (await aimage_to_base64(v))
            if is_image_file(v)
            else (await _arecursive_read_image(v))
            for v in item
        ]
    if isinstance(item, Mapping):
        return {
            k: (await aimage_to_base64(v))
            if is_image_file(v)
            else (await _arecursive_read_image(v))
            for k, v in item.items()
        }
    return item


async def arecursive_read_image(item: Mapping[str, Any]) -> Dict[str, Any]:
    return await _arecursive_read_image(item)


def is_valid_dict_file(file: Union[str, Path]) -> bool:
    ext = Path(file).suffix
    return ext in DICT_EXT


def load_dict_file(file: Union[str, Path]) -> Dict[str, Any]:
    if not is_valid_dict_file(file):
        msg = f"Unsupported file extension: {file!r}"
        raise ValueError(msg)
    ext = Path(file).suffix

    with open(file, encoding="utf-8") as raw:
        if ext == ".toml":
            return rtoml.load(raw)
        if ext == ".json":
            return orjson.loads(raw.read())
        yaml = YAML()
        return dict(yaml.load(raw))


async def aload_dict_file(file: Union[str, Path]) -> Dict[str, Any]:
    if not is_valid_dict_file(file):
        msg = f"Unsupported file extension: {file!r}"
        raise ValueError(msg)
    ext = Path(file).suffix

    async with async_open(file, encoding="utf-8") as raw:
        data = await raw.read()
        if ext == ".toml":
            return rtoml.loads(data)
        if ext == ".json":
            return orjson.loads(data)
        yaml = YAML()
        return dict(yaml.load(data))
