/**
 * Runic Numeral System – Composite Glyph Generator (0 to 9999, Opacity Adjusted)
 *
 * This sketch renders numbers 0 to 9999 as composite runic glyphs.
 * Each number is decomposed into four digits (thousands, hundreds, tens, ones)
 * and each digit is rendered in one quadrant around a central vertical line.
 *
 * Each quadrant is built from 5 segments drawn as simple extended rectangles.
 * Even if a segment is "off," it is rendered with white fill at 50% opacity (and black stroke);
 * when "on," the segment is rendered in black at 100% opacity.
 *
 * The two cross segments (indices 2 and 3) are drawn as two smaller rectangles (split with a gap).
 * The z‑order is such that off segments are drawn first, then on segments.
 *
 * Quadrant flips:
 *   - Upper Right (ones): drawn normally.
 *   - Upper Left (tens): flipped horizontally.
 *   - Lower Right (hundreds): flipped vertically.
 *   - Lower Left (thousands): flipped both horizontally and vertically.
 *
 * A central vertical line (5 pixels wide) spans the full vertical extent of the composite glyph.
 * The sketch runs at 10 fps and saves each frame as a PNG.
 */

// -------------------------------
// Global Settings and Variables
// -------------------------------
int minNumber = 0000;         // Minimum number to render (now including 0)
int maxNumber = 0500;      // Maximum number (0 to 9999)
int currentNumber;
int canvasWidth = 250;
int canvasHeight = 250;
String exportFolder = "frames";
int fps = 10;

// -------------------------------
// Segment Definition
// -------------------------------
// A Segment is defined by its offset (relative to quadrant center),
// its width (length) and height (thickness), and its rotation angle.
class Segment {
  float offsetX, offsetY;  // Position offset relative to quadrant center
  float w, h;              // w = length; h = thickness
  float angle;             // Rotation angle in radians
  
  Segment(float offsetX, float offsetY, float w, float h, float angle) {
    this.offsetX = offsetX;
    this.offsetY = offsetY;
    this.w = w;
    this.h = h;
    this.angle = angle;
  }
}

// We define 5 segments per quadrant.
Segment[] segments = new Segment[5];

void initSegments() {
  // Extended dimensions so that endpoints meet or slightly overlap.
  // Segment A: Top horizontal line ("1")
  segments[0] = new Segment(0, -35, 80, 8, 0);
  // Segment B: Bottom horizontal line ("2")
  segments[1] = new Segment(0, 35, 80, 8, 0);
  // Segment C: Diagonal from upper left to lower right ("3")
  segments[2] = new Segment(0, 0, 100, 8, radians(45));
  // Segment D: Diagonal from lower left to upper right ("4")
  segments[3] = new Segment(0, 0, 100, 8, radians(-45));
  // Segment E: Right vertical line ("6")
  segments[4] = new Segment(35, 0, 8, 80, 0);
}

// -------------------------------
// Rune Patterns for Digits 0–9
// -------------------------------
// Each digit is represented by a boolean[5] array (for segments A–E).
// For digit 0, all segments are off.
boolean[][] runePatterns = new boolean[10][];

void initRunePatterns() {
  runePatterns[0] = new boolean[] { false, false, false, false, false };
  // Dummy patterns for demonstration:
  runePatterns[1] = new boolean[] { true,  false, false, false, false };   // 1: Only A on
  runePatterns[2] = new boolean[] { false, true,  false, false, false };   // 2: Only B on
  runePatterns[3] = new boolean[] { false, false, true,  false, false };   // 3: Only C on
  runePatterns[4] = new boolean[] { false, false, false, true,  false };   // 4: Only D on
  runePatterns[5] = new boolean[] { true,  false, false, true,  false };   // 5: A + D on
  runePatterns[6] = new boolean[] { false, false, false, false, true  };   // 6: Only E on
  runePatterns[7] = new boolean[] { true,  false, false, false, true  };   // 7: A + E on
  runePatterns[8] = new boolean[] { false, true,  false, false, true  };   // 8: B + E on
  runePatterns[9] = new boolean[] { true,  true,  false, false, true  };   // 9: A + B + E on
}

// -------------------------------
// Processing Setup and Draw Loop
// -------------------------------
void settings() {
  size(canvasWidth, canvasHeight);
  pixelDensity(2);
}

void setup() {
  
  currentNumber = minNumber;
  createPath(exportFolder);  // Ensure export folder exists
  frameRate(fps);
  rectMode(CENTER);
  stroke(0);
  strokeWeight(0);
  
  initSegments();
  initRunePatterns();
}

