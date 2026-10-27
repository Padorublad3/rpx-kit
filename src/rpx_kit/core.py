import io
import pickle
import zlib
from fnmatch import fnmatch
from pathlib import Path
from typing import BinaryIO


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module_name, global_name):
        raise pickle.UnpicklingError("Import is prohibited")


def read_index(infile: BinaryIO) -> dict:
    header = infile.read(33)
    if not header.startswith(b"RPA-3.0 "):
        raise ValueError("Unsupported format")
    offset, key = int(header[8:24], 16), int(header[25:33], 16)
    infile.seek(offset)
    virtual_file = io.BytesIO(zlib.decompress(infile.read()))
    index = SafeUnpickler(virtual_file).load()

    for filename in index:
        # index = Dict[str, List[Tuple[int, int, bytes]]]
        # Key = filename
        # Values = list of chunks (offset, length, bytes)
        # Bytes never used in RPA 3.0
        offset, length = index[filename][0][0], index[filename][0][1]
        index[filename] = (offset ^ key, length ^ key)
    return index


def filter_index(index: dict, masks: list):
    if not masks:
        return index
    return {
        filename: data
        for filename, data in index.items()
        if any(_match(filename, mask) for mask in masks)
    }


def _match(filename: str, mask: str) -> bool:
    return fnmatch(filename, mask) or fnmatch(Path(filename).name, mask)


def extract_file(infile: BinaryIO, output_path: Path, file_data: tuple) -> None:
    offset, length = file_data
    with open(output_path, "wb") as out_file:
        infile.seek(offset)
        data = infile.read(length)
        out_file.write(data)


def unpack_rpa(infile: BinaryIO, index: dict, target_path: Path) -> int:
    total = 0
    unique_dirs = {target_path / Path(filename).parent for filename in index}
    for directory in unique_dirs:
        directory.mkdir(parents=True, exist_ok=True)
    for filename, file_data in index.items():
        output_file = target_path / filename
        extract_file(infile, output_file, file_data)
        total += 1
    return total
