# Runic Numeral System – Composite Glyph Generator

This Processing sketch generates composite glyphs for numbers using a custom runic numeral system. Each number (from **0 to 9999**) is decomposed into four digits (thousands, hundreds, tens, ones) and rendered in separate quadrants around a central vertical line. The glyphs are constructed using digital clock–style segments with adjustable opacity, ensuring that segments in the "off" state appear at 50% opacity while "on" segments are fully opaque.

## Features

- **Custom Runic Numerals:**  
  Each digit is represented by a unique combination of five line segments:
  - The top segment represents a value (1, 10, 100, or 1000) depending on the quadrant.
  - The bottom, diagonal, and vertical segments similarly contribute their values.
  - Combinations of segments form numbers 1–9.
  
- **Quadrant Layout:**  
  - **Upper Right (Ones):** Drawn normally.
  - **Upper Left (Tens):** Flipped horizontally.
  - **Lower Right (Hundreds):** Flipped vertically.
  - **Lower Left (Thousands):** Flipped both horizontally and vertically.

- **Opacity Control:**  
  - "On" segments are rendered in black at 100% opacity.
  - "Off" segments are rendered in white at 50% opacity.

- **Z-Order Rendering:**  
  Off segments are drawn first (in the back) and on segments are drawn afterward (in the front).

- **Central Vertical Line:**  
  A 5-pixel-wide central vertical line spans the full vertical extent of the composite glyph.

- **Frame Export:**  
  The sketch runs at 10 fps and saves each frame as a PNG file in the `frames` folder.

- **High Resolution Option:**  
  Increase pixel density (e.g., using `pixelDensity(displayDensity())`) to smooth out diagonal segments if needed.

## Setup and Usage

1. **Requirements:**  
   - [Processing (Java mode)](https://processing.org/download/)
   - Git (for repository management)

2. **Installation:**  
   - Clone this repository to your local machine.
   - Open the `.pde` file in the Processing IDE.

3. **Configuration:**  
   - Modify the `minNumber` and `maxNumber` variables in the code to change the range (currently set to **0–9999**).
   - Adjust segment dimensions, gap sizes, and opacity values as desired.
   - Increase the pixel density by adding `pixelDensity(displayDensity());` in the `setup()` function if necessary.

4. **Running the Sketch:**  
   - Run the sketch in Processing.
   - The sketch will render composite runic glyphs for each number, saving each frame as a PNG in the `frames` folder (e.g., `num_0000.png`, `num_0001.png`, etc.).

5. **Customization:**  
   - Update the `runePatterns` array to modify which segments are "on" or "off" for each digit.
   - Adjust the `initSegments()` function to tweak the appearance of each segment.
   - Modify quadrant transformations in `drawCompositeGlyph()` to change how digits are flipped and positioned.
  
## Video Creation Options

In addition to generating individual composite glyph images from Processing, two options are provided via a Python script for creating a video from these images using ffmpeg.

### Option 1: Standard Base-10,000 Conversion

- **Logic:**  
  Each composite glyph is constructed by converting the frame number to a series of runic digits using standard base-10,000 arithmetic.  
  - For example, frame **10,000** would be represented as `[1, 0]`, meaning the rightmost (least-significant) digit cycles normally from 0 to 9999.
  
- **Behavior:**  
  The least-significant digit (LSB) cycles normally (i.e. it resets to 0 after 9999), and additional digits are added to the left as needed.
  
- **Use Case:**  
  This option is useful if you prefer a traditional numeral system behavior where every digit has its full cycle.

### Option 2: Saturated (Clamped) Conversion

- **Logic:**  
  Alternatively, a "saturated" conversion option is available. In this system, each runic digit can only represent values from 0 to 9999. When the frame number exceeds 9999, the least-significant digit is clamped at **9999**, and the overflow is carried to a new digit on the left.  
  - For example, frame **10,000** becomes `[1, 9999]`, so the LSB stays at 9999, and frame **10,001** becomes `[2, 9999]`.
  
- **Behavior:**  
  This method ensures that the rightmost runic symbol is always fixed at its maximum value (9999) once an overflow occurs. The layout remains constant, as unused (placeholder) positions are rendered with the runic zero.  
  This prevents any changes in composite image dimensions across frames.
  
- **Use Case:**  
  Use this option if you want a fixed layout in your video where the number of runic digits never changes, even when the frame count exceeds 9999.

### How to Create the Video

A Python script is provided that takes three command-line arguments:  
- **fps:** Frame rate for the video (e.g., `30`)
- **duration:** Duration of the video in seconds (e.g., `1.0`)
- **filename:** Output video filename (e.g., `output.mp4`)

The script performs the following:
1. **Calculates the Total Number of Frames:**  
   `total_frames = fps * duration`
2. **Converts Each Frame Number:**  
   - For the standard option, it uses normal base-10,000 conversion.
   - For the saturated option, it clamps the least-significant digit at 9999 and carries overflow to a new digit on the left.
3. **Generates Composite Images:**  
   Composite images are created by concatenating the individual runic digit images (from the `frames` folder). Placeholder runic zeros are used for any digits that are not yet used, ensuring a constant composite layout.
4. **Creates the Video Using ffmpeg:**  
   The script calls ffmpeg via a subprocess to compile the composite images into a video.

**Example Command:**

```python create_video.py 30 1.0 output.mp4```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

*Nick Newell* - [GitHub Profile](https://github.com/blotto)

## Acknowledgments

- Inspired from this [reddit post](https://www.reddit.com/r/coolguides/comments/wscf8f/cool_guide_to_cistercian_numerals/) 
- Inspiration from digital clock displays and custom numeral systems.
- The Processing community for their extensive documentation and support.
