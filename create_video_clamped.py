#!/usr/bin/env python3
import os
import math
import argparse
import subprocess
from PIL import Image

# Folders and base value
FRAMES_FOLDER = "frames"          # Folder with single-digit images (num_XXXX.png)
TEMP_FOLDER = "composite_frames"   # Folder to save composite images
BASE = 9999                        # Maximum value per runic digit

def saturated_digits(x):
    """
    Convert a positive integer x into a list of runic digits using a saturated system.
    If x <= 9999, return [x]. If x > 9999, the least-significant digit is clamped at 9999,
    and the overflow is carried to the next digit on the left.
    
    Examples:
      saturated_digits(1)      -> [1]
      saturated_digits(9999)   -> [9999]
      saturated_digits(10000)  -> [1, 9999]
      saturated_digits(10001)  -> [2, 9999]
    """
    if x <= BASE:
        return [x]
    else:
        return saturated_digits(x - BASE) + [BASE]

def fixed_digit_count(total_frames):
    """
    Determine the fixed number of runic digits required.
    We use at least 4 digits. For total_frames greater than 9999, use the length
    of the saturated_digits(total_frames) but at least 4.
    """
    rep = saturated_digits(total_frames)
    return max(4, len(rep))

def get_composite_digits(num, fixed_digits):
    """
    Convert a frame number (starting at 1) into a fixed-length list of runic digits.
    Uses the saturated_digits conversion and pads on the left with zeros (runic zero)
    so that the total number of digits is fixed.
    """
    # For frame number 0, return [0]
    if num == 0:
        rep = [0]
    else:
        rep = saturated_digits(num)
    # Pad with 0's on the left until the length equals fixed_digits.
    while len(rep) < fixed_digits:
        rep = [0] + rep
    return rep

def load_digit_image(digit):
    """
    Loads the image corresponding to a runic digit.
    The image file is expected to be named num_XXXX.png where XXXX is a 4-digit number.
    """
    filename = os.path.join(FRAMES_FOLDER, f"num_{digit:04d}.png")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Expected file {filename} not found.")
    return Image.open(filename)

def create_composite_image(digits):
    """
    Given a list of runic digit values (from leftmost to rightmost),
    load their images and concatenate them horizontally.
    Assumes all images have the same dimensions.
    """
    imgs = [load_digit_image(d) for d in digits]
    widths, heights = zip(*(img.size for img in imgs))
    total_width = sum(widths)
    max_height = max(heights)
    composite = Image.new('RGBA', (total_width, max_height), (255,255,255,0))
    x_offset = 0
    for img in imgs:
        composite.paste(img, (x_offset, 0))
        x_offset += img.width
    return composite

def generate_composite_frames(total_frames, fixed_digits):
    """
    Generate composite images for each frame from 1 to total_frames.
    Each composite image is created by converting the frame number into a fixed-length
    list of runic digits (using the saturated system) and concatenating their images.
    The images are saved in TEMP_FOLDER as composite_XXXXX.png.
    """
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
    
    for i in range(1, total_frames + 1):
        digits = get_composite_digits(i, fixed_digits)
        comp_img = create_composite_image(digits)
        dst = os.path.join(TEMP_FOLDER, f"composite_{i:05d}.png")
        comp_img.save(dst)
        if i % 100 == 0:
            print(f"Generated composite frame {i}/{total_frames}")

def create_video(fps, duration, output_filename):
    """
    Generates a video from the composite images using ffmpeg.
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
        "-y",  # overwrite output file if it exists
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
