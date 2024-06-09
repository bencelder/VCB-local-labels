"""
A preprocessor for VCB that enables local labels. For example,

@ foo
@ _bar

jmp _bar

expands out to 
@ foo
@ foo_bar
jmp foo_bar

This enables one to reuse common labels like @_loop, @_done, etc:

@ baz
@ _bar
jz  foo_bar
jmp _bar

which expands out to

@ baz
@ _bar
jz  foo_bar
jmp baz_bar

Usage:
> python preprocessor.py infile.vcbasm outfile.vcbasm

If this is the final stage before running the code, you want to have outfile = your-circuit-path.vcbasm

There is no error catching implemented. Malformed input may not result in an error message/crash.
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

f = open(infile, "r")

lines = []
for line in f:
    lines.append(line)

f.close()


import re

# The "toplevel" is the current (global) label
# The "local" is the label that we want to be local to label
regex_toplevel = "^[ \t]*@[ \t]+([a-zA-Z][a-zA-Z0-9]*)[ \t]*\n"
regex_local    = "([ \t])(_[a-zA-Z0-9]*)"

newlines = []
toplevel = ''
for line in lines:

    # Check for updates to the global label
    x = re.findall(regex_toplevel, line)
    if x:
        toplevel = x[0]
        newlines.append(line)
        continue

    # Otherwise, do a find/replace to expand the local labels to their full names
    x = re.sub(regex_local, r"\1" + toplevel + r"\2", line)
    newlines.append(x)

f = open(outfile, "w")
for line in newlines:
    f.write(line)
f.close()
