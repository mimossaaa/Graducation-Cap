// ESP32_Arduino_for_Uno.ino
// Expert embedded-systems solution for Arduino Uno R3 and I2C LCD with "Big Font" characters.

// Required Libraries:
// 1. Wire.h: For I2C communication. This library is pre-installed with the Arduino IDE.
// 2. LiquidCrystal_I2C.h: For controlling I2C LCDs.
//    To install: Open Arduino IDE -> Sketch -> Include Library -> Manage Libraries...
//    Search for "LiquidCrystal I2C" by Frank de Brabander (or a similar popular one) and install it.

#include <Wire.h>             // Include the I2C communication library
#include <LiquidCrystal_I2C.h> // Include the LCD I2C library

// --- Configuration Definitions ---
const int LCD_COLS = 20;     // Number of columns on the LCD (e.g., 16, 20)
const int LCD_ROWS = 4;      // Number of rows on the LCD (e.g., 2, 4)
const int LCD_ADDRESS = 0x3F; // I2C address of the LCD module. Common addresses are 0x27 or 0x3F.
                              // If your LCD doesn't work, try changing this address.

// --- Custom Character Definitions for "Big Font" Letters ---
// Each "big" letter is split into a top half and a bottom half,
// each occupying one 5x8 custom character slot.
//
// Pattern Explanation (for each byte):
// 0babcde
//   a, b, c, d, e represent pixels 0-4 (left to right) in a row.
//   1 = pixel ON, 0 = pixel OFF.
// The 8 bytes define the 8 rows of the 5x8 grid.
//
// Custom character 0: Top half of 'C'
//   0b01110  ( . X X X . )
//   0b10001  ( X . . . X )
//   0b10000  ( X . . . . )
//   0b00000  ( . . . . . ) <- Spacer row in 5x8 cell for top part
//   0b00000  ( . . . . . )
//   0b00000  ( . . . . . )
//   0b00000  ( . . . . . )
//   0b00000  ( . . . . . )
byte C_top[8] = {
  0b01110,
  0b10001,
  0b10000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

// Custom character 1: Bottom half of 'C'
//   0b00000  ( . . . . . ) <- Spacer row in 5x8 cell for bottom part
//   0b00000  ( . . . . . )
//   0b00000  ( . . . . . )
//   0b10000  ( X . . . . )
//   0b10001  ( X . . . X )
//   0b01110, ( . X X X . )
//   0b00000,
//   0b00000
byte C_bottom[8] = {
  0b00000,
  0b00000,
  0b00000,
  0b10000,
  0b10001,
  0b01110,
  0b00000,
  0b00000
};

// Custom character 2: Top half of 'A'
byte A_top[8] = {
  0b01110,
  0b10001,
  0b11111,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

// Custom character 3: Bottom half of 'A'
byte A_bottom[8] = {
  0b00000,
  0b00000,
  0b00000,
  0b10001,
  0b10001,
  0b10001,
  0b00000,
  0b00000
};

// Custom character 4: Top half of 'L'
byte L_top[8] = {
  0b10000,
  0b10000,
  0b10000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

// Custom character 5: Bottom half of 'L'
byte L_bottom[8] = {
  0b00000,
  0b00000,
  0b00000,
  0b10000,
  0b10000,
  0b11111,
  0b00000,
  0b00000
};

// Custom character 6: Top half of 'B'
byte B_top[8] = {
  0b11100,
  0b10010,
  0b11100,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

// Custom character 7: Bottom half of 'B'
byte B_bottom[8] = {
  0b00000,
  0b00000,
  0b00000,
  0b11100,
  0b10010,
  0b11100,
  0b00000,
  0b00000
};


// --- LCD Object Initialization ---
// Create an LCD object with the specified I2C address, columns, and rows.
LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLS, LCD_ROWS);

// --- Setup Function ---
// Runs once when the Arduino Uno R3 starts.
void setup() {
  // Initialize Serial communication for debugging messages.
  Serial.begin(9600); // Common and reliable baud rate for Arduino Uno.
  Serial.println("Arduino Uno I2C LCD Big Font Demo Start");

  // Initialize the I2C bus.
  // For Arduino Uno R3, Wire.begin() implicitly uses A4 (SDA) and A5 (SCL).
  Wire.begin();
  Serial.println("I2C bus initialized for Arduino Uno.");

  // Initialize the LCD.
  lcd.init();
  Serial.println("LCD initialization command sent.");

  // Turn on the LCD backlight.
  lcd.backlight();
  Serial.println("LCD backlight ON.");

  // Define custom characters. Map the top/bottom halves to indices 0-7.
  lcd.createChar(0, C_top);     // C top half
  lcd.createChar(1, C_bottom);  // C bottom half
  lcd.createChar(2, A_top);     // A top half
  lcd.createChar(3, A_bottom);  // A bottom half
  lcd.createChar(4, L_top);     // L top half
  lcd.createChar(5, L_bottom);  // L bottom half
  lcd.createChar(6, B_top);     // B top half
  lcd.createChar(7, B_bottom);  // B bottom half
  Serial.println("Big Font custom characters created and stored.");

  // Clear the LCD display to ensure a clean start
  lcd.clear();

  // Initial message before the main loop starts
  lcd.setCursor(0, 0);
  lcd.print("Loading Big Font...");
  lcd.setCursor(0, 1);
  lcd.print("Prepare for impact!");
  delay(2000);
  lcd.clear();
}

// --- printSegment Function ---
// Displays a segment of a message on a specific row and column.
// This function is the same as printMessage, but renamed for clarity in context
// of multi-segment (big font) display.
//
// Parameters:
//   text: The string segment to display, potentially containing custom character indices (0-7).
//   row: The row (0-indexed) where the text will start.
//   col: The column (0-indexed) where the text will start.
void printSegment(String text, int row, int col) {
  lcd.setCursor(col, row);
  for (int i = 0; i < text.length(); i++) {
    char c = text.charAt(i);
    if (c >= 0 && c <= 7) {
      lcd.write(c); // Print the custom character at its index (0-7)
    } else {
      lcd.print(c); // Print a normal ASCII character
    }
  }
}

// --- Loop Function ---
// Runs repeatedly after setup() completes.
void loop() {
  // Clear the screen for the new message
  lcd.clear();
  delay(100);

  // --- Display "Cal bound" using a mix of big and standard characters ---
  // The big characters (C, A, L, B) will span two rows (row 0 and row 1).
  // The 'bound' part will be standard ASCII and start on row 0.

  // Display the TOP halves of the big characters and the start of 'bound'
  // "\x00" = C_top, "\x02" = A_top, "\x04" = L_top, "\x06" = B_top
  printSegment("\x00\x02\x04 \x06ound", 0, 0); // "C A L  B ound" - top row

  // Display the BOTTOM halves of the big characters
  // "\x01" = C_bottom, "\x03" = A_bottom, "\x05" = L_bottom, "\x07" = B_bottom
  // We need to print spaces or blank characters after the 'B' bottom to
  // visually align with "ound" on the top row if needed, but 'printSegment'
  // will start printing from the cursor, so simple spaces will work if we print past 'B'.
  printSegment("\x01\x03\x05 \x07", 1, 0); // "C A L  B" - bottom row

  // You can add more clarity for the 'bound' part on the second line if desired,
  // but it usually looks better to leave the bottom line aligned with the big font.
  // If you wanted to, you could add: printSegment("       ound", 1, 0); to visually match

  printSegment("       ", 1, 5); // Clear the 'ound' portion of the bottom row, if it overlaps, assuming 5 is where 'o' starts.
                                // Adjust this column number (5) based on visual alignment after testing.
                                // In this specific case, it's better to just leave it. The big characters end and the small ones continue on the top line.

  // Add a general message for the lower rows
  printSegment("Congrats Class of 2025!", 2, 0);
  printSegment("Go get 'em!", 3, 0);

  delay(5000); // Display for 5 seconds

  // --- Example of another message (standard font) ---
  lcd.clear();
  delay(100);
  printSegment("Future is bright!", 0, 0);
  printSegment("Keep shining!", 1, 0);
  delay(3000);

  // --- Scrolling text demo ---
  lcd.clear();
  delay(100);
  String scrollText = "   Success awaits! Congratulations!   ";
  for (int i = 0; i < scrollText.length() - LCD_COLS + 1; i++) {
    printSegment(scrollText.substring(i, i + LCD_COLS), 0, 0);
    delay(200);
  }
  delay(1000);
}