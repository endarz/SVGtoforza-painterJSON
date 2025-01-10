# SVG to ForzaPainterJSON -
# A Python script designed to convert pixel art into Forza Horizon vinyl groups
# via forza-painter.
#
# Created by endarz
# Last edit: 1/10/2025
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

method = int(input('Please specify what method of optimization to use:\n'
               + '\t0 for Horizontal Merging,\n'
               + '\t1 for Vertical Merging.\n'
               + 'It is recommended to try both methods, as one will provide fewer layers than the other.\n\n'
               + 'Method: '))

match method:
        case 0:
            # Horizontal merging.
            #
            # For each row in the pixel grid, use a primary pixel and a secondary pixel.
            # Compare the secondary pixel to the primary pixel; if its color is the same
            # as the primary pixel's color, then add one to the primary pixel's width
            # and replace the secondary pixel with None in the pixel grid.

            # For each row in the grid...
            print('Starting horizontal merging...')
            for i in range(len(pixel_grid)):
                # For each value in the row...
                for j in range(len(pixel_grid[0])):
                    pri_pix = pixel_grid[i][j]                  # Get values for primary and secondary pixels.
                    sec_pix = pixel_grid[i][j + 1]
                    if pri_pix == None or sec_pix == None:      # If either of the values is a None, then reiterate or potentially leave the row.
                        if j == len(pixel_grid[i]) - 2: break   # Edge case: if this is the last pixel in the row, then leave this row.
                        else: continue                          # Otherwise, reiterate.
                    # Check to see if the secondary pixel's color matches the primary pixel's color.
                    # If it does, then merge it with the primary.
                    # Do this until the secondary pixel is a None or does not match.
                    while sec_pix[4] == pri_pix[4]:
                        pri_pix[2] += 1                                 # Increment primary pixel's width by one.
                        pixel_grid[pri_pix[1]][pri_pix[0]] = pri_pix    # Update primary pixel in the pixel grid.
                        pixel_grid[sec_pix[1]][sec_pix[0]] = None       # Replace secondary pixel in the pixel grid with None.
                        if sec_pix[0] == len(pixel_grid[0]) - 1: break  # If the pixel just merged is the last pixel in the row, then leave the color merge loop.
                        else:                                           # Otherwise, get a new secondary pixel.
                            sec_pix = pixel_grid[i][sec_pix[0] + 1]     # Get the next secondary pixel.
                            if sec_pix == None: break                   # If it is a None, then leave the color merge loop.
                    if sec_pix == None:     # If the secondary pixel is a None, then reiterate.
                        continue
                    elif sec_pix[0] == len(pixel_grid[0]) - 1:  # If the end of the row has been reached, then move to the next row.
                        break
        case 1:
            # Vertical merging
            #
            # Instead of merging pixels in the same row, merge pixels in the same column.
            # Since much of this algorithm was copy/pasted from case 0, please see it for detailed comments.
            print('Starting vertical merging...')
            for i in range(len(pixel_grid[0])):
                for j in range(len(pixel_grid)):
                    pri_pix = pixel_grid[j][i]      # Get values for primary and secondary pixels, except going down the columns this time.
                    sec_pix = pixel_grid[j + 1][i]
                    if pri_pix == None or sec_pix == None:
                        if j == len(pixel_grid) - 2: break
                        else: continue
                    while sec_pix[4] == pri_pix[4]:
                        pri_pix[3] += 1     # Increment the HEIGHT instead of WIDTH this time.
                        pixel_grid[pri_pix[1]][pri_pix[0]] = pri_pix
                        pixel_grid[sec_pix[1]][sec_pix[0]] = None
                        if sec_pix[1] == len(pixel_grid) - 1: break
                        else:
                            sec_pix = pixel_grid[sec_pix[1] + 1][i]
                            if sec_pix == None: break
                    if sec_pix == None:
                        continue
                    elif sec_pix[1] == len(pixel_grid) - 1:
                        break
        case _:
            print('ERROR -- '
                  + 'Invalid method value given.')
            exit(1)

print('Merging complete.')

#
#   JSON Generation Phase
#

print('Starting JSON file generation...')
# Create the result JSON file.
result_name = ''
if method == 0:
    result_name += os.path.basename(file_path) + '.horizontal.json'
if method == 1:
    result_name += os.path.basename(file_path) + '.vertical.json'
result = open(result_name, 'w+')

# Prepare values for creating the JSON.
header = '{"shapes":\n['
trailer = '\n]}'
type = 1048677                  # The "shape ID." This value is a square.
data = [0, 0, 0, 0, 0, 0, 0]    # X position; Y position; scale X; scale Y; rotation; and two other values that I don't know.
color = [255, 255, 255, 255]    # Red, Green, Blue and Alpha values
score = 0.8008135               # Shape accuracy; used by forza-painter. :]
json_shapes = []                # Stores the shapes after they are converted to JSON.

# Begin the parsing process.
result.write(header)

# Reverse shapes to print in correct order.
pixel_grid.reverse()

# Parse each pixel in the pixel grid, turning it into JSON.
for row in pixel_grid:
    for pixel in row:
        # Skip to next pixel when a None is found.
        if pixel == None:
            continue
        else:
            # Get the x, y and hexadecimal color code from the rect.
            x = pixel[0]
            y = pixel[1]
            hex_color = pixel[4]

            # Adjust the x and y values so the rectangles are seamless at 0.01 scale.
            # Put the values in their respective places in the data list.
            x = (float(x) * 1.28) + ((pixel[2] * 1.28) / 2)
            data[0] = x
            y = (float(y) * 1.28) + ((pixel[3] * 1.28) / 2)
            data[1] = y

            # Set width and height of rectangle.
            data[2] = 0.01 * pixel[2]
            data[3] = 0.01 * pixel[3]

            # Convert hex color to RGB values.
            color[0] = int(hex_color[0:2], 16)
            color[1] = int(hex_color[2:4], 16)
            color[2] = int(hex_color[4:6], 16)

            # Create a string of JSON.
            json = '{'
            json += '"type":' + str(type) + ','
            json += '"data":' + str(data).replace(' ', '') + ','
            json += '"color":' + str(color).replace(' ', '') + ','
            json += '"score":' + str(score)
            json += '}'

            # Add to JSON shapes list.
            json_shapes.append(json)

# Write JSON shapes to the file.
result.write(',\n'.join(json_shapes))

# End the parsing process.
result.write(trailer)
result.close()
print('JSON file created at ' + os.getcwd() + result_name)

print('Done! The result file has been placed in this script\'s directory.')
input('To exit the script, please close the window or hit ENTER.')

exit(0)