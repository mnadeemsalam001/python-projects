---
title:       "Python 3.14.5 is out! | Python Insider"
date:        "May 10, 2026"
url:         "https://blog.python.org/2026/05/python-3145-is-out"
description: "A special release with a new (old) garbage collector."
word_count:  689
---

Python 3.14.5 final is the fifth maintenance release of 3.14, containing around 154 bugfixes, build improvements and documentation changes since 3.14.4.

python.org/downloads/release/python-3145

## Garbage collector

Notably, the garbage collector (GC) has changed in Python 3.14.5.

The incremental garbage collector shipped in Python 3.14.0-3.14.4 has been reverted back to the generational garbage collector from 3.13, due to a number of reports of significant memory pressure in production environments. See What’s New and discuss.python.org for details.

## Tcl/Tk 9 on macOS

The official macOS installer has been updated to use Tcl/Tk 9.0.3 instead of 8.6.17.

## Major new features of the 3.14 series, compared to 3.13

Some of the major new features and changes in Python 3.14 are:

### New features

- PEP 779: Free-threaded Python is officially supported
- PEP 649: The evaluation of annotations is now deferred, improving the semantics of using annotations.
- PEP 750: Template string literals (t-strings) for custom string processing, using the familiar syntax of f-strings.
- PEP 734: Multiple interpreters in the stdlib.
- PEP 784: A new module `compression.zstd` providing support for the Zstandard compression algorithm.
- PEP 758: `except` and `except*` expressions may now omit the brackets.
- Syntax highlighting in PyREPL, and support for color in unittest, argparse, json and calendar CLIs.
- PEP 768: A zero-overhead external debugger interface for CPython.
- UUID versions 6-8 are now supported by the `uuid` module, and generation of versions 3-5 are up to 40% faster.
- PEP 765: Disallow `return`/`break`/`continue` that exit a `finally` block.
- PEP 741: An improved C API for configuring Python.
- A new type of interpreter. For certain newer compilers, this interpreter provides significantly better performance. Opt-in for now, requires building from source.
- Improved error messages.
- Builtin implementation of HMAC with formally verified code from the HACL\* project.
- A new command-line interface to inspect running Python processes using asynchronous tasks.
- The pdb module now supports remote attaching to a running Python process.

For more details on the changes to Python 3.14, see What’s new in Python 3.14.

### Build changes

- PEP 761: Python 3.14 and onwards no longer provides PGP signatures for release artifacts. Instead, Sigstore is recommended for verifiers.
- Official macOS and Windows release binaries include an experimental JIT compiler.
- Official Android binary releases are now available.

### Removals and new deprecations

- Python removals and deprecations
- C API removals and deprecations
- Overview of all pending removals

## Python install manager

The installer we offer for Windows is being replaced by our new install manager, which can be installed from the Windows Store or from its download page. See our documentation for more information. The JSON file available for download contains the list of all the installable packages available as part of this release, including file URLs and hashes, but is not required to install the latest release. The traditional installer will remain available throughout the 3.14 and 3.15 releases.

## More resources

- Online documentation
- PEP 745, 3.14 Release Schedule
- Report bugs at github.com/python/cpython/issues
- Help fund Python directly (or via GitHub Sponsors) and support the Python community

## And now for something completely different

I asked Guinness World Record holder Rodrigo Girão Serrão for a fun *π* fact:

> **Euler’s identity** says that *e**iπ* + 1 = 0 and is often cited as an equality of profound mathematical elegance, since it relates five of the most fundamental mathematical constants: 0, 1, *π*, *e*, and *i*. A mathematics professor at Stanford University has said “like a Shakespearean sonnet that captures the very essence of love, or a painting that brings out the beauty of the human form that is far more than just skin deep, Euler’s equation reaches down into the very depths of existence”.

Source

## Enjoy the new release

Thanks to all of the many volunteers who help make Python Development and these releases possible! Please consider supporting our efforts by volunteering yourself or through organisation contributions to the Python Software Foundation.

Regards from Helsinki with nearly 17 hours of daylight,

Your release team,\
Hugo van Kemenade\
Ned Deily\
Steve Dower\
Łukasz Langa