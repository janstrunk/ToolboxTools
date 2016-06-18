# encoding=utf-8

# Lists all Toolbox markers contained in one or multiple Toolbox files
# Usage:
# python listtoolboxmarkers.py FILENAME+
# or
# python listtoolboxmarkers.py encoding=ENCODING FILENAME+
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

# Set to save all markers found
markers = set()

# Terminate if no file name was provided
if len(sys.argv) < 2:
    print("Please provide the name(s) of the file(s) to be searched for Toolbox markers!")
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
            # Extract marker
            marker = match.group(1)
            
            # Save marker in set
            markers.add(marker)
    
    # Close Toolbox file
    toolbox_file.close()

# Ignore \_sh marker in header
if "_sh" in markers:
    markers.remove("_sh")

# Output a sorted list of markers
# one per line in order to allow for the use of sort and uniq
for marker in sorted(markers):
    print(marker)
