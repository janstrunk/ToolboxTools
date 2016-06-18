# encoding=utf-8

# Validates the encoding if one or multiple Toolbox files by reading them
# into Python via the codecs module
# Usage:
# python validateencoding.py FILENAME+
# or
# python validateencoding.py encoding=ENCODING FILENAME+
#
# Assumes UTF-8 as default encoding.
#
# Jan Strunk
# August 2012

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

# Compile a regular expression to find an encoding option
encoding_re = re.compile(r"^encoding=(\S+)$")

# Terminate if no file name was provided
if len(sys.argv) < 2:
    print("Please provide the name(s) of the file(s) whose encoding is to be validated!")
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

# Go through the list of files
for filename in list_of_files:
    
    # Print status message
    print("Processing file:", filename, file=sys.stderr)
    
    # Open Toolbox file
    toolbox_file = open(filename, "rb")
    
    # Count line numbers
    line_number = 1
    
    # Go through Toolbox file line by line and search for Toolbox markers
    for line in toolbox_file:

        # Try to decode the line
        try:
            line_decoded = line.decode(encoding)
        
        # A decode error occurred
        except UnicodeDecodeError:
            # Output information about the error
            print("There was a decoding problem in file", filename, "line", line_number, ":", end=" ")
            print(repr(line))
        
        # Break if the end of the file has been reached
        if line == "":
            break
        
        # Increase line number
        line_number += 1
    
    # Close Toolbox file
    toolbox_file.close()
