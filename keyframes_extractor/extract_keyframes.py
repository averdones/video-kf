import argparse

from keyframe_manager.keyframe_extractor import get_keyframes
from ffmpeg_manager.check_ffmpeg import get_ffmpeg_and_ffprobe


def main(video_file, method, output_dir_keyframes="keyframes", dir_exe=None, ffmpeg_exe=None, ffprobe_exe=None):
    """

    Args:
        video_file (str): Path to the video file.
        method (str): Flag to choose between the different methods to select the keyframes. The possible flags are
                      "iframes", "color" and "flow".
        output_dir_keyframes (str): It can be either a full directory path where the keyframes will be stored, or a
                                    string, in which case, a folder with this name will be created in the same
                                    directory of the video and the keyframes will be saved there.
        dir (str): Directory from where to read the executables or where to download them. By default, it is a folder
                   called 'FFmpeg' in the home directory. It won't be used if both ffmpeg_exe and ffprobe_exe are given.
        ffmpeg_exe (str): Path to the ffmpeg executable.
        ffprobe_exe (str): Path to the ffprobe executable.

    Returns:

    """
    # Get ffmpeg and ffprobe
    if ffmpeg_exe is None or ffprobe_exe is None:
        ffmpeg_exe, ffprobe_exe = get_ffmpeg_and_ffprobe(dir_exe)

    # Extract frames
    get_keyframes(ffmpeg_exe, ffprobe_exe, video_file, method, output_dir_keyframes)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Extracts keyframes from a video.")
    parser.add_argument("-ffmpeg", "--ffmpeg", type=str, help="Path to the Ffmpeg executable.")
    parser.add_argument("-ffprobe", "--ffprobe", type=str, help="Path to the Ffprobe executable.")
    parser.add_argument("-dir", "--dir_ffmpeg_ffprobe", type=str, help="Path to the directory containing both Ffmpeg "
                                                                       "and Ffprobe executables.")
    parser.add_argument("-v", "--video_file", type=str, help="Path to the video file to extract the keyframes from.")
    parser.add_argument("-m", "--method", type=str, default="iframes", help="Method to extract the keyframes.")
    parser.add_argument("-o", "--output_dir_keyframes", type=str, default="keyframes", help="Directory where to "
                        "extract keyframes. If it is a string instead of a directory, keyframes will be saved in a "
                        "folder named as this string, located in the same directory of the video.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.video_file, args.method, args.output_dir_keyframes, args.dir_ffmpeg_ffprobe, args.ffmpeg, args.ffprobe)
    # main("D:/My_projects/Python_projects/video_tldr/test_videos/ny/ny.mp4", "color")
