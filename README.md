# SVGtoforza-painterJSON
A very simple Python script for parsing pixel art SVGs and turning them into forza-painter recognizable JSON files. Simple as.

![image](https://github.com/user-attachments/assets/0969c068-3251-4bb4-8519-71898d303ed2)

# How to Use
Prerequisites: [Python 3](https://www.python.org/) and an understanding of forza-painter.
1. Download `SVGtoForzaPainterJSON.py` from this repository and place it somewhere accessible (your Desktop, for example).
2. Create or obtain an `.svg` file *containing rectangles imitating pixels.*
3. Run the script. Either use the command line or run it like an executable.
4. Provide it a path to a file when asked (or provide it through command line arguments).
5. After running, a new `.json` file can be found in the same location as the script itself. Use as directed by forza-painter.

# Overview
### The Why
This project was conceived and written in a day when I felt inspired to make a livery in Forza Horizon 5 using pixel art. Seeing that the two options for me were to make it by hand or to automate it using the marvellous tool [forza-painter](https://github.com/forza-painter/forza-painter), I quickly chose the latter. There was was one caveat, however: **forza-painter uses circles, not squares.** I did not want to simply *fake* the appearance of pixels, either; I wanted scalable, *real* pixel art for vinyl groups, and forza-painter alone would just not cut it.

### The How
Thinking in terms of "scalable" led right away to the `.svg` format: Scalable Vector Graphics. Incredibly simple and close to what Forza has anyways, but I still needed the art. Moreso, I needed software which would export each pixel's information as a square in an `.svg`. Further thinking led me to another feature of forza-painter: the ability to dump vinyl groups made in-game as `.json` files. Users can share these files with others out in the wild and import them through forza-painter. Thus, the connection was made: if I could get an ideal `.svg` where each pixel is a shape, I could convert it into a `.json` that forza-painter could import into Forza.

Using [Asesprite](https://www.aseprite.org/), one can export pixel art as an "ideal `.svg`." **Pixel scale must be set to one (1).** From there, opening the `.svg` in the script included in this repository parses the `.svg` and creates a `.json` file containing the pixel information. Each pixel's position is adjusted to compensate for scaling in Forza. It Just Works™️.

# Future Ideas
- Rectangle optimization. Thinking of ways to reduce the number of same-colored pixels by making some pixels double the size, and so on.
- Batch script alternative.

# Acknowledgements
- [forza-painter](https://github.com/forza-painter/forza-painter), duh!
- [Igara Studio S.A.](https://www.aseprite.org/) for making the greatest pixel art software in all of the civilized world.
- [Mina Cream](https://x.com/MinaCreamu) for the art used in the screenshot.
