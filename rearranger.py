import copy
import os
import random
import tempfile
import zipfile

import CelledImage

PATTERN_FILE = "pattern.txt"
IMAGE_NAME = "image"

class NotEnoughLettersError(Exception):
    pass

class Rearranger:
    """Class for handling the automated rearranging of letters in an image."""
    def __init__(self, fp, pattern=None):
        self.im = None
        self.pattern = None

        _, ext = os.path.splitext(fp)
        if ext.lower() in [".zip", ".fuck"]:
            # "custom" format that packages everything in one
            self.load_zip(fp)
        else:
            if pattern is None:
                raise ValueError(
                    "Can only use 'None' pattern if file contains a pattern"
                )
            self.load_other(fp, pattern)

    def load_zip(self, fp):
        """Load an image and pattern from a zip file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(fp, "r") as z:
                files = z.namelist()
                if not PATTERN_FILE in files:
                    raise TypeError("file is missing pattern")

                image_ext = None
                for f in files:
                    n, x = os.path.splitext(f)
                    if n == IMAGE_NAME:
                        image_ext = x
                        break

                if image_ext is None:
                    raise TypeError("file is missing image")

                extracted_pattern = z.extract(PATTERN_FILE, tmpdir)
                extracted_image = z.extract(
                    IMAGE_NAME + image_ext, tmpdir
                )

            with open(extracted_pattern) as f:
                self.pattern = f.read()
            self.im = CelledImage.open(
                extracted_image, self.pattern_size
            )
        self.process_pattern()

    def load_other(self, fp, pattern):
        """Load and store an image and pattern separately."""
        self.pattern = pattern
        self.im = CelledImage.open(fp, self.pattern_size)
        self.process_pattern()

    @property
    def pattern_size(self):
        lines = self.pattern.splitlines()
        return (max([len(line) for line in lines]), len(lines))

    def process_pattern(self):
        """Turn the pattern into a letter dictionary. Stored as self.patterndict"""
        # ensure lines are all the same length
        lines = pad_lines(self.pattern)

        self.patterndict = {}
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                char = lines[y][x]
                if char not in self.patterndict:
                    self.patterndict[char] = []
                self.patterndict[char].append((x, y))

    def save_pattern(self, fp, image_ext=".png"):
        """Save an image together with it's pattern in a zip file"""
        name, ext = os.path.splitext(fp)
        if ext == "":
            ext = ".fuck"

        with tempfile.TemporaryDirectory() as tmpdir:
            self.im.save(os.path.join(tmpdir, IMAGE_NAME + image_ext))
            with open(os.path.join(tmpdir, PATTERN_FILE), "w") as f:
                f.write(self.pattern)
            with zipfile.ZipFile(name + ext, "w") as z:
                z.write(
                    os.path.join(tmpdir, IMAGE_NAME + image_ext),
                    IMAGE_NAME + image_ext
                )
                z.write(
                    os.path.join(tmpdir, PATTERN_FILE), PATTERN_FILE
                )

    def rearrange(
        self,
        target,
        allow_duplicates=False,
        space=None,
        unlimited_spaces=True
    ):
        """Rearrange the letters into the desired pattern.

If allow_duplicates is True, letters can be reused. Implies unlimited_spaces.
If space is set to a coordinate (x,y), this coordinate will be used for
all spaces. Implies unlimited_spaces.
If unlimited_spaces is True, an unlimited number of spaces can be used.
"""
        if isinstance(space, tuple):
            unlimited_spaces = True
        else:
            space = None
        if allow_duplicates:
            unlimited_spaces = True

        patterndict = copy.deepcopy(self.patterndict)
        lines = pad_lines(target)
        cells = (len(lines[0]), len(lines))
        newim = CelledImage.new(
            self.im.im.mode,
            (self.im.w * cells[0], self.im.h * cells[1]), cells
        )

        for y in range(len(lines)):
            for x in range(len(lines[0])):
                char = lines[y][x]
                mutator = None
                # make sure the character is available
                if char not in patterndict or len(
                    patterndict[char]
                ) == 0:
                    # check if the opposite case is available
                    if char.swapcase() in patterndict and len(
                        patterndict[char.swapcase()]
                    ) > 0:
                        char = char.swapcase()
                    else:
                        raise NotEnoughLettersError(
                            "No {} remaining.".format(repr(char))
                        )

                if char == " " and space is not None:
                    index = space
                else:
                    index = random.choice(patterndict[char])
                if (char == " " and not unlimited_spaces
                    ) or (char != " " and not allow_duplicates):
                    patterndict[char].remove(index)

                newcell = self.im[index[0], index[1]]
                if mutator is not None:
                    newcell = mutator(newcell)
                newim[x, y] = newcell
        return newim

    def mutate_letter(self, char):
        """If a letter is unavailable, attempt to produce it through a mutation

If a mutation can be done, will return the character and a mutation function.

Mutation functions will take an image in and return a new image."""
        pass

def pad_lines(string):
    lines = string.splitlines()
    required_length = max([len(line) for line in lines])
    for i, line in enumerate(lines):
        while len(lines[i]) < required_length:
            lines[i] += " "
    return lines
