# SVG to ForzaPainterJSON -
# A Python script designed to convert pixel art into Forza Horizon vinyl groups
# via forza-painter.
#
# Created by endarz
# Last edit: 1/4/2025
# Licenced under MIT License.

import sys
import os.path

# Get the path to a file.
# If a path is not provided through args, ask the user for a path.
if len(sys.argv) < 2:
    file_path = input('Please provide the path to an SVG to be converted.\n'
                      + 'Paths may contain quotation marks.\n\n'
                      + 'Path: ')
else:
    file_path = sys.argv[1]

# If the path begins/ends quotation marks, remove them. (FUCK YOU, Windows 11.)
if file_path.startswith('"') and file_path.endswith('"'):
    file_path = file_path.replace('"', '')

# Check the given path for validity.
# Is it a file?
if not os.path.isfile(file_path):
    print('ERROR -- ' +
          file_path + ' is not a path to a file. Check the path and run again.')
    exit()

# Is it an SVG?
if not file_path.endswith('.svg'):
    print('ERROR -- ' +
          file_path + ' is not an .svg file. Either provide an .svg or give the file an extension.')
    exit()


# A valid SVG file has been given at this point.
# Prepare for parsing.

# Open the SVG and obtain its lines.
svg = open(file_path, 'r')
svg_lines = svg.readlines()
svg.close()

# Isolate the rectangles from the SVG.
svg_lines = svg_lines[2:-1]

# Optimization Phase

# Create a working file to perform destructive optimizations in.


# Choose what method to use for optimization.
# Set to 0 to combine by row (horizontal optimization).
# Set to 1 to combine by column (vertical optimization).
optimizer = 0

if optimizer == 0:
    # Placeholder.
    pass
if optimizer == 1:
    # Placeholder.
    pass


# Create the result JSON file.
result = open(os.path.basename(file_path) + '.json', 'w')

# Prepare values for creating the JSON.
header = '{"shapes":\n['
trailer = '\n]}'
type = 1048677                  # The "shape ID." This value is a square.
data = [0, 0, 0, 0, 0, 0, 0]    # X position; Y position; scale X; scale Y; rotation; and two other values that I don't know.
color = [255, 255, 255, 255]    # Red, Green, Blue and Alpha values
score = 0.8008135               # Shape accuracy; used by forza-painter. :]


# Begin the parsing process.
result.write(header)

# Parse each rect in the SVG file. Turn it into a JSON line.
i = 1
for rect in svg_lines:
    # Get the x, y and hexadecimal color code from the rect.
    x = rect[rect.find('"') + 1 : rect.find('" y="')]   # Some unhinged, absolutely mental string hacking going on here!!!
    y = rect[rect.find('y="') + 3 : rect.find('" w')]
    hex_color = rect[rect.find('fill="') + 7 : rect.find('" /')]

    # Adjust the x and y values so the squares are seamless at 0.01 scale.
    # Put the values in their respective places in the data list.
    x = float(x) * 1.28
    data[0] = x
    y = float(y) * 1.28
    data[1] = y

    # TODO: Change this to support values >0.01 for horizontal and vertical runs.
    data[2] = 0.01
    data[3] = 0.01

    # Convert hex color to RGB values.
    color[0] = int(hex_color[0:2], 16)
    color[1] = int(hex_color[2:4], 16)
    color[2] = int(hex_color[4:6], 16)

    # Write the rectangle into the JSON
    result.write('{')
    result.write('"type":' + str(type) + ',')
    result.write('"data":' + str(data).replace(' ', '') + ',')
    result.write('"color":' + str(color).replace(' ', '') + ',')
    result.write('"score":' + str(score))
    result.write('}')
    # Decide if the end of the JSON has been reached.
    if i < len(svg_lines):
        result.write(',\n')
    i += 1


# End the parsing process.
result.write(trailer)
result.close()

print('Done! The result file has been placed in this script\'s directory.')