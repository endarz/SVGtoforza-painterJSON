# SVGtoforza-painterJSON
A very simple Python script for parsing pixel art SVGs and turning them into forza-painter recognizable JSON files. Simple as.

# How to Use
Prerequisites: [Python 3](https://www.python.org/) and an understanding of forza-painter.
1. Download `SVGtoForzaPainterJSON.py` from this repository and place it somewhere accessible (your Desktop, for example).
2. Create or obtain an `.svg` file containing `rect` objects, each one having a width and height no greater than 1.
A valid example:
```
<rect x="33" y="0" width="1" height="1" fill="#5DD498" />
```
A valid `.svg` can be obtained using Asesprite or any tool that exports each pixel as a `rect`. **Plain SVGs, Inkscape SVGs, Affinity Designer SVGs or other tools WILL NOT WORK.** See `example.svg` in the repository for a valid file.

3. Run the script. Either use the command line or run it like an executable.
4. Provide it a path to a file when asked (or provide it through command line arguments).
5. After running, a new `.json` file can be found in the same location as the script itself. Use as directed by forza-painter.

It is the user's responsibility to perform simple image optimizations, such as restricting color use to a limited palette or providing images with simple or transparent backgrounds, if they expect this tool to work properly.

# Overview
### The Why
This project was conceived and written in a day when I felt inspired to make a livery in Forza Horizon 5 using pixel art. Seeing that the two options for me were to make it by hand or to automate it using the marvellous tool [forza-painter](https://github.com/forza-painter/forza-painter), I quickly chose the latter. There was was one caveat, however: **forza-painter uses circles, not squares.** I did not want to simply *fake* the appearance of pixels, either; I wanted scalable, *real* pixel art for vinyl groups, and forza-painter alone would just not cut it.

### The How
Thinking in terms of "scalable" led right away to the `.svg` format: Scalable Vector Graphics. Incredibly simple and close to what Forza has anyways, but I still needed the art. Moreso, I needed software which would export each pixel's information as a square in an `.svg`. Further thinking led me to another feature of forza-painter: the ability to dump vinyl groups made in-game as `.json` files. Users can share these files with others out in the wild and import them through forza-painter. Thus, the connection was made: if I could get an ideal `.svg` where each pixel is a shape, I could convert it into a `.json` that forza-painter could import into Forza.

Using [Asesprite](https://www.aseprite.org/), one can export pixel art as an "ideal `.svg`." **Pixel scale must be set to one (1).** From there, opening the `.svg` in the script included in this repository parses the `.svg` and merges neighboring pixels of the same color into rectangles, greatly reducing the layer count. Thes script creates a `.json` file containing shape information as output. Each shape's position and scale is adjusted to the units used in the Forza vinyl editor. It Just Works™️.

# Future Ideas
~~- Rectangle optimization. Thinking of ways to reduce the number of same-colored pixels by making some pixels double the size, and so on.~~ Added in Update #2.

# Acknowledgements
- [forza-painter](https://github.com/forza-painter/forza-painter), duh!
- [Igara Studio S.A.](https://www.aseprite.org/) for making the greatest pixel art software in all of the civilized world.
