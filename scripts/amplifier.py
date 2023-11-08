import os
import argparse
import logging
from moviepy.editor import VideoFileClip

# Configure the logging settings
logging.basicConfig(filename='../amplifier.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def increase_volume(input_path, output_path, increase_db):
    try:
        clip = VideoFileClip(input_path)
        modified_clip = clip.volumex(10 ** (increase_db / 20.0))  # Convert dB to linear scale

        # Save the modified video to the same folder as the original video
        modified_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        # Log success
        logging.info(f"Audio amplified for {input_path} and saved as {output_path}")
        print(f"Audio amplified for {input_path} and saved as {output_path}")

        return output_path
    except Exception as e:
        # Log any errors that occur during processing
        logging.error(f"Error processing {input_path}: {str(e)}")
        print(f"Error processing {input_path}: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Increase the volume of a video by a specified number of decibels.")
    parser.add_argument("-db", type=float, required=True, help="Volume increase in decibels")
    parser.add_argument("-i", type=str, help="Input video file path")
    parser.add_argument("-f", type=str, help="Input file containing a list of video file paths")
    parser.add_argument("-o", type=str, help="Output location for the modified videos")

    args = parser.parse_args()

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
        output_path = os.path.join(output_dir, f'{filename}_INCREASED{args.db}{extension}')

        if args.o:
            output_path = os.path.join(args.o, os.path.basename(output_path))

        new_video_path = increase_volume(input_path, output_path, args.db)
        if new_video_path:
            print(f"Volume increased {args.db} for {input_path} and saved as {new_video_path}")


if __name__ == "__main__":
    main()
