import PIL
import numpy as np


@dataclass
class ImageProcessor:
    """For future development: use `input_mask`
    """
    image_file: BytesIO

    def get_image_mask(self, file):
        return np.array(
            PIL.Image.open(file))

    async def prepare_image_mask(self):
        self.image_mask = self.get_image_mask(
            self.image_file.file)
