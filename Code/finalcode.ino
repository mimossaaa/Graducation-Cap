// ESP32_Arduino_for_Uno.ino
// Expert embedded-systems solution for Arduino Uno R3 and I2C LCD.
// This version displays centered, motivational graduation messages with UC Berkeley themes,
// including your new "Congrats Bal Grads 2025" messages.

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

// --- LCD Object Initialization ---
// Create an LCD object with the specified I2C address, columns, and rows.
LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLS, LCD_ROWS);

// --- printCenteredMessage Function ---
// Displays a plaintext string centered on a specified row of the LCD.
//
// Parameters:
//   text: The string to display.
//   row: The row (0-indexed) where the text will be centered.
void printCenteredMessage(String text, int row) {
  int col = (LCD_COLS - text.length()) / 2; // Calculate starting column for centering
  if (col < 0) col = 0; // Prevent negative column if text is longer than LCD_COLS
  lcd.setCursor(col, row);
  lcd.print(text);
}

// --- Setup Function ---
// Runs once when the Arduino Uno R3 starts.
void setup() {
  // Initialize Serial communication for debugging messages.
  Serial.begin(9600); // Common and reliable baud rate for Arduino Uno.
  Serial.println("Arduino Uno I2C LCD Graduation Messages Demo Start");

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

  // No custom characters are defined in this version.
  Serial.println("Custom characters are not used in this demo.");

  // Clear the LCD display to ensure a clean start
  lcd.clear();
}

// --- Loop Function ---
// Runs repeatedly after setup() completes.
void loop() {
  // Message 1: General Congratulations
  lcd.clear();
  delay(100);
  printCenteredMessage("CONGRATULATIONS!", 0);
  printCenteredMessage("Your Journey Begins", 1);
  printCenteredMessage("Now!", 2);
  printCenteredMessage("So Proud of You!", 3); // Added a line to fill the screen
  delay(4000);

  // NEW Message: Congrats Bal Grads 2025
  lcd.clear();
  delay(100);
  printCenteredMessage("Congrats Bal Grads", 0); // Fits on one line
  printCenteredMessage("2025", 1);                // Fits on one line, centered below
  printCenteredMessage("", 2);
  printCenteredMessage("Good Luck Everyone!", 3);
  delay(4000);

  // Message 2: UC Berkeley Specific
  lcd.clear();
  delay(100);
  printCenteredMessage("Next Stop:", 0);
  printCenteredMessage("UC BERKELEY!", 1);
  printCenteredMessage("Go Bears!", 2);
  printCenteredMessage("Cal Bound!", 3);
  delay(4000);

  // Message 3: Motivational
  lcd.clear();
  delay(100);
  printCenteredMessage("The Golden Bear", 0);
  printCenteredMessage("Awaits You!", 1);
  delay(4000);

  // Message 4: GO BFS!
  lcd.clear();
  delay(100);
  printCenteredMessage("GO BFS", 0);
  printCenteredMessage("The best club at", 1);
  printCenteredMessage("Balboa", 2);
  printCenteredMessage("4L", 3);
  delay(4000);

  // Message 5: Short and Sweet
  lcd.clear();
  delay(100);
  printCenteredMessage("YOU DID IT!", 1);
  printCenteredMessage("GO BEARS!", 2);
  delay(3000);

  // Demonstrate the scrolling
  lcd.clear();
  delay(100);
  String scrollText = "   Berkeley Here You Come! The Future Is Yours!   ";
  for (int i = 0; i < scrollText.length() - LCD_COLS + 1; i++) {
    printCenteredMessage(scrollText.substring(i, i + LCD_COLS), 0); // Scroll on row 0
    printCenteredMessage("Your New Adventure!", 2); // Static message on row 2
    printCenteredMessage("UC Berkeley 2025!", 3); // Static message on row 3
    delay(200); // Adjust delay for scroll speed
  }
  delay(2000);
}