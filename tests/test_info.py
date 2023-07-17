from pathlib import Path

from PIL import Image

from aaa1111 import AAA1111

image_png = "tests/image/test1.png"
image_webp = "tests/image/test2.webp"
image_jpg = "tests/image/test3.jpg"


class TestInfo:
    api = AAA1111(username="aaa1111", password="test")

    def test_png_info1(self):
        resp = self.api.png_info(image_png)
        assert resp.info.startswith("masterpiece")
        assert "parameters" in resp.items

    def test_png_info2(self):
        resp = self.api.png_info(image_webp)
        assert not resp.info
        assert "parameters" in resp.items

    def test_png_info3(self):
        resp = self.api.png_info(Path(image_jpg))
        assert not resp.info
        assert "parameters" in resp.items

    def test_png_info4(self):
        pil = Image.open(image_png)
        resp = self.api.png_info(pil)
        assert resp.info.startswith("masterpiece")
        assert "parameters" in resp.items

    def test_png_info5(self):
        pil = Image.open(image_png).convert("L")
        resp = self.api.png_info(pil)
        assert resp.info.startswith("masterpiece")
        assert "parameters" in resp.items

    def test_progress(self):
        resp = self.api.progress()
        assert resp.current_image is None
        assert "job_count" in resp.state

    def test_cmd_flags(self):
        resp = self.api.cmd_flags()
        assert "api" in resp

    def test_samplers(self):
        resp = self.api.samplers()
        assert resp
        assert "Euler" in [item.name for item in resp]

    def test_upscalers(self):
        resp = self.api.upscalers()
        assert resp
        assert "Nearest" in [item.name for item in resp]

    def test_latent_upscale_modes(self):
        resp = self.api.latent_upscale_modes()
        assert resp
        assert "Latent (bicubic)" in [item.name for item in resp]

    def test_sd_models(self):
        resp = self.api.sd_models()
        assert resp
        assert any(item.model_name.startswith("Counterfeit") for item in resp)
        assert "5998292c04" in [item.hash for item in resp]

    def test_sd_vae(self):
        resp = self.api.sd_vae()
        assert resp
        assert any(item.model_name.startswith("kl-f8-anime2") for item in resp)

    def test_hypernetworks(self):
        resp = self.api.hypernetworks()
        assert not resp

    def test_face_restorers(self):
        resp = self.api.face_restorers()
        assert resp
        assert "CodeFormer" in [item.name for item in resp]

    def test_realesrgan_models(self):
        resp = self.api.realesrgan_models()
        assert resp
        assert any(item.name.startswith("R-ESRGAN") for item in resp)

    def test_prompt_styles(self):
        resp = self.api.prompt_styles()
        assert resp
        assert any(item.name.startswith("default") for item in resp)

    def test_embeddings(self):
        resp = self.api.embeddings()
        assert resp.loaded
        assert any(item.startswith("EasyNegative") for item in resp.loaded)

    def test_memory(self):
        resp = self.api.memory()
        assert resp.cuda
        assert resp.ram

    def test_scripts(self):
        resp = self.api.scripts()
        assert resp.txt2img
        assert resp.img2img
        assert any("adetailer" in item for item in resp.txt2img)
        assert any("controlnet" in item for item in resp.img2img)

    def test_script_info(self):
        resp = self.api.script_info()
        assert resp
        assert any(item.is_alwayson for item in resp)
        assert any(item.name == "controlnet" for item in resp)

    def test_loras(self):
        resp = self.api.loras()
        assert resp
        assert any(item.name.startswith("add_detail") for item in resp)
