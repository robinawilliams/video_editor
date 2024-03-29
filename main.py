import os
import argparse
import logging
import sys
import shutil
from moviepy.editor import VideoFileClip

# Configure the logging settings
logging.basicConfig(filename='video_editor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_non_conflicting_filename(path):
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = path

    while os.path.exists(new_path):
        new_path = f"{base}_{counter}{ext}"
        counter += 1

    return new_path


def rotate_video(clip, rotation_angle):
    try:
        rotated_clip = clip.rotate(rotation_angle)  # Rotate the video by the specified angle
        return rotated_clip
    except Exception as e:
        logging.error(f"Error rotating video: {str(e)}")
        print(f"Error rotating video: {str(e)}")
        return None


def increase_volume(clip, increase_db):
    try:
        modified_clip = clip.volumex(10 ** (increase_db / 20.0))  # Convert dB to linear scale
        return modified_clip
    except Exception as e:
        logging.error(f"Error increasing volume: {str(e)}")
        print(f"Error increasing volume: {str(e)}")
        return None


def normalize_audio(clip, volume_multiplier):
    try:
        normalized_clip = clip.volumex(volume_multiplier)  # Normalize the audio
        return normalized_clip
    except Exception as e:
        logging.error(f"Error normalizing audio: {str(e)}")
        print(f"Error normalizing audio: {str(e)}")
        return None


def remove_successful_line_from_file(file_path, line_to_remove):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != line_to_remove:
                file.write(line)


def main():
    parser = argparse.ArgumentParser(description="Modify videos")
    parser.add_argument("-db", type=float, help="Volume increase in decibels")
    parser.add_argument("-r", type=str, choices=["left", "right"], help="Rotate a video by 90 degrees left or right.")
    parser.add_argument("-v", type=float, help="Volume multiplier for audio normalization (e.g., 1.0 for no change, "
                                               "Anything less than 1.0 will equalize the audio.)")
    parser.add_argument("-i", type=str, help="Input video file path")
    parser.add_argument("-f", type=str, help="Input file containing a list of video file paths")
    parser.add_argument("-o", type=str, help="Output location for the modified videos")

    args = parser.parse_args()

    # Create a list of valid video extensions
    valid_extensions = ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.mpeg', '.mpg', '.m4v']

    # Check if an input file containing a list of video file paths is provided
    if args.f:
        # Read the input file and filter out lines with non-video extensions
        with open(args.f, 'r') as file:
            input_paths = [line.strip() for line in file if
                           os.path.splitext(line.strip())[1].lower() in valid_extensions]

        # Overwrite the input file with the filtered paths
        with open(args.f, 'w') as file:
            file.write('\n'.join(input_paths))

    if (args.i or args.f) and args.db is None and args.r is None and args.v is None:
        logging.error(
            "Error: You need to specify an operation (audio increase, video rotation, audio normalization or"
            "a combination of an audio edit and a video edit with -db, -r, -v, -db/-r or -db/-v")
        print(
            "Error: You need to specify an operation (audio increase, video rotation, audio normalization or"
            "a combination of an audio edit and a video edit with -db, -r, -v, -db/-r or -db/-v")
        sys.exit(1)

    if args.i and args.f:
        logging.error("Error: Both input video and input file specified. Please choose one.")
        print("Error: Both input video and input file specified. Please choose one.")
        sys.exit(1)

    if not args.i and not args.f:
        logging.error("Error: Either input video or input file must be specified.")
        print("Error: Either input video or input file must be specified.")
        sys.exit(1)

    if args.i:
        input_paths = [args.i]
    else:
        with open(args.f, 'r') as file:
            input_paths = [line.strip() for line in file]

    for input_path in input_paths:
        try:
            # Check if the file name length exceeds 260 characters
            if len(os.path.basename(input_path)) > 254:
                logging.warning(f"File over 255 warning!!! Fix: {input_path}")
                temp_dir = os.path.dirname(input_path)
                temp_copy_path = os.path.join(temp_dir, 'temp_EXCEPTION.mp4')
                shutil.copyfile(input_path, temp_copy_path)

                filename, extension = os.path.splitext(os.path.basename(temp_copy_path))
                output_dir = os.path.dirname(temp_copy_path)

                operation_tags = []  # Initialize an empty list to keep track of operations

                # Determine the rotation operation tag
                if args.r:
                    rotation_tag = "ROTATED_" + args.r.upper()
                    operation_tags.append(rotation_tag)  # Add to the operations list
                    rotation_angle = 90 if args.r == "left" else -90
                else:
                    rotation_angle = None

                # Determine the volume increase operation tag
                if args.db:
                    volume_tag = f"INCREASED_{args.db}DB"
                    operation_tags.append(volume_tag)  # Add to the operations list

                # Determine the audio normalization operation tag
                if args.v:
                    normalization_tag = f"NORMALIZED_{args.v}"
                    operation_tags.append(normalization_tag)  # Add to the operations list

                # Join the operation tags with underscores to create a filename suffix
                operation_suffix = "_".join(operation_tags)

                # Create the output path with the operation suffix
                output_path = os.path.join(output_dir, f'{filename}_{operation_suffix}{extension}')

                if args.o:
                    output_path = os.path.join(args.o, os.path.basename(output_path))

                # Check if the output path already exists and get a non-conflicting name
                output_path = get_non_conflicting_filename(output_path)

                # Load the original video clip
                original_clip = VideoFileClip(temp_copy_path)
                successful_operations = True

                # Apply the operations in sequence, checking if they are successful
                if args.r and successful_operations:
                    processed_clip = rotate_video(original_clip, rotation_angle)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                if args.db and successful_operations:
                    processed_clip = increase_volume(original_clip, args.db)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                if args.v and successful_operations:
                    processed_clip = normalize_audio(original_clip, args.v)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                # Only write the final modified clip to the output path if all operations were successful
                if successful_operations:
                    original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    logging.info(f"Video {operation_suffix.lower()} saved as {output_path}")
                    print(f"Video {operation_suffix.lower()} saved as {output_path}")

                    # Remove the successfully processed line from the input file
                    if args.f:
                        remove_successful_line_from_file(args.f, input_path)
                else:
                    logging.error(f"Error: Operations failed for video {input_path}")
                    print(f"Error: Operations failed for video {input_path}")

                # Close the original clip to free resources
                original_clip.close()

                # Delete the temporary copy
                os.remove(temp_copy_path)

            else:
                filename, extension = os.path.splitext(os.path.basename(input_path))
                output_dir = os.path.dirname(input_path)

                operation_tags = []  # Initialize an empty list to keep track of operations

                # Determine the rotation operation tag
                if args.r:
                    rotation_tag = "ROTATED_" + args.r.upper()
                    operation_tags.append(rotation_tag)  # Add to the operations list
                    rotation_angle = 90 if args.r == "left" else -90
                else:
                    rotation_angle = None

                # Determine the volume increase operation tag
                if args.db:
                    volume_tag = f"INCREASED_{args.db}DB"
                    operation_tags.append(volume_tag)  # Add to the operations list

                # Determine the audio normalization operation tag
                if args.v:
                    normalization_tag = f"NORMALIZED_{args.v}"
                    operation_tags.append(normalization_tag)  # Add to the operations list

                # Join the operation tags with underscores to create a filename suffix
                operation_suffix = "_".join(operation_tags)

                # Create the output path with the operation suffix
                output_path = os.path.join(output_dir, f'{filename}_{operation_suffix}{extension}')

                if args.o:
                    output_path = os.path.join(args.o, os.path.basename(output_path))

                # Check if the output path already exists and get a non-conflicting name
                output_path = get_non_conflicting_filename(output_path)

                # Load the original video clip
                original_clip = VideoFileClip(input_path)
                successful_operations = True

                # Apply the operations in sequence, checking if they are successful
                if args.r and successful_operations:
                    processed_clip = rotate_video(original_clip, rotation_angle)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                if args.db and successful_operations:
                    processed_clip = increase_volume(original_clip, args.db)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                if args.v and successful_operations:
                    processed_clip = normalize_audio(original_clip, args.v)
                    if processed_clip:
                        original_clip = processed_clip
                    else:
                        successful_operations = False

                # Only write the final modified clip to the output path if all operations were successful
                if successful_operations:
                    original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    logging.info(f"Video {operation_suffix.lower()} saved as {output_path}")
                    print(f"Video {operation_suffix.lower()} saved as {output_path}")

                    # Remove the successfully processed line from the input file
                    if args.f:
                        remove_successful_line_from_file(args.f, input_path)
                else:
                    logging.error(f"Error: Operations failed for video {input_path}")
                    print(f"Error: Operations failed for video {input_path}")

                # Close the original clip to free resources
                original_clip.close()

        except OSError as e:
            logging.error(f"OSError: {str(e)} Skipping this file and moving to the next one.")
            print(f"OSError: {str(e)} Skipping this file and moving to the next one.")
            continue


if __name__ == "__main__":
    main()
