import os
import subprocess
import time

import pytest
from dotenv import load_dotenv

load_dotenv()
python = os.environ["AAA1111_PYTHON"]
webui_dir = os.environ["AAA1111_WEBUI"]
sleep_sec = int(os.getenv("AAA1111_SLEEP", 20))
cmd_args = [
    "--xformers",
    "--api",
    "--disable-nan-check",
    "--skip-install",
    "--gradio-auth",
    "aaa1111:test",
]
process = None


def pytest_sessionstart(session: pytest.Session) -> None:
    global process
    process = subprocess.Popen([python, "launch.py", *cmd_args], cwd=webui_dir)
    time.sleep(sleep_sec)


def pytest_sessionfinish(session: pytest.Session) -> None:
    global process
    if process is not None:
        process.terminate()
