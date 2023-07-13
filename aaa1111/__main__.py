from pathlib import Path
from typing import List, Optional

from rich.status import Status
from typer import Argument, Option, Typer
from typing_extensions import Annotated
from ulid import ULID

from aaa1111.client import AAA1111
from aaa1111.utils import load_dict_file

app_txt2img = Typer(no_args_is_help=True)
app_img2img = Typer(no_args_is_help=True)


@app_txt2img.command()
def txt2img(
    params: Annotated[
        List[Path],
        Argument(
            show_default=False,
            help="Path to params files. .toml, .yaml, .yml, .json available.",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ],
    output: Annotated[
        Path,
        Option(
            "-o",
            "--output",
            help="Path to output directory.",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
        ),
    ] = "output",
    host: str = "127.0.0.1",
    port: int = 7860,
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host' and 'port' are ignored.",
        ),
    ] = None,
    https: bool = False,
    save_ext: str = "png",
):
    client = AAA1111(host=host, port=port, base_url=base_url, https=https)
    output.mkdir(parents=True, exist_ok=True)
    length = len(params)

    for i in range(length):
        payload = load_dict_file(params[i])
        prompts = payload.get("prompt", "")
        negatives = payload.get("negative_prompt", "")
        with Status(
            f"Requesting task {i + 1}/{length}...\nprompts: {prompts}\nnegatives: {negatives}"
        ):
            resp = client.txt2img(payload)

            for image in resp.images:
                image.save(output / (f"{ULID()}.{save_ext}"), lossless=True)


@app_img2img.command()
def img2img(
    params: Annotated[
        List[Path],
        Argument(
            show_default=False,
            help="Path to params files. .toml, .yaml, .yml, .json available.",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ],
    output: Annotated[
        Path,
        Option(
            "-o",
            "--output",
            help="Path to output directory.",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
        ),
    ] = "output",
    host: str = "127.0.0.1",
    port: int = 7860,
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host' and 'port' are ignored.",
        ),
    ] = None,
    https: bool = False,
    save_ext: str = "png",
):
    client = AAA1111(host=host, port=port, base_url=base_url, https=https)
    output.mkdir(parents=True, exist_ok=True)
    length = len(params)

    for i in range(length):
        payload = load_dict_file(params[i])
        prompts = payload.get("prompt", "")
        negatives = payload.get("negative_prompt", "")
        with Status(
            f"Requesting task {i + 1}/{length}...\nprompts: {prompts}\nnegatives: {negatives}"
        ):
            resp = client.img2img(payload)

            for image in resp.images:
                image.save(output / (f"{ULID()}.{save_ext}"), lossless=True)


if __name__ == "__main__":
    app_txt2img()
