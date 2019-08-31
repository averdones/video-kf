from videokf.utils.all_utils import copy_keyframes_from_frames
from videokf.utils.vidutils import extract_frames, get_iframes, get_keyframes_color, get_keyframes_flow


# Valid extraction methods
VALID_METHODS = ["iframes", "color", "flow"]


def get_keyframes(ffmpeg_exe, ffprobe_exe, video_file, method="iframes", output_dir="keyframes",
                  remove_frames_dir=True):
    """Computes the indices of the most relevant frames (keyframes) of the video.

    There are 3 available methods to compute the keyframes:
        - iframes: the keyframes are directly the iframes of the video.
        - color: the keyframes are selected as the frames with the most common colors in each sequence (each
                 sequence starts at each iframe).
        - flow: the keyframes are selected as the most still frames, compared with the previous one, in each
                sequence (each sequence starts at each iframe).

    The "iframes" method is the fastest one and the only one that doesn't require the extraction of all the frames
    in the video. Instead, only the frames corresponding to the iframes will be extracted.

    For the rest of the methods (currently "color" and "flow"), it is necessary to extract all frames of the video
    because they make use of image information.

    Args:
        ffmpeg_exe (str): ffmpeg executable.
        ffprobe_exe (str): ffprobe executable.
        video_file (str): Path to the video file.
        method (str): Flag to choose between the different methods to select the keyframes. The possible flags are
                      "iframes", "color" and "flow".
        output_dir (str): It can be either a full directory path where the keyframes will be stored, or a string, in
                          which case, a folder with this name will be created in the same directory of the video and
                          the keyframes will be saved there.
        remove_frames_dir (bool): If True, it removes the folder containing all the frames, after it has been used.

    Returns:

    """
    if method not in VALID_METHODS:
        print("Invalid method! Please select one of the following 3:")
        for m in VALID_METHODS:
            print(f" - {m}")

        return

    # Calculate the iframe indices of the video
    iframes = get_iframes(ffprobe_exe, video_file)

    # Compute the keyframe indices using the selected method
    if method=="iframes":
        extract_frames(ffmpeg_exe, video_file, frames_selected=iframes, output_dir=output_dir, frame_type=method)
    else:
        # For the rest of the methods it is necessary to extract all the frames in the video
        # Extract the frames and store the directory where the frames are saved as a variable
        frames_dir = extract_frames(ffmpeg_exe, video_file)

        # Extract the keyframes indices
        if method=="color":
            keyframes = get_keyframes_color(iframes, frames_dir)
        elif method == "flow":
            keyframes = get_keyframes_flow(iframes, frames_dir)

        # Copy selected keyframes and remove frames directory (if selected)
        copy_keyframes_from_frames(frames_dir, keyframes, name_dir=output_dir, remove_frames_dir=remove_frames_dir)
