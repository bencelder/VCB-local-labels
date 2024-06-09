# VCB-local-labels

A preprocessor for VirtualCircuitBoard that enables local labels. For example,
```
@ foo
@ _bar
jmp _bar
```
expands out to 
```
@ foo
@ foo_bar
jmp foo_bar
```
This enables one to reuse common labels like @_loop, @_done, etc:
```
@ baz
@ _bar
jz  foo_bar
jmp _bar
```
which expands out to
```
@ baz
@ _bar
jz  foo_bar
jmp baz_bar
```
Usage: in the terminal, run
> python preprocessor.py test.vcbasm test-out.vcbasm

If this is the final stage before running the simulator, you want to have the output file be named your-circuit-path.vcbasm

There is no error catching implemented. Malformed input may not result in an error message/crash.
