# Quick guide
## Installation
    pip install video-kf
## Usage
Open a command line, or a terminal, from the same directory where your video is located and run:
    
    video-kf "My_video.mp4"
    
If the command line was open in a different directory from where the video is located, then the full path would be 
needed.

# Extended documentation
Video-kf is a Python package that can be run either from the command line, or from inside Python, by importing it.
It extracts the most relevant keyframes of a video, based on different methods.

At the moment, there are 3 methods available:

- **iframes**: it extracts the [iframes](https://en.wikipedia.org/wiki/Video_compression_picture_types) of the video, 
calculated by ffmpeg. This is the default option.

    Use in the command line:

    ```
    video-kf "My_video.mp4"
    ```
    
    or
    
    ```
    video-kf "My_video.mp4" -m "iframes"
    ```
        
    Use inside Python:
    
    ```python
    import videokf as vf
    
    vf.extract_keyframes("My_video.mp4")
    ```
    
    or
    
    ```python
    import videokf as vf
    
    vf.extract_keyframes("My_video.mp4", method="iframes")
    ```

- **color**: it returns the average frame, based on color, of every shot sequence. Shot sequences are group of frames 
that start with an iframe.

    Use in the command line:
    
    ```
    video-kf "My_video.mp4" -m "color"
    ```
            
    Use inside Python:
    
    ```python
    import videokf as vf
    
    vf.extract_keyframes("My_video.mp4", method="color")
    ```

- **flow**: it returns the most still frame with respect of the previous frame of every shot sequence. Shot sequences 
are group of frames that start with an iframe.
 
    Use in the command line:
    
    ```
    video-kf "My_video.mp4" -m "flow"
    ```
        
    Use inside Python:
    
    ```python
    import videokf as vf
    
    vf.extract_keyframes("My_video.mp4", method="flow")
    ```

### Caution

The methods *color* and *flow* **will download all the frames** of the video. Keep in mind that if the video is long, 
this will take time, as well as space to save the frames.

This is not the case for the method *iframes* that will only download the iframes.

## Use of Ffmpeg and Ffprobe
Video-kf automatically downloads the executable files of *ffmpeg* and *ffprobe* and saves them, by default, in a 
folder called "Ffmpeg" located in your *home* directory. You can choose to save the executable files in a different 
location by running:

```
video-kf "My_video.mp4" -dir "PATH_RO_A_DIFFERENT_LOCATION"
```

If you already have *ffmpeg* or *ffprobe* installed, you can also use your own executable files. There are various ways 
of doing this, all of them equivalent. Choose the one that best suits you:

- Using the command line options *ffmpeg* and *ffprobe* (you can choose to use just one of the two):
    
    ```
    video-kf "My_video.mp4" -ffmpeg "PATH_TO_FFMPEG" -ffprobe "PATH_TO_FFPROBE"
    ```

- Saving *ffmpeg* and *ffprobe* as environmental variables named respectively FFMPEG and FFPROBE.
- Saving manually *ffmpeg* and *ffprobe* in the folder called "Ffmpeg", which by default is located in your *home* 
directory, and running the program normally (either in the command line or inside python). You can also choose a 
different directory through the command line with the ```-dir``` option

# Command line options
    positional arguments:
      video_file            Path to the video file to extract the keyframes from.
    
    optional arguments:
      -h, --help            show this help message and exit
      -m METHOD, --method METHOD
                            Method to extract the keyframes
      -o OUTPUT_DIR_KEYFRAMES, --output_dir_keyframes OUTPUT_DIR_KEYFRAMES
                            Directory where to extract keyframes. If it is a
                            string instead of a directory, keyframes will be saved
                            in a folder named as this string, located in the same
                            directory of the video
      -ffmpeg FFMPEG, --ffmpeg FFMPEG
                            Path to the Ffmpeg executable
      -ffprobe FFPROBE, --ffprobe FFPROBE
                            Path to the Ffprobe executable
      -dir DIR_FFMPEG_FFPROBE, --dir_ffmpeg_ffprobe DIR_FFMPEG_FFPROBE
                            Path to the directory containing both Ffmpeg and
                            Ffprobe executables
      --no-frames-rm        If present, this option will NOT remove the directory
                            with the extracted frames, if they were extracted
                            (only for 'color' and 'flow' methods)

### References

FFmpeg Developers. (2016). Ffmpeg tool [Software].
Available from http://ffmpeg.org/

Binaries obtained from: https://ffbinaries.com/readme
 