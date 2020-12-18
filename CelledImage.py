from typing import Tuple, Union

from PIL import Image

class CelledImage:
    def __init__(
        self, fp: Union[str, Image.Image], cells: Tuple[int, int]
    ):
        if isinstance(fp, str):
            im = Image.open(fp)
            self.im = im.copy()
            im.close()
        elif isinstance(fp, Image.Image):
            self.im = fp.copy()
        else:
            raise TypeError
        self.cells = cells

        size = self.im.size
        self.w = int(round(size[0] / cells[0]))
        self.h = int(round(size[1] / cells[1]))

    def _get_box(self, x, y):
        if x >= self.cells[0]:
            raise IndexError("index out of range")
        while x < 0:
            x += self.cells[0]
        if y >= self.cells[1]:
            raise IndexError("index out of range")
        while y < 0:
            y += self.cells[1]

        u = self.w * x
        u_prime = min(self.im.size[0] - 1, u + self.w)
        v = self.h * y
        v_prime = min(self.im.size[1] - 1, v + self.h)

        return (u, v, u_prime, v_prime)

    def __getitem__(self, xy: Tuple[int, int]):
        assert len(xy) == 2
        x, y = xy
        box = self._get_box(x, y)
        return self.im.crop(box)

    def __setitem__(self, xy: Tuple[int, int], cell: Image.Image):
        assert len(xy) == 2
        x, y = xy
        box = self._get_box(x, y)
        sx = box[2] - box[0]
        sy = box[3] - box[1]
        self.im.paste(cell.resize((sx, sy), Image.ANTIALIAS), box)

    def show(self, title=None, command=None):
        self.im.show(title=title, command=command)

    def save(self, fp, format=None, **params):
        self.im.save(fp=fp, format=format, **params)

def open(fp: str, cells: Tuple[int, int]) -> CelledImage:
    return CelledImage(fp, cells)

def new(mode, size, cells, color=0):
    newim = Image.new(mode, size, color)
    return CelledImage(newim, cells)