void draw() {
  background(255);
  
  // Draw the composite rune for the current number.
  drawCompositeGlyph(currentNumber);
  
  // Draw the central vertical line as a rectangle.
  float quadOffsetY = 60;
  float topEdge = -quadOffsetY - 40;    // e.g., -60 - 30 = -90
  float bottomEdge = quadOffsetY + 40;    // e.g., 60 + 30 = 90
  float lineHeight = bottomEdge - topEdge; // 180
  fill(0);
  noStroke();
  rect(width/2, height/2, 8, lineHeight);
  stroke(255);
  
  // Display the current number as text at the bottom.
  /*fill(0);
  textAlign(CENTER, BOTTOM);
  textSize(24);
  text("Number: " + currentNumber, width/2, height - 10);*/
  
  // Save the current frame as a PNG.
  saveFrame(exportFolder + "/num_" + nf(currentNumber, 4) + ".png");
  println("Rendered number: " + currentNumber);
  
  currentNumber++;
  if (currentNumber > maxNumber) {
    println("Done generating symbols up to " + maxNumber + ".");
    exit();
  }
}

// -------------------------------
// Drawing Functions
// -------------------------------

// Draws a single segment as a rectangle.
// For cross segments (indices 2 and 3), draw them as two smaller rectangles with a gap.
void drawSegment(int index, Segment s, boolean on) {
  pushMatrix();
    translate(s.offsetX, s.offsetY);
    rotate(s.angle);
    if (index == 2 || index == 3) {
      drawSplitSegment(s, on);
    } else {
      // Set fill color with adjusted opacity.
      if (on) {
        fill(0, 255);       // Black, fully opaque
      } else {
        fill(255, 128);     // White, 50% opacity
      }
      rect(0, 0, s.w, s.h);
    }
  popMatrix();
}

// Draws a split segment (for cross bars) as two smaller rectangles separated by a gap.
void drawSplitSegment(Segment s, boolean on) {
  float gap = 4;  // Gap between parts in pixels.
  float halfLength = s.w / 2.0;
  float partLength = halfLength - gap / 2.0;
  
  if (on) {
    fill(0, 255);
  } else {
    fill(255, 128);
  }
  
  // Draw left part:
  pushMatrix();
    float leftCenter = - (halfLength + gap / 2.0) / 2.0;
    rect(leftCenter, 0, partLength, s.h);
  popMatrix();
  
  // Draw right part:
  pushMatrix();
    float rightCenter = (halfLength + gap / 2.0) / 2.0;
    translate(rightCenter, 0);
    rect(0, 0, partLength, s.h);
  popMatrix();
}

// Draws the rune for a single digit in one quadrant.
// The quadrant is centered at (offsetX, offsetY) relative to the composite glyph center.
// Z-order: first draw off segments, then on segments.
void drawQuadrant(int digit, float offsetX, float offsetY) {
  pushMatrix();
    translate(offsetX, offsetY);
    // First pass: draw off segments.
    for (int i = 0; i < 5; i++) {
      if (!runePatterns[digit][i]) {
        drawSegment(i, segments[i], false);
      }
    }
    // Second pass: draw on segments.
    for (int i = 0; i < 5; i++) {
      if (runePatterns[digit][i]) {
        drawSegment(i, segments[i], true);
      }
    }
  popMatrix();
}

// Draws the composite rune for the given number (0–9999).
// Quadrant arrangement:
//   - Upper Right (ones): drawn normally.
//   - Upper Left (tens): flipped horizontally.
//   - Lower Right (hundreds): flipped vertically.
//   - Lower Left (thousands): flipped both horizontally and vertically.
void drawCompositeGlyph(int number) {
  int ones = number % 10;
  int tens = (number / 10) % 10;
  int hundreds = (number / 100) % 10;
  int thousands = (number / 1000) % 10;
  
  pushMatrix();
    // Translate composite glyph to canvas center.
    translate(width/2, height/2);
    float quadOffsetX = 35;
    float quadOffsetY = 60;
    
    // Upper Right quadrant (ones) – drawn normally.
    drawQuadrant(ones, quadOffsetX, -quadOffsetY);
    
    // Upper Left quadrant (tens) – flipped horizontally.
    pushMatrix();
      translate(-quadOffsetX, -quadOffsetY);
      scale(-1, 1);
      drawQuadrant(tens, 0, 0);
    popMatrix();
    
    // Lower Right quadrant (hundreds) – flipped vertically.
    pushMatrix();
      translate(quadOffsetX, quadOffsetY);
      scale(1, -1);
      drawQuadrant(hundreds, 0, 0);
    popMatrix();
    
    // Lower Left quadrant (thousands) – flipped both horizontally and vertically.
    pushMatrix();
      translate(-quadOffsetX, quadOffsetY);
      scale(-1, -1);
      drawQuadrant(thousands, 0, 0);
    popMatrix();
  popMatrix();
}
