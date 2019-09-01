import os
import re
from pathlib import Path
import requests
import zipfile
import platform

from videokf.utils.all_utils import make_dir, url_retrieve


def get_ff(type, dir=None):
    """Gets ffmpeg or ffprobe executables, either from an env var, from dir or downloading it.

    Args:
        type (str): Choose what url file to return. Either 'ffmpeg' or 'ffprobe'.
        dir(str): Directory from where to read the executable or where to download it.

    Returns:
        tuple(str): Tuple with ffmpeg path file.

    """
    save_dir = get_default_dir(dir)

    # Get urls
    url = choose_url(type)

    # Get files or download them
    ff = get_executable(type, save_dir, url)

    return str(ff)


def get_executable(file_name, dir, url):
    """Gets an executable file after checking if it's an env variable and if it's in dir.

    First, it will be checked if file_name is an environmental variable.
    If that it False, it will be checked if the file is in dir.
    If this fails, the file will be downloaded and saved in dir.

    Args:
        file_name (str): File to check.
        dir (str): Directory to check and where to save the file in case of download.
        url (str): Url from where to download the file.

    Returns:
        str: Full path of the file.

    """
    return check_environ_var(file_name.upper()) or \
           check_if_file_exists(file_name, dir) or \
           download_and_unzip(url, dir, file_name)


def check_environ_var(var):
    """Checks if an environmental variable is present or not and returns it.

    Args:
        var (str): Environmental variable to check.

    Returns:
        str or None: Full path of the environmental variable, it it exists. It returns None, if the variable doesn't
                     exist.

    """
    return os.environ.get(var)


def check_if_file_exists(file, dir):
    """Checks if a file exists in a directory and returns its full path if it does exist.

    Args:
        file (str): Full path of the file to check.
        dir (str): Directory to check for the existence of the file.

    Returns:
        str: Full path of the file if it exists. It returns None, if the file doesn't exist.

    """
    my_file = dir / Path(file)
    if my_file.is_file():
        return my_file.absolute()

    # Check windows case with .exe extension
    my_file = my_file.with_suffix(".exe")
    if my_file.is_file():
        return my_file.absolute()


def download_and_unzip(url, dir, file_name, remove_zip=True):
    """Downloads a zip file, unzips it and removes the zip file if the flag is true.

    Args:
        url (str): Url of the zip file to download.
        dir (str): Directory to extract the zip file to.
        file_name (str): File name to extract from inside the zip file.
        remove_zip (bool): If True, it removes the zip file after unzipping it.

    """
    file_name = Path(file_name)

    print(f"Downloading {file_name} ...")
    zip_file = Path(dir) / "temp_file.zip"
    url_retrieve(url, zip_file)
    print("Download complete")

    with zipfile.ZipFile(zip_file) as f:
        # List all files inside zip file
        file_list = f.namelist()

        # Match files with 'file_name' pattern
        match_list = [re.match(f"{file_name.name}(.exe)*", x) for x in file_list]

        # Get file that matched the pattern.
        # If file not matched, return None, which will prompt an error during extraction
        save_file = next((item.string for item in match_list if item is not None), None)

        # Extract the file
        f.extract(save_file, dir)

    if remove_zip:
        Path(zip_file).unlink()

    return Path(dir) / save_file


def choose_url(type):
    """Chooses which url to download ffmpeg and ffprobe from based on the operating system.

    Args:
        type (str): Choose what url file to return. Either 'ffmpeg' or 'ffprobe'.

    Returns:
        tuple(str): Tuple of two elements: the first one is the url of ffmpeg and the second one of ffprobe.

    """
    # Download urls information
    url_api = "https://ffbinaries.com/api/v1/version/latest"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/50.0.2661.102 Safari/537.36"}
    result = requests.get(url_api, headers=headers).json()["bin"]

    # Find operating system and architecture
    system = platform.system()
    architecture, _= platform.architecture()

    if system == "Windows" and architecture == "64bit":
        url = result["windows-64"]
    elif system == "Windows" and architecture == "32bit":
        url = result["windows-32"]
    elif system == "Linux" and architecture == "64bit":
        url = result["linux-64"]
    elif system == "Linux" and architecture == "32bit":
        url = result["linux-32"]
    elif system == "Darwin":
        url = result["osx-64"]
    else:
        print("There was an error while detecting your operating system! Please, download ffmpeg and ffprobe manually.")

    return url[type]


def set_default_dir():
    """Sets the default directory where ffmpeg and ffprobe will be searched and download, if not found.

    Args:
          dir(str): Directory from where to read the executable or where to download it.

    """
    return Path.home()


def get_default_dir(dir=None):
    """Gets the path of the default directory where ffmpeg and ffprobe will be searched and donwload, if not found.

    It will create the directory, if it doesn't exist.

    Args:
          dir(str): Directory from where to read the executable or where to download it.

    """
    if dir is None:
        dir = set_default_dir()

    return make_dir("Ffmpeg", dir)




if __name__ == "__main__":
    get_ff("ffmpeg")