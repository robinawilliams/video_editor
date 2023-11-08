import os
import argparse
import logging
from moviepy.editor import VideoFileClip

# Configure the logging settings
logging.basicConfig(filename='../audio_normalizer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def normalize_audio(input_path, output_path, volume_multiplier):
    try:
        clip = VideoFileClip(input_path)
        normalized_clip = clip.volumex(volume_multiplier)  # Normalize the audio

        # Save the video with normalized audio to the same folder as the original video
        normalized_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Log success
        logging.info(f"Audio normalized for {input_path} and saved as {output_path}")
        print(f"Audio normalized for {input_path} and saved as {output_path}")

        return output_path
    except Exception as e:
        # Log any errors that occur during processing
        logging.error(f"Error processing {input_path}: {str(e)}")
        print(f"Error processing {input_path}: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Normalize the audio of a video.")
    parser.add_argument("-v", type=float, required=True,
                        help="Volume multiplier for audio normalization (e.g., 1.0 for no change, Anything less than "
                             "1.0 will equalize the audio.)")
    parser.add_argument("-i", type=str, help="Input video file path")
    parser.add_argument("-f", type=str, help="Input file containing a list of video file paths")
    parser.add_argument("-o", type=str, help="Output location for the videos with normalized audio")

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
        output_path = os.path.join(output_dir, f'{filename}_NORMALIZED{args.v}{extension}')

        if args.o:
            output_path = os.path.join(args.o, os.path.basename(output_path))

        new_video_path = normalize_audio(input_path, output_path, args.v)

        if new_video_path:
            print(f"Audio normalized for {input_path} and saved as {new_video_path}")


if __name__ == "__main__":
    main()
