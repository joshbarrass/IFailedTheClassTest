# IFailedTheClassTest

A letter rearrangement tool

-----------------------------

IFailedTheClassTest is a tool designed for rearranging and mutating
letters in an image to spell out a new word. Letters that exist in the
original text will be prioritised, but if none can be found an attempt
will be made to mutate another letter (e.g. rotating a `p` to make a
`d`).

Currently **this can only be used via an interactive Python session!**
I hope to make a proper user interface when I get time.  Run
`rearranger.py` in your Python REPL and create a `Rearranger` class as
such:

```
r = Rearranger("/path/to/image.png", "pattern\n  of  \n  letters")
```

The pattern should be replaced with the arrangement of letters in the
image. Any blank cells in the image should be replaced with a space,
and the lines should be padded with spaces so that the size of each
cell can be determined properly.

Once an image and pattern has been loaded, the pattern can be saved
with the image. The file format used should be either `.zip` or
`.fuck`. Use:

```
r.save_pattern("/path/to/image.zip")
# alternatively
r.save_pattern("/path/to/image.fuck")
```

This new file can then be loaded without needing to specify a pattern.

In order to use the image to create new text, use the
`Rearranger.rearrange` function:

```
newim = r.rearrange("new text")
```

The image returned is a `PIL.Image`, which can be saved with
`Image.save`.

```
newim.save("/path/to/newimage.png")
# or it can be previewed directly
newim.show()
```
