import os
import shutil
import sys
from typing import List, Set, Dict

file_types_mapping: Dict[str, str] = {}


def escape_chars(filename: str) -> str:
    """Escapes characters such as space, quotes etc.

    Args:
        filename (str): [description]

    Returns:
        str: [description]
    """

    split_filename: List[str] = filename.split()
    for i in range(len(split_filename)):
        split_filename[i] = "\\'".join(split_filename[i].split("'"))
        split_filename[i] = '\\"'.join(split_filename[i].split('"'))
        split_filename[i] = "\\(".join(split_filename[i].split('('))
        split_filename[i] = "\\)".join(split_filename[i].split(')'))
    
    return "\\ ".join(split_filename)

def get_distinct_file_types(directory_path: str) -> Set[str]:
    """Gets distinct file types.

    Args:
        directory_path (str): [description]

    Returns:
        Set[str]: [description]
    """

    directory_contents: List[str] = os.listdir(path=directory_path)
    file_types: Set[str] = set()

    for content in directory_contents:
        escaped_content_name: str = escape_chars(filename=content)
        content_abs_path = directory_path + "/" + content

        if os.path.isfile(content_abs_path):
            content_info: str = os.popen(f"file --mime-type {escape_chars(directory_path) + '/' + escaped_content_name}").read()
            content_mimetype: str = "_".join(content_info.split()[-1].split("/"))
            file_types.add(content_mimetype)
            file_types_mapping[content] = directory_path + "/" + content_mimetype
    
    return file_types


def create_directories(directory_path: str, file_types: Set[str]):
    """Creates directories corresponding to the file_types

    Args:
        directory_path (str): [description]
        file_types (Set[str]): [description]
    """

    for file in file_types:
        try:
            os.mkdir(directory_path + "/" + file)
        except FileExistsError:
            continue
        except OSError as e:
            print(str(e))
            cleanup(directory_path=directory_path, file_types=file_types)
            sys.exit(1)


def organize_files(directory_path: str, file_types: Set[str]):
    """Organizes the files.

    Args:
        directory_path (str): [description]
        file_types (Set[str]): [description]
    """

    for f in file_types_mapping:
        try:
            os.rename(directory_path + "/" + f, file_types_mapping[f] + "/" + f)
        except FileExistsError:
            continue
        except OSError as e:
            print(str(e))
            cleanup(directory_path=directory_path, file_types=file_types)
            sys.exit(1)


def cleanup(directory_path: str, file_types: Set[str]):
    """Cleans up in case of error.

    Args:
        directory_path (str): [description]
        file_types (Set[str]): [description]
    """

    for f in file_types:
        try:
            shutil.rmtree(directory_path + "/" + f)
        except Exception:
            continue


if __name__ == "__main__":

    while True:
        directory_path: str = input("Enter absolute path of directory you want to organize: ").strip()

        if not os.path.isabs(directory_path):
            print("Please enter absolute path")
        
        else:
            break
    
    file_types: Set[str] = get_distinct_file_types(directory_path=directory_path)
    create_directories(directory_path=directory_path, file_types=file_types)
    organize_files(directory_path=directory_path, file_types=file_types)