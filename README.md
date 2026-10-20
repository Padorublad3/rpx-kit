# RPX-KIT

## Description 
A toolkit for extracting or viewing only RPA-3.0 archives made with Renpy


## Features
**Safe Unpickling**. Uses a custom SafeUnpickler that blocks all external imports during deserialization.

**Zero Dependencies**.

**CLI Mask Filtering**. Filter files directly using shell-style patterns (e.g., -m "*.png"). Extract or list only what you need without dumping the entire archive to disk first.

**Cross-Platform**. Works identically on Windows, Linux, and macOS. Path handling is abstracted via pathlib, so no slash-related issues.


## Installation
> [!NOTE]
> **Python >= 3.9** is required

Via pip
```bash
pip install git+https://github.com/Padorublad3/rpx-kit.git
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
## Mask Cheat Sheet

Masks use standard shell-style patterns (`fnmatch`). Remember to wrap them in quotes!

| Pattern | Meaning | Example Match |
| :--- | :--- | :--- |
| `*` | Matches **any sequence** of characters (including none) | `*.png` → `image.png`, `bg/day.png` |
| `?` | Matches exactly **one** character | `img?.png` → `img1.png`, but NOT `img10.png` |
| `[abc]` | Matches **one** char from the set | `file[123].txt` → `file1.txt`, `file2.txt` |
| `[a-z]` | Matches one char in a **range** | `letter[a-e].rpyc` → `lettera.rpyc` |
| `[!abc]` | Matches one char **NOT** in the set | `img[!0-9].png` → `imgA.png`, but NOT `img1.png` |

##  Tips:
1. **Extensions:** Always start with `*.` for extensions.
   ✅ `-m "*.jpg"` 
   ❌ `-m ".jpg"` (looks for a file literally named `.jpg`)
2. **Paths vs Names:** Masks work on both full paths and filenames.
   - `-m "images/*"` finds everything inside the `images/` folder.
   - `-m "bg_*"` finds any file starting with `bg_`, regardless of its folder.
3. **OR Logic:** Multiple `-m` flags are combined with OR.
