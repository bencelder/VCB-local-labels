"""
A preprocessor for VCB that enables local labels. For example,

@ foo
@ .bar

jmp .bar

expands out to 
@ foo
@ foo.bar
jmp foo.bar

This enables one to reuse common labels like .loop, .done, etc:

@ baz
@ .bar
jz  foo.bar
jmp .bar

which expands out to

@ baz
@ .bar
jz  foo.bar
jmp baz.bar

Usage:
> python preprocessor.py infile.vcbasm outfile.vcbasm

If this is the final stage before running the code, you want to have outfile = your-circuit-path.vcbasm

There is no error catching implemented. Malformed input may not result in an error message/crash.

This currently only does ONE replacement per line.
"""
import sys

if len(sys.argv) != 3:
    print("Incorrect number of input arguments.")
    print("Usage:")
    print("> python preprocessor.py infile.vcbasm outfile.vcbasm")
    # Exit with an error code
    sys.exit(1)

infile  = sys.argv[1]
outfile = sys.argv[2]

# Read the original code in
f = open(infile, "r")
lines = []
for line in f:
    lines.append(line)

f.close()

# Transform the code with regex
import re

# The "toplevel" is the current (global) label
# The "local" is the label that we want to be local to label

# A toplevel statement looks like
# @ name_of_thing   # optional comment
# That is, @, followed by at least one spaces or tab, and then a label name.
# The label name must start with a letter, but after that can contain any number of
# underscores or numbers.
# It is followed by a space, tab, or newline
# https://regex101.com/r/OHPAvk/1
# By matching the trailing whitespace, we avoid matching on full names like
# @ foo.bar
regex_toplevel = r"@[ \t]+([a-zA-Z][a-zA-Z0-9_]*)[ \t\n]"

# A full label name looks like global_name.local_name
# The local name must start with a letter or number, and can contain underscores
# https://regex101.com/r/RrMqKS/1
# We match to the last character of the global name, so as to avoid matching
# local name usage like
# @ .bar
regex_full_name = r"([a-zA-Z_]+)\.([a-zA-Z0-9][a-zA-Z0-9_]*)"

# A local label in use consists of a space or tab, then a ., and then a local name
regex_local = r"([ \t]+)\.([a-zA-Z0-9][a-zA-Z0-9_]*)"


newlines = []
toplevel = ''
for line in lines:


    # Check for updates to the global label
    x = re.findall(regex_toplevel, line)
    if x:
        toplevel = x[0]
        newlines.append(line)
        continue

    # First do a find/replace on full names (globalname.localname -> globalname_localname)
    line = re.sub(regex_full_name, r"\1_\2", line)

    # Now do a find/replace to expand the local labels to their full names
    line = re.sub(regex_local, r"\1" + toplevel + r"_\2", line)
    newlines.append(line)

# Write the transformed code to the outputfile
f = open(outfile, "w")
for line in newlines:
    f.write(line)
f.close()

