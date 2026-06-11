import argparse
import os
import shutil

from star_manager.core.zipmod_utils import (
    ERROR_CORRUPTED,
    ERROR_NO_MANIFEST,
    ERROR_NO_VALUE,
    ERROR_OTHER,
    find_zipmod_files,
    generate_zipmod_filename,
    get_manifest_value,
    remove_empty_dirs,
)


def safe_move(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    filename = os.path.basename(src)
    base, ext = os.path.splitext(filename)
    dest_path = os.path.join(dst_dir, filename)
    counter = 1

    while os.path.exists(dest_path):
        dest_path = os.path.join(dst_dir, f"{base}_{counter}{ext}")
        counter += 1

    shutil.move(src, dest_path)
    return dest_path


def sort_zipmod(file_path, sort_dir, error_dirs):
    author = get_manifest_value(file_path, "author")
    error_targets = {
        ERROR_NO_MANIFEST: error_dirs["no_manifest"],
        ERROR_NO_VALUE: error_dirs["no_author"],
        ERROR_CORRUPTED: error_dirs["corrupted"],
        ERROR_OTHER: error_dirs["other_error"],
    }

    if author in error_targets:
        safe_move(file_path, error_targets[author])
        return

    target_dir = os.path.join(sort_dir, author)
    os.makedirs(target_dir, exist_ok=True)

    name = get_manifest_value(file_path, "name")
    if name == ERROR_NO_VALUE:
        name = None

    target_path = generate_zipmod_filename(target_dir, author, name)
    shutil.move(file_path, target_path)


def sort_mods(input_dir, output_dir=None, delete_empty=False):
    output_dir = output_dir or input_dir
    sort_dir = os.path.join(output_dir, "sort")
    error_dir = os.path.join(output_dir, "error")
    error_dirs = {
        "corrupted": os.path.join(error_dir, "corrupted"),
        "no_manifest": os.path.join(error_dir, "no_manifest"),
        "other_error": os.path.join(error_dir, "other_error"),
        "no_author": os.path.join(error_dir, "no_author"),
    }

    os.makedirs(sort_dir, exist_ok=True)
    for directory in error_dirs.values():
        os.makedirs(directory, exist_ok=True)

    zipmod_files = find_zipmod_files(input_dir)
    for zipmod_file in zipmod_files:
        sort_zipmod(zipmod_file, sort_dir, error_dirs)

    if delete_empty:
        remove_empty_dirs(input_dir, [sort_dir, error_dir])

    return len(zipmod_files)


def build_parser():
    parser = argparse.ArgumentParser(description="Sort and rename .zipmod files by manifest.xml metadata.")
    parser.add_argument("directory", help="Input directory")
    parser.add_argument("-o", "--output", help="Output directory. Defaults to input directory.")
    parser.add_argument("-d", "--delete-empty", action="store_true", help="Delete empty folders after sorting.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not os.path.isdir(args.directory):
        parser.error(f"Directory does not exist: {args.directory}")

    count = sort_mods(args.directory, args.output, args.delete_empty)
    print(f"Processed {count} zipmod files.")


if __name__ == "__main__":
    main()
