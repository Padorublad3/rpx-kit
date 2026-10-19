# RPX-KIT

## Description 
A toolkit for extracting or viewing only RPA-3.0 archives made with Renpy


## ✨Features
**Safe Unpickling**. Uses a custom SafeUnpickler that blocks all external imports during deserialization.

**Zero Dependencies**.

**CLI Mask Filtering**. Filter files directly using shell-style patterns (e.g., -m "*.png"). Extract or list only what you need without dumping the entire archive to disk first.

**Cross-Platform**. Works identically on Windows, Linux, and macOS. Path handling is abstracted via pathlib, so no slash-related issues.


## Installation
> [!NOTE]
> **Python >= 3.9** is required

Via pip
```bash
pip install https://github.com/Padorublad3/rpx-kit.git
```


## Usage
```
rpx-kit [-l | -o DIR] [-m PATTERN]... INPUT_PATH

Arguments:
  INPUT_PATH       Input .rpa archive file

Options:
  -l, --list       Print list of files contained in the archive
  -o, --output     Target directory for extraction (creates if missing)
  -m, --mask       Filter by fnmatch pattern (repeatable, e.g., -m "*.png")
```


## Examples
List all PNG and JPG files:
```bash
rpx-kit mygame/archive.rpa -m "*.png" -m "*.jpg" -l
```
Save the list to a text file:
```bash
rpx-kit mygame/archive.rpa -m "*.png" -m "*.jpg" -l > result.txt
```
Extract only PNG and JPG files to a folder:
```bash
rpx-kit mygame/archive.rpa -m "*.png" -m "*.jpg" -o destination_folder
```