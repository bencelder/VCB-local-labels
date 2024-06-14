# VCB-local-labels

A preprocessor for the VirtualCircuitBoard assembler that enables local labels. For example,
```
@ foo
@ .bar
jmp .bar
```
expands out to 
```
@ foo
@ foo_bar
jmp foo_bar
```
This enables one to reuse common labels like ```.loop```, ```.done```, etc.  For instance, we can re-use ```.bar```, and we can still refer to ```foo.bar``` by using its full name:
```
@ baz
@ .bar
jz  foo.bar
jmp .bar
```
The preprocessor expands this out to
```
@ baz
@ baz_bar
jz  foo_bar
jmp baz_bar
```
Usage: in the terminal, run
> python preprocessor.py test.vcbasm test-out.vcbasm

If this is the final stage before running the simulator, you'll want to have the output file be named ```your-circuit-path.vcbasm```

There is no error catching implemented. Malformed input may not result in an error message/crash, but will likely produce broken code.
