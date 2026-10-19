import argparse
from pathlib import Path
from .core import read_index,unpack_rpa,filter_index
from time import time
from sys import exit


def validate_input_path(path:str) -> Path:
    path_obj = Path(path)
    if path_obj.is_file() and path_obj.suffix.lower() == ".rpa":
        return path_obj
    else:
        raise argparse.ArgumentTypeError("Invalid path")


def validate_output_path(path:str) -> Path:
    path_obj = Path(path)
    if path_obj.exists() and not path_obj.is_dir():
        raise argparse.ArgumentTypeError(f"Output path exists but is not a directory: {path}")
    else:
        return path_obj


parser = argparse.ArgumentParser()


parser.add_argument(
    "input_path",
    type=validate_input_path,
    help="Path to the RPA-3.0 archive"
)


parser.add_argument(
    "-o",
    "--output",
    dest="output_path",
    type=validate_output_path,
    help="Output path"
)


parser.add_argument(
    "-l",
    "--list",
    action="store_true",
    help="Prints a list of files inside the archive"

)


parser.add_argument(
 "-m",
 "--mask",
 action="append",
 dest = "masks",
 default=None,
help="Filter by mask, can be repeated: -m '*.rpyc' -m '*.png'"
)


def main():
    args = parser.parse_args()
    with open(args.input_path,"rb") as file:
        index = read_index(file)
        if args.masks:
            index = filter_index(index,args.masks)
            if not index:
                print("No files match the given mask")
                exit(0)
        if args.list:
            for filename in index:
                print(filename)
        else:
            if args.output_path is None:
                parser.error("-o/--output is required when unpacking")
            start_time = time()
            args.output_path.mkdir(parents=True,exist_ok=True)
            total = unpack_rpa(file,index,args.output_path)
            end_time = time()
            print("Done")
            print(f"Total files extracted: {total}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()