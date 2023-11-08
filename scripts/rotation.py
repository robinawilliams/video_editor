import os
import argparse
import logging
from moviepy.editor import VideoFileClip

# Configure the logging settings
logging.basicConfig(filename='rotation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def rotate_video(input_path, output_path, rotation_angle):
    try:
        clip = VideoFileClip(input_path)
        rotated_clip = clip.rotate(rotation_angle)  # Rotate the video by the specified angle

        # Save the rotated video to the same folder as the original video
        rotated_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        # Log success
        logging.info(f"Clip rotated for {input_path} and saved as {output_path}")
        print(f"Clip rotated for {input_path} and saved as {output_path}")

        return output_path
    except Exception as e:
        # Log any errors that occur during processing
        logging.error(f"Error processing {input_path}: {str(e)}")
        print(f"Error processing {input_path}: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Rotate a video by 90 degrees left or right.")
    parser.add_argument("-r", type=str, required=True, choices=["left", "right"],
                        help="Rotation direction (left or right)")
    parser.add_argument("-i", type=str, help="Input video file path")
    parser.add_argument("-f", type=str, help="Input file containing a list of video file paths")
    parser.add_argument("-o", type=str, help="Output location for the rotated videos")

    args = parser.parse_args()
    rotation_angle = 90 if args.r == "left" else -90  # Rotate left: 90 degrees, Rotate right: -90 degrees

    if args.i and args.f:
        logging.error("Error: Both input video and input file specified. Please choose one.")
        print("Error: Both input video and input file specified. Please choose one.")
        return

    if not args.i and not args.f:
        logging.error("Error: Either input video or input file must be specified.")
        print("Error: Either input video or input file must be specified.")
        return

    if args.i:
        input_paths = [args.i]
    else:
        with open(args.f, 'r') as file:
            input_paths = [line.strip() for line in file]

    for input_path in input_paths:
        filename, extension = os.path.splitext(os.path.basename(input_path))
        output_dir = os.path.dirname(input_path)
        output_path = os.path.join(output_dir, f'{filename}_ROTATED{args.r}{extension}')

        if args.o:
            output_path = os.path.join(args.o, os.path.basename(output_path))

        new_video_path = rotate_video(input_path, output_path, rotation_angle)
        if new_video_path:
            print(f"Video rotated {args.r} for {input_path} and saved as {new_video_path}")


if __name__ == "__main__":
    main()
