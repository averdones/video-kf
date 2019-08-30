import os
from pathlib import Path
import urllib.request
import zipfile
import platform

from keyframes_extractor.utils.all_utils import make_dir


def get_ffmpeg_and_ffprobe(dir=None):
    """Gets both ffmpeg and ffprobe executables, either from an env var, from dir or downloading them.

    Args:
        dir(str): Directory from where to read the executables or where to download them.

    Returns:
        tuple(str): Tuple with ffmpeg and ffprobe path file, in this order.

    """
    # Set home as default directory
    if dir is None:
        dir = make_dir("Ffmpeg", Path.home())

    # Get urls
    ffmpeg_url, ffprobe_url = choose_url()

    # Get files or download them
    ffmpeg = get_executable("ffmpeg", dir, ffmpeg_url)
    ffprobe = get_executable("ffprobe", dir, ffprobe_url)

    return str(ffmpeg), str(ffprobe)


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
    my_file = dir / Path(file).with_suffix(".exe")
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
    zip_file, _ = urllib.request.urlretrieve(url, Path(dir) / "temp_file.zip")
    print("Download complete")

    with zipfile.ZipFile(zip_file) as f:
        f.extract(str(file_name.with_suffix(".exe")), dir)

    if remove_zip:
        Path(zip_file).unlink()

    return Path(dir) / file_name.with_suffix(".exe")


def choose_url():
    """Chooses which url to download ffmpeg and ffprobe from based on the operating system.

    Returns:
        tuple(str): Tuple of two elements: the first one is the url of ffmpeg and the second one of ffprobe.

    """
    system = platform.system()
    architecture, _= platform.architecture()

    if system == "Windows" and architecture == "64bit":
        ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1-win-64.zip"
        ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffprobe-4.1-win-64.zip"
    elif system == "Windows" and architecture == "32bit":
        ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1-win-32.zip"
        ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffprobe-4.1-win-32.zip"
    elif system == "Linux" and architecture == "64bit":
        ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1-linux-64.zip"
        ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffprobe-4.1-linux-64.zip"
    elif system == "Linux" and architecture == "32bit":
        ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1-linux-32.zip"
        ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffprobe-4.1-linux-32.zip"
    elif system == "Darwin":
        ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1.7-osx-64.zip"
        ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffprobe-4.1.7-osx-64.zip"
    else:
        print("Operating system not detected! Please, download ffmpeg and ffprobe manually.")

    return ffmpeg_url, ffprobe_url
