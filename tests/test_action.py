from aaa1111 import AAA1111


class TestAction:
    api = AAA1111(username="aaa1111", password="test")

    def test_refresh_checkpoints(self):
        self.api.refresh_checkpoints()

    def test_unload_checkpoint(self):
        self.api.unload_checkpoint()

    def test_reload_checkpoint(self):
        self.api.reload_checkpoint()
