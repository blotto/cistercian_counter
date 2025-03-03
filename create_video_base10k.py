#!/usr/bin/env python3
import os
import math
import argparse
import subprocess
from PIL import Image

# Constants
FRAMES_FOLDER = "frames"              # folder with Processing images: num_XXXX.png
TEMP_FOLDER = "composite_frames"       # folder to save composite images

# Base for each runic digit (each digit is 0..9999)
BASE = 10000

def fixed_digit_count(total_frames):
    """Determine the fixed number of runic digits needed for the entire video.
    We always use at least 4 digits. For frame counts above 9999, we use
    the number of digits in the base-10000 representation, but never less than 4.
    """
    if total_frames < BASE:
        return 4
    else:
        # Number of digits in base-10000 representation of total_frames:
        digits = math.floor(math.log(total_frames, BASE)) + 1
        return max(4, digits)

def get_composite_digits(num, fixed_digits):
    """Convert num (an integer starting at 1) into a list of digits in base 10000,
    left-padded with zeros so that the list length equals fixed_digits.
    For example, if fixed_digits==4 and num==1, return [0,0,0,1].
    """
    digits = []
    n = num
    # Convert to base 10000 (least-significant digit first)
    while n > 0:
        digits.append(n % BASE)
        n //= BASE
    # If num is zero, ensure we return all zeros.
    if not digits:
        digits = [0]
    # Pad with zeros to the left until the length is fixed_digits.
    while len(digits) < fixed_digits:
        digits.append(0)
    # Reverse to get most significant digit first.
    digits.reverse()
    return digits

def load_digit_image(digit):
    """Load the image corresponding to a runic digit.
    The file should be named num_XXXX.png where XXXX is a zero-padded 4-digit number.
    """
    filename = os.path.join(FRAMES_FOLDER, f"num_{digit:04d}.png")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Expected file {filename} not found.")
    return Image.open(filename)

def create_composite_image(digits):
    """Given a list of runic digit values, load their images and concatenate them horizontally.
    Assumes all images have the same dimensions.
    """
    images = [load_digit_image(d) for d in digits]
    widths, heights = zip(*(img.size for img in images))
    total_width = sum(widths)
    max_height = max(heights)
    composite = Image.new('RGBA', (total_width, max_height), (255,255,255,0))
    x_offset = 0
    for img in images:
        composite.paste(img, (x_offset, 0))
        x_offset += img.width
    return composite

def generate_composite_frames(total_frames, fixed_digits):
    """Generate composite images for each frame from 1 to total_frames.
    For each frame, convert its frame number into a fixed-digit list (in base 10000)
    and create a composite image by horizontally concatenating the corresponding
    runic digit images. Save these composite images in TEMP_FOLDER.
    """
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
    
    for i in range(1, total_frames + 1):
        digits = get_composite_digits(i, fixed_digits)
        # For a single-digit composite (i.e. if fixed_digits == 1) we simply copy the image.
        # Otherwise, we composite them side by side.
        if fixed_digits == 1:
            src = os.path.join(FRAMES_FOLDER, f"num_{digits[0]:04d}.png")
            dst = os.path.join(TEMP_FOLDER, f"composite_{i:05d}.png")
            with Image.open(src) as im:
                im.save(dst)
        else:
            comp_img = create_composite_image(digits)
            dst = os.path.join(TEMP_FOLDER, f"composite_{i:05d}.png")
            comp_img.save(dst)
        if i % 100 == 0:
            print(f"Generated composite frame {i}/{total_frames}")

def create_video(fps, duration, output_filename):
    """Generate a video from composite images using ffmpeg.
    The total number of frames is determined by fps * duration.
    Composite images are taken from TEMP_FOLDER, named composite_XXXXX.png.
    """
    total_frames = int(fps * duration)
    fixed_digits = fixed_digit_count(total_frames)
    print(f"Using fixed composite digit count: {fixed_digits}")
    generate_composite_frames(total_frames, fixed_digits)
    
    # Build the ffmpeg command.
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output if it exists
        "-framerate", str(fps),
        "-i", os.path.join(TEMP_FOLDER, "composite_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_filename
    ]
    
    print("Running ffmpeg command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Create video from runic frame images.")
    parser.add_argument("fps", type=int, help="Frame rate for the video (e.g., 30)")
    parser.add_argument("duration", type=float, help="Duration of the video in seconds (e.g., 1.0)")
    parser.add_argument("filename", type=str, help="Output video filename (e.g., output.mp4)")
    args = parser.parse_args()
    
    create_video(args.fps, args.duration, args.filename)

if __name__ == "__main__":
    main()
