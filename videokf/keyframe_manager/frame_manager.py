from pathlib import Path
import numpy as np
import cv2


class Frame:

    def __init__(self, idx, frames_dir, extract_features=False):
        """Initializes instance of class Frame.

        Args:
            idx (int): Index of the frame.
            frames_dir (str): Directory containing all frames.
            extract_features (bool): If True, it extracts the frame features when instance is initialized.

        """
        self.idx = idx
        self.frames_dir = frames_dir
        self.im = cv2.imread(str((Path(self.frames_dir) / str(self.idx + 1)).with_suffix(".jpg")))
        self.im_gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        self.features = None

        # Call the extract features method
        if extract_features:
            self.extract_features()

        self.histogram = calculate_histogram(self.im)

    def extract_features(self):
        """Extracts features from the frame."""
        # Parameters for ShiTomasi corner detection
        feature_params = {"maxCorners": 100, "qualityLevel": 0.3, "minDistance": 7, "blockSize": 7}
        self.features = cv2.goodFeaturesToTrack(self.im_gray, **feature_params)

    def show(self):
        """Plots the frame."""
        cv2.imshow("frame", self.im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def calculate_histogram(im):
    """Calculates color histogram.

    Args:
        im (array): Image from where to calculate the color histogram.

    Returns:
        array: Color histogram.

    """
    return cv2.calcHist([im], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])


def calculate_stillness(frame, prev_frame):
    """Calculates if a frame is still or if it has motion in it.

    Args:
        frame (obj Frame): Frame from where to extract the motion score.
        prev_frame (obj Frame): Previous frame from the one being scored.

    Returns:
        float: Positive number denoting the motion difference between the two frames.
               Higher means more motion difference. The minimum value is zero (no difference at all)

    """
    # Parameters for lucas kanade optical flow
    lk_params = {"winSize": (15, 15), "maxLevel": 2,
                 "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)}

    # If no feature found for a frame, just return None
    if prev_frame.features is not None:
        _, _, err = cv2.calcOpticalFlowPyrLK(prev_frame.im, frame.im, prev_frame.features, None, **lk_params)

        # Get average of errors as a final difference metric
        return np.nanmean(err)
    else:
        return None
