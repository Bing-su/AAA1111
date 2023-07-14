import io
from pathlib import Path
from typing import Any, Dict, List, Optional

import rich.progress as pg
from rich.panel import Panel
from rich.syntax import Syntax
from ruamel.yaml import YAML
from typer import Argument, Option, Typer
from typing_extensions import Annotated
from ulid import ULID

from aaa1111.client import AAA1111
from aaa1111.utils import load_dict_file

app_txt2img = Typer()
app_img2img = Typer()
yaml = YAML()


@app_txt2img.command(no_args_is_help=True)
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
            envvar="AAA1111_OUTPUT_DIR",
        ),
    ] = "output",
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host' and 'port' and 'https' are ignored.",
            envvar="AAA1111_BASE_URL",
        ),
    ] = None,
    host: str = "127.0.0.1",
    port: int = 7860,
    https: bool = False,
    save_ext: str = "png",
):
    _inner(params, output, base_url, host, port, https, save_ext, task="txt2img")


@app_img2img.command(no_args_is_help=True)
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
            envvar="AAA1111_OUTPUT_DIR",
        ),
    ] = "output",
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host' and 'port' and 'https' are ignored.",
            envvar="AAA1111_BASE_URL",
        ),
    ] = None,
    host: str = "127.0.0.1",
    port: int = 7860,
    https: bool = False,
    save_ext: str = "png",
):
    _inner(params, output, base_url, host, port, https, save_ext, task="img2img")


def _inner(
    params: List[Path],
    output: Path,
    base_url: Optional[str],
    host: str,
    port: int,
    https: bool,
    save_ext: str,
    *,
    task: str = "txt2img",
):
    client = AAA1111(host=host, port=port, base_url=base_url, https=https)
    output.mkdir(parents=True, exist_ok=True)
    length = len(params)

    progress = pg.Progress(
        pg.SpinnerColumn(),
        pg.TextColumn("[progress.description]{task.description}"),
        pg.TimeElapsedColumn(),
        pg.TimeRemainingColumn(),
        pg.MofNCompleteColumn(),
    )

    with progress:
        for i in progress.track(range(length), description=f"Processing {task}..."):
            payload = load_dict_file(params[i])
            panel = Panel(
                Syntax(format_payload(payload), "yaml", theme="ansi_dark"),
                title=f"{task} [green]{i + 1}/{length}[/green]",
            )
            progress.print(panel)
            if task == "txt2img":
                resp = client.txt2img(payload)
            elif task == "img2img":
                resp = client.img2img(payload)
            else:
                msg = f"Unknown task: {task}"
                raise ValueError(msg)

            for image in resp.images:
                image.save(output / (f"{ULID()}.{save_ext}"), lossless=True)


def format_payload(payload: Dict[str, Any]) -> str:
    stream = io.StringIO()
    yaml.dump(payload, stream)
    return stream.getvalue().strip()


if __name__ == "__main__":
    app_txt2img()
