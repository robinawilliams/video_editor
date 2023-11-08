# Video Editor

## A tool to automatically edit videos. 

## How to install this project

1. Clone this repo
2. Install dependencies - `pip install -r requirements.txt`

## How to run this project

1. python main.py \[command line arguments]

Command line arguments:
- `-db` - Volume increase in decibels
- `-r` - Rotate a video by 90 degrees left or right.
- `-v` - Normalize the audio
- `-i` - Input video file path, e.g., /home/user/videos
- `-f` - Input file containing a list of video file paths, e.g., /home/user/videos/video_paths.txt
- `-o` - Output location for the modified videos, e.g., /home/user/new_videos

Add lines to the video_paths.txt file, e.g.,
/home/user/videos/video1.mp4
/home/user/videos/video2.mp4
/home/user/videos/video3.mp4

Examples:
- python main.py -db 10 -i "/home/user/1.mp4"
- python main.py -db 10 -i "/home/user/1.mp4" -o "/home/user/"
- python main.py -db 10 -f /home/user/video_paths.txt
- python main.py -db 10 -f /home/user/video_paths.txt -o "/home/user/"


## Helpful Tools
List absolute filepaths:

- ls -d "$(pwd)"/*

- ls -d /path/to/your/directory/*

- ls -d /path/to/your/directory/* > video_paths.txt

List recursively:
- find "$(pwd)" -type f -exec ls -d {} \;

- find /path/to/your/directory -type f -exec ls -d {} \;

- find /path/to/your/directory -type f -exec ls -d {} \; > video_paths.txt

Just directories
- find /path/to/your/directory -type d > video_paths.txt

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

This is a work in progress. Known issues will go here.

## Like this project?

Please share it.

## FAQ

In progress.
