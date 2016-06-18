# encoding=utf-8

# Lists all characters contained in files
# Usage:
# python list_characters.py FILENAME+
# or
# python list_characters.py encoding=ENCODING FILENAME+
#
# Assumes UTF-8 as default encoding.
#
# Jan Strunk
# July 2013

# Use the codecs module to allow easy decoding of character encodings
import codecs

# Regular expressions module
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

# Compile a regular expression to find an encoding option
encoding_re = re.compile(r"^encoding=(\S+)$")

# Terminate if no file name was provided
if len(sys.argv) < 2:
    print("Please provide the name(s) of the file(s) to be searched for characters!")
    sys.exit()

# List of Toolbox files to process
list_of_files = []

# Was another encoding selected at the command line?
if len(sys.argv) > 2:
    match = encoding_re.search(sys.argv[1])
    if match:
        encoding = match.group(1)
        list_of_files = sys.argv[2:]
    else:
        list_of_files = sys.argv[1:]
else:
    list_of_files = sys.argv[1:]

# Expand wildcards on Windows
if platform == "win32":
    new_list_of_files = []
    for file_name in list_of_files:
        abs_file_name = os.path.abspath(os.path.normpath(file_name))
        file_names = glob.glob(abs_file_name)
        new_list_of_files.extend(file_names)

    list_of_files = new_list_of_files

# Dictionary from characters to file_names
characters = {}

# Go through the list of files
for filename in list_of_files:
    
    # Print status message
    print("Processing file:", filename, file = sys.stderr)
    
    # Open file
    input_file = codecs.open(filename, "r", encoding)
    
    # Go through file line by line
    for line in input_file:
        
        # Split line into characters
        line_characters = list(line)
        
        # Go through all characters in the line
        for character in line_characters:
            
            # Save the character in a dictionary from characters
            # to filenames
            if character in characters:
                
                characters[character] += 1
            
            else:
                
                characters[character] = 1
            
    # Close Toolbox file
    input_file.close()

# Output a sorted list of markers
# one per line in order to allow for the use of sort and uniq
for character in sorted(characters):
    
    print(character + "\t" + " " + str(characters[character]))
