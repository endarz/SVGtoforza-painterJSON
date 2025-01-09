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
            #print('Row: ' + str(row))
            for i in range(len(row)):
                #print('i: ' + str(i))
                pri_pix = row[i]
                sec_pix = row[i + 1]
                #print('Primary pixel: ' + str(pri_pix))
                #print('Secondary pixel: ' + str(sec_pix))
                if pri_pix == None or sec_pix == None:  # If either of the pixels is a None...
                    if i == len(row) - 2:   # Edge case: if the last pixel in the row is a none, leave this row.
                        #print('Last pixel in the row is a None. Leaving the row...')
                        break
                    else:                   # Otherwise, go to the next iteration.
                        #print('One of the pixels is a None. Reiterating...')
                        continue
                # Check if the secondary pixel's color matches primary pixel's color.
                # If it does, then merge.
                while sec_pix[4] == pri_pix[4]:
                    #print('Color match found.')
                    #print('Merging ' + str(sec_pix) + ' with ' + str(pri_pix))
                    pri_pix[2] += 1                                 # Increment primary pixel's width by one.
                    pixel_grid[pri_pix[1]][pri_pix[0]] = pri_pix    # Update primary pixel in the pixel grid.
                    pixel_grid[sec_pix[1]][sec_pix[0]] = None       # Update secondary pixel in the pixel grid.
                    row[sec_pix[0]] = None                          # Update secondary pixel in the row.
                    #print('New pixel: ' + str(pri_pix))
                    #print('Row: ' + str(row))

                    # Check if the last pixel in the row just got merged.
                    # If it did, then we need to leave and start a new row.
                    if sec_pix[0] == len(row) - 1:
                        #print('Last pixel in the row just got merged. Leaving the row...')
                        break
                    else:
                        #print('Getting new secondary pixel...')
                        sec_pix = row[sec_pix[0] + 1]               # Get the pixel following the secondary pixel.
                        #print('New secondary: ' + str(sec_pix))
                        if sec_pix == None:                         # If the new secondary pixel is a None, exit the loop.
                            #print('New secondary is a None. Exiting the merge loop...')
                            break
                if sec_pix == None:
                    #print('The new secondary is a None. Reiterating...')
                    continue
                elif sec_pix[0] == len(row) - 1:
                    #print('The end of the row has been reached. Leaving the row...')
                    break
    case 1:
        pass
print('Merging complete.')

#
#   JSON Generation Phase
#

print('Starting JSON file generation...')
# Create the result JSON file.
result = open(os.path.basename(file_path) + '.json', 'w+')

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

# Write json shapes to the file.
result.write(',\n'.join(json_shapes))

# End the parsing process.
result.write(trailer)
result.close()
print('JSON file created at ' + os.getcwd() + os.path.basename(file_path) + '.json.')

print('Done! The result file has been placed in this script\'s directory.')

exit(0)