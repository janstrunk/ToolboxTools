# encoding=utf-8

# Count all tokens contained in one tier of one or multiple Toolbox files
# Usage:
# python counttokenstoolbox.py WORDTIERNAME FILENAME+
# or
# python counttokenstoolbox.py encoding=ENCODING WORDTIERNAME FILENAME+
#
# Assumes UTF-8 as default encoding.
#
# Jan Strunk
# August 2012

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
toolbox_marker = re.compile(r"^\\(\S+)\s")

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
                tokens = line.split()
                
                # Remove tier marker at the start of the line
                tokens = tokens[1:]
                
                # Count the number of words in the current line
                number_of_tokens += len(tokens)
    
    # Close Toolbox file
    toolbox_file.close()

print(number_of_tokens, "tokens found in tier", tier_name)
