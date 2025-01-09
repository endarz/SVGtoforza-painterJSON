# SVG to ForzaPainterJSON -
# A Python script designed to convert pixel art into Forza Horizon vinyl groups
# via forza-painter.
#
# Created by endarz
# Last edit: 1/6/2025
# Licenced under MIT License.

import sys
import os.path

#
# HELPER METHODS
#

# For an SVG string representing a rectangle, returns its x-value.
def getRectXValue(str):
    # Some unhinged, absolutely mental string hacking going on here!!!
    return int(str[str.find('"') + 1 : str.find('" y="')])

# For an SVG string representing a rectangle, returns its y-value.
def getRectYValue(str):
    return int(str[str.find('y="') + 3 : str.find('" w')])

# For an SVG string representing a rectangle, return its width.
# (Alias for getSVGWidth() because they do the same thing.)
def getRectWidth(str):
    return getSVGWidth(str)

# For an SVG string representing a rectangle returns its height value.
def getRectHeight(str):
    return int(str[str.find('height="') + 8 : str.find('" f')])

# For an SVG string representing a rectangle, returns its fill color in hexadecimal.
def getRectColor(str):
    return str[str.find('fill="#') + 7 : str.find('" /')]

# For an SVG string, returns its width value.
def getSVGWidth(str):
    return int(str[str.find('width="') + 7 : str.find('" h')])

# For an SVG string, returns its height value.
def getSVGHeight(str):
    return int(str[str.find('height="') + 8 : str.find('" x')])

# For an SVG string representing a rectangle, return a list representing a rect object.
def rectLineToList(str):
    rect_list = [getRectXValue(str),
            getRectYValue(str),
            getRectWidth(str),
            getRectHeight(str),
            getRectColor(str)]
    return rect_list


#
# MAIN METHOD
#

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

# Open the SVG and put its lines in a list.
svg = open(file_path, 'r')
svg_lines = []
for line in svg.readlines():
    svg_lines.append(line)
svg.close()

# Is it empty?
if len(svg_lines) == 0:
    print('ERROR -- ' +
          'The .svg given is empty and contains no lines.')
    exit(1)

# Are there any rects in the file (after omitting metadata)?
for line in svg_lines[2 : len(svg_lines) - 1]:
    if line == None:
        print('ERROR -- '
              + 'The .svg given contains no <rect> tags.')
        exit(1)
    if str(line).find('<rect') == -1:
        print('ERROR -- '
              + '\'' + str(line) + '\''
              + ' is unexpected and cannot be accepted. Was this file exported from Asesprite?')
        exit(1)
    



svg_lines.reverse() # Reverse the list of svg_lines to use it like a stack in Python.

#
# Preparation Phase
#

# Creating the pixel grid.
#
# Get the image's dimensions from the second line of metadata.
svg_lines.pop()     # Pop first line because it's redundant.

# Create a two-dimensional list to represent the pixels in the SVG.
pixel_grid = []
x = int(getSVGWidth(svg_lines[-1]))
y = int(getSVGHeight(svg_lines[-1]))
for i in range(y):
    pixel_grid.append([None] * x)

svg_lines.pop()             # Pop second line because it's no longer needed.
                            # svg_lines now contains rectangles and an ending </svg> tag.
svg_lines = svg_lines[1:]   # Remove the </svg> tag at the bottom of the stack.

# Populate the pixel grid, end to front (because the lines were reversed).
count = 0
for line in svg_lines:
    count += 1
    rect = rectLineToList(line)
    pixel_grid[rect[1]][rect[0]] = rect

#
#   Optimization Phase
#

