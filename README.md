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
