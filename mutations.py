from PIL import Image

# MUTATIONS lists ways of mutating a letter into another letter.  The
# first key is the target letter, and MUTATIONS[target] will return a
# new dict. The second key is the required
# letter. MUTATIONS[target][required] returns the mutation function
# needed to turn the required letter into the target letter.
MUTATIONS = {
    "d": {
        "P":
            lambda im: im.transpose(Image.ROTATE_180),
        "p":
            lambda im: im.transpose(Image.ROTATE_180),
        "b":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "q":
            lambda im: im.transpose(Image.ROTATE_180).
            transpose(Image.FLIP_LEFT_RIGHT),
    },
    "P": {
        "d":
            lambda im: im.transpose(Image.ROTATE_180),
        "b":
            lambda im: im.transpose(Image.ROTATE_180).
            transpose(Image.FLIP_LEFT_RIGHT),
        "q":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
    },
    "b": {
        "d":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "p":
            lambda im: im.transpose(Image.ROTATE_180).
            transpose(Image.FLIP_LEFT_RIGHT),
        "P":
            lambda im: im.transpose(Image.ROTATE_180).
            transpose(Image.FLIP_LEFT_RIGHT),
        "q":
            lambda im: im.transpose(Image.ROTATE_180),
    },
    "q": {
        "p":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "P":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "d":
            lambda im: im.transpose(Image.ROTATE_180).
            transpose(Image.FLIP_LEFT_RIGHT),
        "b":
            lambda im: im.transpose(Image.ROTATE_180),
    },
    #
    "U": {
        "C": lambda im: im.rotate(90, Image.BILINEAR),
        "c": lambda im: im.rotate(90, Image.BILINEAR),
    },
    "C": {
        "U": lambda im: im.rotate(-90, Image.BILINEAR),
        "u": lambda im: im.rotate(-90, Image.BILINEAR),
    },
    #
    "M": {
        "w": lambda im: im.transpose(Image.ROTATE_180),
        "W": lambda im: im.transpose(Image.ROTATE_180),
    },
    "W": {
        "M": lambda im: im.transpose(Image.ROTATE_180),
        "m": lambda im: im.transpose(Image.ROTATE_180),
    },
    "S": {
        "z": lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "Z": lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
    },
    "Z": {
        "s": lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
        "S": lambda im: im.transpose(Image.FLIP_LEFT_RIGHT),
    },
    #
    "r": {
        "L":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT).
            transpose(Image.ROTATE_180),
    },
    "L": {
        "r":
            lambda im: im.transpose(Image.FLIP_LEFT_RIGHT).
            transpose(Image.ROTATE_180),
    },
}
