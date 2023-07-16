import io
from pathlib import Path
from typing import Any, Dict, List, Optional

import rich.progress as pg
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from ruamel.yaml import YAML
from typer import Argument, Option, Typer
from typing_extensions import Annotated

from aaa1111.client import AAA1111
from aaa1111.utils import FILE_EXT, load_from_file, save_image

app_txt2img = Typer()
app_img2img = Typer()


defalut_output = Path("output")


@app_txt2img.command(no_args_is_help=True)
def txt2img(
    params: Annotated[
        List[Path],
        Argument(
            show_default=False,
            help="Path to params files. .toml, .yaml, .yml, .json, .json5 available. others will be ignored.",
            exists=True,
            rich_help_panel="api",
        ),
    ],
    save_dir: Annotated[
        Path,
        Option(
            "-d",
            "--save-dir",
            help="Path to save directory.",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            envvar="AAA1111_SAVE_DIR",
            rich_help_panel="save",
        ),
    ] = defalut_output,
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host', 'port' and 'https' are ignored.",
            envvar="AAA1111_BASE_URL",
            rich_help_panel="api",
        ),
    ] = None,
    host: Annotated[str, Option("-h", "--host", rich_help_panel="api")] = "127.0.0.1",
    port: Annotated[int, Option("-p", "--port", rich_help_panel="api")] = 7860,
    https: Annotated[bool, Option(rich_help_panel="api")] = False,
    save_ext: Annotated[
        str, Option("-e", "--save-ext", rich_help_panel="save")
    ] = "png",
    quality: Annotated[int, Option("-q", "--quality", rich_help_panel="save")] = 95,
    lossless: Annotated[bool, Option(rich_help_panel="save")] = True,
):
    _inner(
        params,
        save_dir,
        base_url,
        host,
        port,
        https,
        save_ext,
        quality,
        lossless,
        task="txt2img",
    )


@app_img2img.command(no_args_is_help=True)
def img2img(
    params: Annotated[
        List[Path],
        Argument(
            show_default=False,
            help="Path to params files. .toml, .yaml, .yml, .json, .json5 available. others will be ignored.",
            exists=True,
            rich_help_panel="api",
        ),
    ],
    save_dir: Annotated[
        Path,
        Option(
            "-d",
            "--save-dir",
            help="Path to save directory.",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            envvar="AAA1111_SAVE_DIR",
            rich_help_panel="save",
        ),
    ] = defalut_output,
    base_url: Annotated[
        Optional[str],
        Option(
            "-b",
            "--base-url",
            help="base url, if given, 'host', 'port' and 'https' are ignored.",
            envvar="AAA1111_BASE_URL",
            rich_help_panel="api",
        ),
    ] = None,
    host: Annotated[str, Option("-h", "--host", rich_help_panel="api")] = "127.0.0.1",
    port: Annotated[int, Option("-p", "--port", rich_help_panel="api")] = 7860,
    https: Annotated[bool, Option(rich_help_panel="api")] = False,
    save_ext: Annotated[
        str, Option("-e", "--save-ext", rich_help_panel="save")
    ] = "png",
    quality: Annotated[int, Option("-q", "--quality", rich_help_panel="save")] = 95,
    lossless: Annotated[bool, Option(rich_help_panel="save")] = True,
):
    _inner(
        params,
        save_dir,
        base_url,
        host,
        port,
        https,
        save_ext,
        quality,
        lossless,
        task="img2img",
    )


def _inner(
    params: List[Path],
    save_dir: Path,
    base_url: Optional[str],
    host: str,
    port: int,
    https: bool,
    save_ext: str,
    quality: int,
    lossless: bool,
    *,
    task: str = "txt2img",
):
    client = AAA1111(host=host, port=port, base_url=base_url, https=https)
    save_dir.mkdir(parents=True, exist_ok=True)
    params = filter_paths(params)
    length = len(params)

    progress = pg.Progress(
        pg.SpinnerColumn(),
        pg.TextColumn("[progress.description]{task.description}"),
        pg.BarColumn(),
        pg.TimeElapsedColumn(),
        "/",
        pg.TimeRemainingColumn(),
        pg.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    pg_task = progress.add_task(task, total=length)

    with Live(progress) as live:
        for i in range(length):
            payload = load_from_file(params[i])
            panel = Panel(
                Syntax(format_payload(payload), "yaml", theme="ansi_dark"),
                title=f"{task} [green]{i + 1}/{length}[/green]",
            )
            live.update(Group(progress, panel))

            if task == "txt2img":
                resp = client.txt2img(payload)
            elif task == "img2img":
                resp = client.img2img(payload)
            else:
                msg = f"Unknown task: {task}"
                raise ValueError(msg)

            for j, image in enumerate(resp.images):
                infotexts = resp.info.get("infotexts", [])
                if infotexts:
                    j %= len(infotexts)
                    infotext = infotexts[j]
                else:
                    infotext = None

                save_image(image, save_dir, infotext, save_ext, quality, lossless)

            progress.update(pg_task, advance=1)
            live.refresh()


def format_payload(payload: Dict[str, Any]) -> str:
    stream = io.StringIO()
    YAML().dump(payload, stream)
    return stream.getvalue().strip()


def filter_paths(paths: List[Path]) -> List[Path]:
    return [p for p in paths if p.is_file() and p.suffix.lower() in FILE_EXT]


if __name__ == "__main__":
    app_txt2img()
