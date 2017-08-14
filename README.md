# Archie [![Build Status](https://travis-ci.org/niccroad/Archie.svg?branch=master)](https://travis-ci.org/niccroad/Archie)
Enforce and maintain the architecture of C/C++ source code.

Archie uses the C/C++ preprocessor #include mechanism to enforce a specified project architecture at compile time. In order to 
enforce development stick to a specified layered architecture all translation units in the source directory tree are given a tier
of the architecture. Header files are then reorganized into a series of tier folders during the build step and a translation unit 
may only then #include other header files which come from the same tier or a lower tier of the architecture. This effectively makes
it impossible to introduce circular dependencies spanning several tiers of the program.

## Usage

### Configuration

The architecture is configured in a YAML format file by default called .archie-config. A simple configuration might look like,

```
source_paths: [source]
base_include_folder: build/include

default_tier: 2
modules:
  - pattern: '**/entities'
    tier: 1
  - pattern: '**/*_p.h(pp)?'
    tier: 0
```

### Source Layout

When using Archie, source code should be layed out into a collection of folders first grouping code together by the
feature it relates to. A second grouping should then be applied with common folder names separating translation units
by the tier they belong to. This groups related code together, but at build time maintains a clear relationship between
translation units and what dependencies they can use.

```
  - source
      - firstfeature            # (Tier 3)
          - entities            # (Tier 1)
          - behaviours          # (Tier 2)
          - db                  # (Tier 4)
          - ui                  # (Tier 4)
      - secondfeature           # (Tier 3)
          - entities            # (Tier 1)
          - behaviours          # (Tier 2)
          - ui                  # (Tier 4)
```

During the header reorganization step the headers in the source code are hard-linked to an alternative build structure
which might look like the following for this example.

```
  - build
      - include
          - T1                    # (from both entities folders)
          - T2                    # (from both behaviours folders)
          - T3                    # (from both feature folders)
          - T4                    # (from db and ui folders)
```

### Source Code

In the source code you simply refer to your includes as if all headers are available in a single shared folder. At 
compile time only those includes of the same or a lower tier will be available on the include path, which prevents
circular dependencies from being introduced across more than one layer.

```cpp
#include "Tier2Class.h"
// In a Tier 2 cpp file you can #include headers from a lower tier.
#include "SomeClassAtTier1.h"
// The following #include however would result in an un-resolved include.
// #include "SomeClassAtTier4.h"

Tier2Class::Tier2Class() { }
```

### SCons Integration

Archie is written in python and is 2.7 compatible so integration with scons is relatively easy. Several small examples are included 
in the project using scons to build. The key steps actions are,

```python
import archie
# Create Archie object, the defaults are used for the parameters here
archie = archie.Archie('.archie-config', base_include_path = None)
# Restructure header files according to the configuration
archie.installHeaderFiles()
# ...
# Retrieve a list of the include folders to compile translation units in the folder source/entities
includes = archie.getIncludePath('source/entities')
```

### Other Build Integration

Other build integrations are done by running Archie as a python script on the command line. The re-organize headers step is done
with the command,

```sh
# Reorganises headers into their build folders.
python -m archie --install_headers

# Prints the include path, including the flags, for a source folder.
python -m archie --show_include_path source/entities
# -Ibuild\include\T1
```
