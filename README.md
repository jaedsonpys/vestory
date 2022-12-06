# Vestory - Fast, simple and practical

![BADGE](https://img.shields.io/static/v1?label=license&message=GPL%20v3.0&color=red&style=flat-square)
![BADGE](https://img.shields.io/static/v1?label=language&message=Python&color=orange&style=flat-square)

**Vestory** (junction of "Version" and "History"), is a practical and fast version control used in any terminal by command line (**CLI**). With simple and easy-to-remember commands, making it easy to use. 

> Version control **better than Vestory** is now available, [meet Pie](https://github.com/jaedsonpys/pie) now!

### Links

- [Version 1.2](#Version-1.2)
- [Installation](#Installation)
- [How it works](#How-it-works)
- [Using the Vestory](#Using-the-Vestory)
    - [Initializing repository](#Initializing-repository)
    - [Add files](#Add-files)
    - [Submit Changes](#Submit-Changes)
    - [Merge changes](#Merge-changes)
    - [View change-log](#View-change-log)
    - [File Status](#File-Status)
    - [Ignoring files or directories](#Ignoring-files-or-directories)
- [License](#License)

## Version 1.2

This version of Vestory can:

- [x] Monitor file changes;
- [x] Save file changes;
- [x] View change logs;
- [x] Merge file changes;
- [x] Ignore files;

## Installation

To install **Vestory**, use the PyPi package manager:

```
pip install vestory
```

After that, you can use it from the command line with the `vestory` command.

## Using the Vestory

First, see the list of commands available so far:

- `init`: creates a new repository;
- `add [files]`: adds files to change tracking;
- `submit`: saves the changes made so far.

### Initializing repository

To initialize a repository, use the `init` command:

```
vestory init
```

Before that, your settings must be done to initialize a repository
correctly.

### Add files

To add files to change tracking:

```
vestory add example.txt
```

It is also possible to add several files at once, typing the name of each one or using the `-a` flag:

```
vestory add example.txt test.py project/app.py
```
```
vestory add -a
```

> the `-a` flag adds all files present in the directory.

### Submit changes

To commit a change, you need to specify the files, or commit the change of all files that were added using the `-a` flag.

It is also necessary to add a comment about that change, for this we use the `-c` flag. See an example:

```
vestory submit example.txt -c 'first changes'
```

You can commit changes to all monitored files and add a comment using the `-ac` abbreviation:

```
vestory submit -ac 'first changes'
```

### Merge changes

With the `join` argument, you will merge all changes to a file, replacing the original file. See the use of this argument:

```
vestory join
```
<!--
This command will make all files being tracked merge your changes. It is also possible to merge changes from just one file:

```
vestory join test.txt
``` -->

Note that a warning message will appear before the process is carried out:

```
warning: the "join" command will replace the current files.
> Do you wish to proceed? [y/n]
```

Confirming, the process will be carried out.

### View change log

To see all the changes that have been made, use the `log` argument:

```
vestory log
```

The following information will be displayed:

- Author name
- Author's email
- Date of change
- change ID
- Comment on the change

### Status of files

The status of the file shows whether it has been changed or not, to check this information use the `status` argument:

```
vestory status
```

### Ignoring files or directories

To ignore files or directories, create a file at the root of your directory called `.ignoreme`. Add line by line each file/directory that will be ignored. By ignoring a file, it will not be added to the change tracking when using the `add -a` command, nor will it have its changes committed.

When adding subdirectories to `.ignoreme`, do it like this:

```
dir/subdir
```

## License

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
