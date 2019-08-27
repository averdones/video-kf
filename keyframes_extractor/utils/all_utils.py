import shutil
from pathlib import Path


def make_dir(new_dir, path):
    """Creates a directory if it doesn't exist.

    Args:
        new_dir (str): Name of the new directory to be created.
        path (str): Path where the new directory will be created.

    Returns:
        str: Path of the newly created directory.

    """
    new_path = path / Path(new_dir)
    new_path.mkdir(exist_ok=True)

    return new_path


def make_frames_list(frames):
    """Creates a string list in the appropriate format for ffmpeg to extract a specific set of frames.

    This function is used inside the extract_frames() function.

    Args:
        frames (list[int]): List of frame indices.

    Returns:
        str: String in the appropriate format for ffmpeg.

    """
    aux = "".join([f"eq(n\\,{x})+" for x in frames])[:-1]

    return f"select='{aux}'"


def copy_keyframes_from_frames(frames_dir, keyframes, name_dir="keyframes", remove_frames_dir=True):
    """Copy a set of frames from a folder containing all the frames in a video to a new location.

    The new directory will be located in the same folder of the frames folder.

    Args:
        frames_dir (str): Directory containing all the frames of the video (previously extracted).
        keyframes (list[int]): List of indices of the keyframes computed.
        name_dir (str): Name of the new directory that will be created to store the keyframes (if it doesn't already
                        exist). By default, it's called "keyframes".
        remove_frames_dir (bool): If True, it removes the folder containing all the frames, after it has been used.

    Returns:
         Directory where the keyframes have been copied.

    """
    # Create new directory if it doesn't already exist
    keyframes_dir = make_dir(name_dir, Path(frames_dir).parent)

    # Copy keyframes from frames directory
    for i in keyframes:
        filename = Path(str(i)).with_suffix(".jpg")
        shutil.copyfile(frames_dir / filename, keyframes_dir / filename)

    # Remove frames folder
    if remove_frames_dir:
        shutil.rmtree(frames_dir)