# Choose what method to use for optimization.
# Set to 0 to combine by row (horizontal merging).
# Set to 1 to combine by column (vertical merging).
method_of_opt = 0
match method_of_opt:
    case 0:
        # Horizontal merging.
        #
        # For each row in the pixel grid, use a primary pixel and a secondary pixel.
        # Compare the secondary pixel to the primary pixel; if its color is the same
        # as the primary pixel's color, then add one to the primary pixel's width
        # and replace the secondary pixel with None in the pixel grid.
        print('Starting horizontal merging...')
        for row in pixel_grid:
            print('Starting new row.')
            for i in range(len(row)):
                print(i)
                pri_pix = row[i]
                sec_pix = row[i + 1]
                print(pri_pix)
                print(sec_pix)
                if pri_pix == None or sec_pix == None:  # If either of the pixels is a None...
                    if i == len(row) - 2:   # Edge case: if the last pixel in the row is a none, leave this row.
                        print('Last pixel in the row is None. Leaving this row...')
                        break
                    else:                   # Otherwise, go to the next iteration.
                        print('One of the pixels is None. Reiterating...')
                        continue
                # Check if the secondary pixel's color matches primary pixel's color.
                # If it does, then merge.
                if sec_pix[4] == pri_pix[4]:
                    print('Color match found, will merge.')
                else:
                    print('Color does not match, will not merge.')
                while sec_pix[4] == pri_pix[4]:
                    sys.stdout.write('Merging ')
                    sys.stdout.write(str(pri_pix))
                    sys.stdout.write(' with ')
                    sys.stdout.write(str(sec_pix))
                    print('')

                    pri_pix[2] += 1                                 # Increment primary pixel's width by one.
                    pixel_grid[pri_pix[1]][pri_pix[0]] = pri_pix    # Update primary pixel in the pixel grid.
                    pixel_grid[sec_pix[1]][sec_pix[0]] = None       # Update secondary pixel in the pixel grid.
                    row[sec_pix[0]] = None                          # Update secondary pixel in the row.

                    print('Row:')
                    print(row)
                    # Check if the last pixel in the row just got merged.
                    # If it did, then we need to leave and start a new row.
                    if sec_pix[0] == len(row) - 1:
                        print('Last pixel in the row just got merged.')
                        break
                    else:
                        print('Getting next secondary pixel...')
                        sec_pix = row[sec_pix[0] + 1]               # Get the pixel following the secondary pixel.
                        if sec_pix == None:                         # If the new secondary pixel is a None, exit the loop.
                            break
                if sec_pix == None or sec_pix[0] == len(row) - 1:
                    break
                    
        print('Horizontal merging complete.')
        print('Pixel grid:')
        for row in pixel_grid:
            print(row)
    case 1:
        pass

exit("Script completed!")




"""
optimized_lines = []    # Optimized lines get appended here.

# Choose what method to use for optimization.
# Set to 0 to combine by row (horizontal optimization).
# Set to 1 to combine by column (vertical optimization).
method_of_opt = 0
match method_of_opt:
    case 0:
        # Horizontal optimization.

            # Pop two SVG lines from the list.
            line_1 = svg_lines.pop()    # String that is the "primary line." line_2 merges with it if possible.
            line_2 = svg_lines.pop()    # String that is the "secondary line," a potentially redundant line.

            while not line_2 == '</svg>':
                # Get x values.
                line_1_x = getRectXValue(line_1)
                line_2_x = getRectXValue(line_2)
                # Get y values.
                line_1_y = getRectYValue(line_1)
                line_2_y = getRectYValue(line_2)
                # Get colors.
                line_1_color = getRectColor(line_1)
                line_2_color = getRectColor(line_2)

                count = 0
                # If the two pixels share a y-value and color, prepare to look ahead.
                if line_1_y == line_2_y and line_1_color == line_2_color:
                    count += 1
                    prev_x = line_2_x
                    line_2 = svg_lines.pop()


                    line_1_values = getRectAsList(line_1)   # Get line_1's values.
                    line_1_values[2] +=                # Increment width value by count.
                    # Create a new SVG string from the new values.
                    # I tried to make this its own method, but Python didn't like it.
                    chunks = ['<rect ',
                                'x="',
                                line_1_values[0].__str__(),
                                '" y="',
                                line_1_values[1].__str__(),
                                '" width="',
                                line_1_values[2].__str__(),
                                '" height="',
                                line_1_values[3].__str__(),
                                '" fill="#',
                                line_1_values[4],
                                '" />\n']           
                    line_1 = ''.join(chunks)
                    line_2 = svg_lines.pop()                # Get a new secondary line.

                else:
                    optimized_lines.append(line_1)          # Append line_1. It cannot merge with line_2.
                    line_1 = line_2                         # line_2 becomes the "primary line"
                    line_2 = svg_lines.pop()                # Get a new secondary line.
    case 1:
        # Vertical pass. Has not been implemented yet.
        # If two rects share both an x-value AND a fill color,
        # combine them.
        pass

#
# Conversion to JSON Phase
#

# Create the result JSON file.
result = open(os.path.basename(file_path) + '.json', 'w+')

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
for line in optimized_lines:
    # Get the x, y and hexadecimal color code from the rect.
    x = getRectXValue(line)
    y = getRectYValue(line)
    hex_color = getRectColor(line)

    # Adjust the x and y values so the rectangles are seamless at 0.01 scale.
    # Put the values in their respective places in the data list.
    x = (float(x) * 1.28) + ((getRectWidth(line) * 1.28) / 2)
    data[0] = x
    y = (float(y) * 1.28) + ((getRectHeight(line) * 1.28) / 2)
    data[1] = y

    # Set width and height of rectangle.
    data[2] = 0.01 * getRectWidth(line)
    data[3] = 0.01 * getRectHeight(line)

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
    if i < len(optimized_lines):
        result.write(',\n')
    i += 1


# End the parsing process.
result.write(trailer)
result.close()

print('Done! The result file has been placed in this script\'s directory.')
"""