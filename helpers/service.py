import subprocess
import time


class ServiceHelper:
    def __init__(self, host: str, port: str, exec_path: str, bin_path: str):
        self.exec_path = exec_path
        self.bin_path = bin_path
        self.host = host
        self.port = port
        self.process: subprocess.Popen | None = None

    def start(self) -> subprocess.Popen:
        command = [self.bin_path, self.host, self.port]
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.exec_path,
            text=True,
        )
        # Make sure process is running
        # TODO: add better wait mechanism
        time.sleep(0.01)
        assert self.process.poll() is None
        return self.process

    def stop(self) -> subprocess.Popen:
        try:
            self.process.terminate()
            self.process.wait(0.5)
        except subprocess.TimeoutExpired:
            self.process.kill()
        return self.process

    def restart(self) -> subprocess.Popen:
        self.stop()
        self.start()

    def get_logs(self):
        pass
