# encoding=utf-8

# TODO:
# - Use argparse
# - Add option to print to output file
# - Add option to change sort order
# - Add option to perform case folding

# Count all values (whole lines) contained in one tier of one or multiple Toolbox files
# Usage:
# python countvaluestoolbox.py TIERNAME FILENAME+
# or
# python countvaluestoolbox.py encoding=ENCODING TIERNAME FILENAME+
#
# Assumes UTF-8 as default encoding.
#
# Jan Strunk
# October 2012

# Use the codecs module to allow easy decoding of character encodings
import codecs

# Regular expressions
import re

# Access to command-line arguments
import sys

# Modules for handling paths
import os.path
import glob

# Default encoding
encoding = "utf-8"

# Determine the platform we are running on
platform = sys.platform
if platform.startswith("linux"):
    platform = "linux"

# Compile a regular expression to find a Toolbox marker
toolbox_marker = re.compile(r"^\\(\S+)\s+(.+)$")

# Compile a regular expression to find an encoding option
encoding_re = re.compile(r"^encoding=(\S+)$")

# Terminate if no file name was provided
if len(sys.argv) < 3:
    print("Please provide the name of the Toolbox tier and the name(s) of the file(s) to be searched!")
    sys.exit()

# List of Toolbox files to process
list_of_files = []

# Name of the tier to be searched
tier_name = ""

# Was another encoding selected at the command line?
if len(sys.argv) > 3:
    match = encoding_re.search(sys.argv[1])
    if match:
        encoding = match.group(1)
        tier_name = sys.argv[2]
        list_of_files = sys.argv[3:]
    else:
        tier_name = sys.argv[1]
        list_of_files = sys.argv[2:]
else:
    tier_name = sys.argv[1]
    list_of_files = sys.argv[2:]

# Expand wildcards on Windows
if platform == "win32":
    new_list_of_files = []
    for file_name in list_of_files:
        abs_file_name = os.path.abspath(os.path.normpath(file_name))
        file_names = glob.glob(abs_file_name)
        new_list_of_files.extend(file_names)

    list_of_files = new_list_of_files

# Variable to count the number of tokens
number_of_tokens = 0

# Variable to count the number of types (values)
number_of_types = 0

# Dictionary to count the types (values) and how often they occur
type_dict = {}

# Go through the list of files
for filename in list_of_files:
    
    # Print status message
    print("Processing file:", filename, file = sys.stderr)
    
    # Open Toolbox file
    toolbox_file = codecs.open(filename, "r", encoding)
    
    # Go through Toolbox file line by line and search for Toolbox markers
    for line in toolbox_file:
        # Remove superfluous whitespace
        line = line.strip()
        
        # Does the beginning of the line contain a marker?
        match = toolbox_marker.search(line)
        if match:
            marker_name = match.group(1).strip()
            
            # Was the marker of the requested tier found?
            if marker_name == tier_name:

                # Split line at white space
                value = match.group(2).strip()
                
                # Count the current value as one token
                number_of_tokens += 1
                
                # Has the type already been encountered?
                if value in type_dict:
                    
                    # Increment count
                    type_dict[value] += 1
                    
                # New type
                else:
                    type_dict[value] = 1
    
    # Close Toolbox file
    toolbox_file.close()

# Output statistics
print(number_of_tokens, "tokens found in tier", tier_name)

# Count the number of distinct types
number_of_types = len(type_dict)

# Calculate the type/token ratio
if number_of_types > 0:
    type_token_ratio = round(number_of_types / number_of_tokens, 4)
else:
    print("No types found.")
    sys.exit()

# Output statistics
print(number_of_types, "distinct types in tier", tier_name)
print("Type/token ratio:", type_token_ratio)

# Output a frequency table of types
print()
print("Type\tFrequency")
for cur_type in sorted(type_dict, key=type_dict.get, reverse=True):
    print(cur_type + "\t" + str(type_dict[cur_type]))
