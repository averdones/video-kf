from videokf.ffmpeg_manager.check_ffmpeg import get_ffmpeg, get_ffprobe
from videokf.keyframe_manager.keyframe_extractor import get_keyframes


def extract_keyframes(video_file, method="iframes", output_dir_keyframes="keyframes", dir_exe=None, ffmpeg_exe=None,
                      ffprobe_exe=None):
    """

    Args:
        video_file (str): Path to the video file.
        method (str): Flag to choose between the different methods to select the keyframes. The possible flags are
                      "iframes", "color" and "flow".
        output_dir_keyframes (str): It can be either a full directory path where the keyframes will be stored, or a
                                    string, in which case, a folder with this name will be created in the same
                                    directory of the video and the keyframes will be saved there.
        dir_exe (str): Directory from where to read the executables or where to download them. By default, it is a
                       folder called 'FFmpeg' in the home directory. It won't be used if both ffmpeg_exe and
                       ffprobe_exe are given.
        ffmpeg_exe (str): Path to the ffmpeg executable.
        ffprobe_exe (str): Path to the ffprobe executable.

    Returns:

    """
    # Get paths to ffmpeg and ffprobe executables
    if ffmpeg_exe is None:
        ffmpeg_exe = get_ffmpeg(dir_exe)

    if ffprobe_exe is None:
        ffprobe_exe = get_ffprobe(dir_exe)

    # Extract frames
    get_keyframes(ffmpeg_exe, ffprobe_exe, video_file, method, output_dir_keyframes)
