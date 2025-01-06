# SVG to ForzaPainterJSON -
# A Python script designed to convert pixel art into Forza Horizon vinyl groups
# via forza-painter.
#
# Created by endarz
# Last edit: 1/6/2025
# Licenced under MIT License.

import sys
import os.path

# Helper methods.

# For a rect SVG string, returns its x-value.
def getRectXValue(str):
    # Some unhinged, absolutely mental string hacking going on here!!!
    return int(str[str.find('"') + 1 : str.find('" y="')])

# For a rect SVG string, returns its y-value.
def getRectYValue(str):
    return int(str[str.find('y="') + 3 : str.find('" w')])

# For a rect SVG string, returns its width value.
def getRectWidth(str):
    return int(str[str.find('width="') + 7 : str.find('" h')])

# For a rect SVG string, returns its height value.
def getRectHeight(str):
    return int(str[str.find('height="') + 8 : str.find('" f')])

# For a rect SVG string, returns its fill color in hexadecimal.
def getRectColor(str):
    return str[str.find('fill="#') + 7 : str.find('" /')]

# For a rect SVG string, return a list representing a rect object.
def getRectAsList(str):
    rect_list = [getRectXValue(str),
            getRectYValue(str),
            getRectWidth(str),
            getRectHeight(str),
            getRectColor(str)]
    return rect_list

# For a rect as a list, convert it into a string of SVG.
def svg(rect_list):
    svg_str = '<rect ' + 'x="' + str(rect_list[0])
    svg_str += '" y="' + str(rect_list[1])
    svg_str += '" width="' + str(rect_list[2])
    svg_str += '" height="' + str(rect_list[3])
    svg_str += '" fill="#' + rect_list[4]
    svg_str += '" />'

    return svg_str


# Main method.

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


# A valid SVG file has been given at this point. Next is the optimization phase.

# Optimization phase.

# Open the SVG and obtain its lines.
svg = open(file_path, 'r')
svg_lines = svg.readlines()
svg_lines = svg_lines.reverse() # Reverse the list so that the list can be used like a stack.
optimized_lines = []            # Optimized lines get appended here.

# Choose what method to use for optimization.
# Set to 0 to combine by row (horizontal optimization).
# Set to 1 to combine by column (vertical optimization).
method_of_opt = 0

match method_of_opt:
    case 0:
        # Horizontal optimization.

            # Pop two SVG lines from the list.
            line_1 = svg_lines.pop()    # "Primary line." line_2 merges with it if possible.
            line_2 = svg_lines.pop()    # "Secondary line." A potentially redundant line.

            while not line_2 == '</svg>':
                # Get the y-value and color for both lines.
                line_1_y = getRectYValue(line_1)
                line_2_y = getRectYValue(line_2)
                line_1_color = getRectColor(line_1)
                line_2_color = getRectColor(line_2)

                # If two rects share both a y-value AND a fill color, combine them.
                if line_1_y == line_2_y and line_1_color == line_2_color:
                    line_1_values = getRectAsList(line_1)   # Get line_1's values.
                    line_1_values[2] += 1                   # Increment width value by one.
                    line_1 = svg(line_1_values)             # Convert the values to an SVG string.
                    line_2 = svg_lines.pop()                # Get a new secondary line.
                else:
                    optimized_lines.append(line_1)          # Append line_1. It cannot merge with line_2.
                    line_1 = line_2                         # line_2 becomes the "primary line"
                    line_2 = svg_lines.pop()                # Get a new secondary line.
        
    case 1:
        # Vertical pass.
        # If two rects share both an x-value AND a fill color,
        # combine them.
        pass


# Isolate the rectangles from the SVG.
svg_lines = svg_lines[2:-1]


# Conversion to JSON phase.

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
for line in svg_lines:
    # Get the x, y and hexadecimal color code from the rect.
    x = getRectXValue(line)
    y = getRectYValue(line)
    hex_color = getRectColor(line)

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