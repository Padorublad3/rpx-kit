import argparse
from pathlib import Path
from .core import read_index,unpack_rpa,filter_index
from time import time
from rpx_kit import __version__
import sys


def validate_input_path(path:str) -> list[Path]:
    path_obj = Path(path)
    if path_obj.is_file() and path_obj.suffix.lower() == ".rpa":
        return [path_obj]
    elif path_obj.exists() and path_obj.is_dir():
        result = scan_folder(path_obj)
        if not result:
            print(f"Warning! No RPA archives found in {path}",file=sys.stderr)
            return []
        else:
            return result
    else:
        print(f"Not a valid RPA file or directory: {path}",file=sys.stderr)
        return []


def validate_output_path(path:str) -> Path:
    path_obj = Path(path)
    if path_obj.exists() and not path_obj.is_dir():
        raise argparse.ArgumentTypeError(f"Output path exists but is not a directory: {path}")
    else:
        return path_obj


def scan_folder(path_obj:Path) -> list[Path]:
    scan = list(path_obj.rglob("*.rpa"))
    return scan


parser = argparse.ArgumentParser()


parser.add_argument(
    "input_paths",
    nargs="*",
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


parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}"
)


def main():
    args = parser.parse_args()
    if not args.input_paths:
        raise argparse.ArgumentTypeError("No paths provided")
    input_paths = [validate_input_path(path) for path in args.input_paths]
    if input_paths:
        archives = [path for paths in input_paths for path in paths]
        print(f"{len(archives)} archives found")
    else:
        raise argparse.ArgumentTypeError("No valid paths provided")
    start_time = time()    
    for archive in archives:
        print(f"Processing {archive}, total size = {round(archive.stat().st_size /(1024 * 1024),2) } MB")
        with open(archive,"rb") as file:
            try:
                index = read_index(file)
            except Exception as e:
                print(f"Skip {archive}, error: {e}",file=sys.stderr)
                continue
            if args.masks:
                index = filter_index(index,args.masks)
                if not index:
                    print(f"No files match the given mask in {archive}")
                    continue
            if args.list:
                for filename in sorted(index.keys()):
                    print(f"{filename}")
            else:
                if args.output_path is None:
                    parser.error("-o/--output is required when unpacking")
                output_dir = args.output_path / archive.stem
                output_dir.mkdir(parents=True,exist_ok=True)
                total = unpack_rpa(file,index,output_dir)
                
                print(f"Done, {archive} processed")
                print(f"Total files extracted: {total}")
    end_time = time() 
    print(f"Time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
