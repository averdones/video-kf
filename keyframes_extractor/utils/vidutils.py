import os
from pathlib import Path
import subprocess
import numpy as np
import cv2

from keyframes_extractor.utils.all_utils import make_dir, make_frames_list
from keyframes_extractor.keyframe_manager.frame_manager import Frame, calculate_stillness


def extract_frames(ffmpeg_exe, video_file, frames_selected=None, output_dir="frames", frame_quality=1):
    """Extracts the frames in a video and saves them in a (possibly) new directory.

    It can extract only some specific frames specified by their index.

    Args:
        ffmpeg_exe (str): ffmpeg executable.
        video_file (str): Path of the video from which to extract the frames.
        frames_selected (list): Select which frames to extract. By default (None), it extracts all frames in the video.
        output_dir (str): It can be either a full directory path where the frames will be stored, or a string, in which
                          case, a folder with this name will be created in the same directory of the video and the
                          frames will be saved there.
        frame_quality (str or int): Quality in which the frames will be saved. The lower the number, the higher the
                                    quality (and the heavier the file). By default 1, which is the highest quality
                                    (negative numbers are equivalent to 1).

    Returns:
        str: Directory where the frames have been stored.

    """
    if Path(output_dir).is_dir():
        frames_dir = Path(output_dir).mkdir(exist_ok=True)
    else:
        frames_dir = make_dir(output_dir, Path(video_file).parent)

    # Extract frames only if directory is empty
    if len(os.listdir(frames_dir)) == 0:
        if frames_selected is None:
            # Extract all frames
            ffmpeg_args = [ffmpeg_exe, "-hide_banner", "-i", video_file, "-q:v", str(frame_quality),
                           str((frames_dir / "%d").with_suffix(".jpg"))]
        else:
            # Extract only selected frames
            ffmpeg_args = [ffmpeg_exe, "-i", video_file, "-vf", make_frames_list(frames_selected), "-vsync", "0",
                           "-q:v", str(frame_quality), "-frame_pts", "1", str((frames_dir / "%d").with_suffix(".jpg"))]

        subprocess.check_output(ffmpeg_args)

        print("Frames successfully extracted.")
    else:
        print("!!! The output directory is not empty. No frames were extracted. !!!")

    return frames_dir


def get_iframes(ffprobe_exe, video_file):
    """Get the iframe indices of a video using ffprobe.

    Args:
        ffprobe_exe (str): ffprobe executable.
        video_file (str): Path of the video from which to get the iframe indices.

    Returns:
        list: List of iframes in the video.

    """
    # Run ffprobe
    ffprobe_args = [ffprobe_exe, "-i", video_file, "-loglevel", "error", "-select_streams", "v",
                    "-show_frames", "-show_entries", "frame=pict_type", "-of", "csv=print_section=0"]
    ffprobe_output = subprocess.check_output(ffprobe_args)

    # Count the number of type I (iframes) and save their indices
    iframes = []
    for i, line in enumerate(ffprobe_output.decode("utf8").splitlines()):
        if line == "I":
            iframes.append(i)

    return iframes


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

# Methods for extracting the keyframes of a video using the extracted frames and image information (color, flow, etc.)

def get_keyframes_color(iframes, frames_dir):
    """Method to compute the most relevant frame (keyframe) on each shot sequence, based on color histogram.

    The iframes mark the start of every shot sequence. For every shot sequence, one frame is selected as new
    keyframe.

    The selected keyframe is the frame whose color histogram is closer to the average of the color
    histograms of all the frames in the sequence shot.

    Args:
        iframes (list): List with all the iframes in the video.
        frames_dir (str): Directory where all the frames of the video are stored (extracted previously).

    Returns:
        list: List of all relevant keyframes indices in the video, one for each sequence.

    """
    keyframes = [None] * (len(iframes) - 1)

    # Loop through all the sequences
    for i in range(len(iframes) - 1):
        all_hist = []
        for j in range(iframes[i], iframes[i + 1]):
            frame = Frame(j, frames_dir)
            all_hist.append(frame.histogram)

        all_hist = np.array(all_hist)
        color_mean = np.mean(all_hist, axis=0)

        # Find closest frame to average frame
        min_corr = -1
        # Initialize so it doesn't error in case program doesn't go inside if statement
        min_idx = j
        for h in range(all_hist.shape[0]):
            corr = cv2.compareHist(all_hist[h], color_mean, cv2.HISTCMP_CORREL)
            if corr >= min_corr:
                min_corr = corr
                min_idx = h

        # Add new keyframe index
        keyframes[i] = iframes[i] + min_idx

    return keyframes


def get_keyframes_flow(iframes, frames_dir):
    """Method to compute the most relevant frame (keyframe) on each shot sequence, based on optical flow.

    The iframes mark the start of every shot sequence. For every shot sequence, one frame is selected as new
    keyframe.

    The selected keyframe is the most still frame in the shot sequence, compared with its previous frames.

    Args:
        iframes (list): List with all the iframes in the video.
        frames_dir (str): Directory where all the frames of the video are stored (extracted previously).

    Returns:
        list: List of all relevant keyframes indices in the video, one for each sequence.

    """
    keyframes = [None] * (len(iframes) - 1)

    # Loop through all the sequences
    for i in range(len(iframes) - 1):
        # Load first frame of the sequence
        frame_prev = Frame(iframes[i], frames_dir, extract_features=True)

        # Loop through the rest of the frames in the sequence
        min_motion = np.Inf
        min_motion_idx = iframes[i]
        for j in range(iframes[i] + 1, iframes[i + 1]):
            frame = Frame(j, frames_dir, extract_features=True)

            # Calculate motion difference
            motion = calculate_stillness(frame, frame_prev)

            # Compute frame with minimum motion, if motion is not None
            # Motion is None only if previous frame has no features (eg.: black frame, i.e. no corners)
            if motion is not None and motion < min_motion:
                min_motion = motion
                min_motion_idx = j

            frame_prev = frame

        keyframes[i] = min_motion_idx

    return keyframes
