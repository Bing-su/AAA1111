# AAA1111

An Api for Automatic1111

## 설치

```
pip install aaa1111
```

pip를 통하여 설치할 수 있습니다.


## 사용법

### 1. CLI
aaa1111을 설치하면, `txt2img`, `img2img` 2가지 cli 명령어를 사용할 수 있습니다.

```sh
❯ txt2img --help

 Usage: txt2img [OPTIONS] PARAMS...

╭─ api ───────────────────────────────────────────────────────────────────────────╮
│ *    params      PARAMS...  Path to params files. .toml, .yaml, .yml, .json,    │
│                             .json5 available. others will be ignored.           │
│                             [required]                                          │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershel  Install completion for    │
│                             l|pwsh]                   the specified shell.      │
│                                                       [default: None]           │
│ --show-completion           [bash|zsh|fish|powershel  Show completion for the   │
│                             l|pwsh]                   specified shell, to copy  │
│                                                       it or customize the       │
│                                                       installation.             │
│                                                       [default: None]           │
│ --help                                                Show this message and     │
│                                                       exit.                     │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ save ──────────────────────────────────────────────────────────────────────────╮
│ --save-dir  -d                   DIRECTORY  Path to save directory.             │
│                                             [env var: AAA1111_SAVE_DIR]         │
│                                             [default: output]                   │
│ --save-ext  -e                   TEXT       [default: png]                      │
│ --quality   -q                   INTEGER    [default: 95]                       │
│ --lossless      --no-lossless               [default: lossless]                 │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ api ───────────────────────────────────────────────────────────────────────────╮
│ --base-url  -b                TEXT     base url, if given, 'host', 'port' and   │
│                                        'https' are ignored.                     │
│                                        [env var: AAA1111_BASE_URL]              │
│                                        [default: None]                          │
│ --host      -h                TEXT     [default: 127.0.0.1]                     │
│ --port      -p                INTEGER  [default: 7860]                          │
│ --https         --no-https             [default: no-https]                      │
╰─────────────────────────────────────────────────────────────────────────────────╯
```

`--api`옵션을 활성화한채 실행중인 webui가 필요합니다.


명령어 뒤에 입력 파라미터를 담은 파일의 경로를 1개 또는 그 이상 지정해주는 것으로 이미지를 생성합니다.

```sh
# 하나의 파일만 사용
txt2img examples/txt1.yaml
```

```sh
# glob 패턴
txt2img examples/txt*
```

지원하지 않는 확장자를 가진 파일은 무시됩니다.

`.toml, .yaml, .yml, .json, .json5` 5가지 확장을 지원하며, 파일은 하나의 python dict를 반환하도록 작성되어야 합니다.

예시: yaml

[`ruamel.yaml`](https://yaml.readthedocs.io/en/latest/overview.html)을 사용중이므로 기본적으로 yaml 1.2를 사용합니다.

```yaml
prompt: masterpiece, best quality, 1girl
negative_prompt: (worst quality, low quality:1.1), text, title, logo, signature, (EasyNegativeV2:0.7), (negative_hand-neg:0.7)
sampler_name: DPM++ 2M Karras
batch_size: 2
n_iter: 1
cfg_scale: 7.5
width: 512
height: 768
steps: 20

override_settings:
  CLIP_stop_at_last_layers: 2

alwayson_scripts:
  Simple wildcards:
    args: [] # Simple wildcards doesn't accept arguments
```

예시: toml

```toml
prompt = "masterpiece, best quality, 1girl"
negative_prompt = "(worst quality, low quality:1.1), text, title, logo, signature, (EasyNegativeV2:0.7), (negative_hand-neg:0.7)"
sampler_name = "DPM++ 2M Karras"
batch_size = 2
n_iter = 1
cfg_scale = 7.5
width = 512
height = 768
steps = 20

[override_settings]
CLIP_stop_at_last_layers = 2

[alwayson_scripts."Simple wildcards"]
args = []  # Simple wildcards doesn't accept arguments
```

예시: json5

```json5
// json5 example with comments

{
    "prompt": "masterpiece, best quality, 1girl",
    "negative_prompt": "(worst quality, low quality:1.1), text, title, logo, signature, (EasyNegativeV2:0.7), (negative_hand-neg:0.7)",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 2,
    "n_iter": 1,
    "cfg_scale": 7.5,
    "width": 512,
    "height": 768,
    "steps": 20,

    "override_settings": {
        "CLIP_stop_at_last_layers": 2
    },

    "alwayson_scripts": {
        "Simple wildcards": {
            "args": [],  // Simple wildcards doesn't accept arguments
        },
    },  // Trailing comma available
}
```

### 2. python

기본 사용방법

```py
from aaa1111 import AAA1111
from aaa1111.types import TXT2IMG, IMG2IMG
from aaa1111.types.extension import SimpleWildcards

api = AAA1111()
params = TXT2IMG(
    prompt="masterpiece, best quality, 1girl, __woman_clothes__, __places__",
    negative_prompt="(worst quality, low quality:1.1), text, title, logo, signature, (EasyNegativeV2:0.7), (negative_hand-neg:0.7)",
    sampler_name="DPM++ 2M Karras",
    batch_size=2,
    n_iter=1,
    cfg_scale=7.5,
    width=512,
    height=768,
    steps=20,
    override_settings={"CLIP_stop_at_last_layers": 2},
    alwayson_scripts=[SimpleWildcards()]
)

resp = api.txt2img(txt2img)
images = resp.images
```

대신 설정 파일 경로를 넣을 수도 있습니다.

```py
from aaa1111 import AAA1111

api = AAA1111()
resp = api.txt2img("examples/txt1.yaml")
images = resp.images
```

async 호출도 지원합니다.

```py
import asyncio
from aaa1111 import AAA1111

async def gen():
    api = AAA1111()
    resp = await api.atxt2img("examples/txt1.yaml")
    return resp.images

images = asyncio.run(gen())
```
