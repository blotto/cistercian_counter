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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

*Nick Newell* - [GitHub Profile](https://github.com/blotto)

## Acknowledgments

- Inspired from this [reddit post](https://www.reddit.com/r/coolguides/comments/wscf8f/cool_guide_to_cistercian_numerals/) 
- Inspiration from digital clock displays and custom numeral systems.
- The Processing community for their extensive documentation and support.
