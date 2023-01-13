#!/usr/bin/env python
from io import BytesIO

from time import sleep
from PIL import Image
import numpy as np

# To test program locally without RPI or PiCamera
# comment the next line
from picamera import PiCamera


# rename DummyPiCamera to PiCamera
class DummyPiCamera:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def still_capture_sync(self, resize: tuple[int, int], warmup_time: float = 0.0, save: str = None):
        return Image.fromarray(np.zeros(resize))


class Camera:

    def __init__(self):
        self._pi = None

    def __enter__(self):
        return self.get_backend()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.get_backend().__exit__(exc_type, exc_val, exc_tb)

    def get_backend(self):
        if self._pi is None:
            self._pi = PiCamera()

        return self._pi

    def still_capture_sync(self, resize: tuple[int, int], warmup_time: float = 0.0, save: str = None):
        backend = self.get_backend()

        stream = BytesIO()

        if warmup_time > 0.0:
            backend.start_preview()
            sleep(warmup_time)
            backend.stop_preview()

        backend.capture(stream, resize=resize)

        stream.seek(0)
        image = Image.open(stream)

        if save is not None:
            image.save(save)

        return image
