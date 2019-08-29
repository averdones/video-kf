import argparse

from extract_keyframes import extract_keyframes


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


def main():
    args = parse_arguments()
    e = extract_keyframes(args.video_file, args.method, args.output_dir_keyframes, args.dir_ffmpeg_ffprobe, args.ffmpeg,
                          args.ffprobe)
    e()
