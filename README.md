DWARF/Ada testsuite
===================

This repository hosts a tiny testsuite to check various properties of the DWARF
debug information that GCC generates for Ada programs in minimal GNAT encodings
mode (`-fgnat-encodings=minimal`).

I wrote this testsuite to help me developing and maintaining GCC patches for
Ada DWARF debug info.


Running
-------

First, make sure that `which python` yields a Python 2 setup that has the
[pyelftools](https://github.com/eliben/pyelftools) package installed. Then,
just run:

```sh
./run.py
```

This will run all testcases in the [tests](tests/) directory and display on the
standard output whether they succeeded or failed. If they failed, an error
message is displayed.

It is possible to run just several specific testcases. For instance:

```sh
$ ./run.py tests/fixedpoint tests/record_subtype
Using compiler: /usr/bin/gcc
OK:    tests/fixedpoint
OK:    tests/record_subtype
```

If you want to use this testsuite during GCC development, it is possible to
make it use the `gnat1` executable directly, which is handy as you don’t have
to build the whole GCC project. Note that you’ll need a minimal runtime to do
that (if not, `gnat1` will complain about missing `system.ads`). Just run:

```sh
./run.py --gnat1=/path/to/your/gnat1
```


How about the GCC testsuite?
----------------------------

I’m not very familiar with TCL/DejaGNU and writing tests that do more than
checking text outputs with this technology looks hard. Writing pyelftools-based
testcases was much more easier, faster and more reliable so that’s what I did
when I worked on GCC’s DWARF output.

While my long term plan is to port these testcases to the official GCC
testsuite, this is going to require a lot of work, so in the meantime there is
this repository. :-)
