# generate_lcd_chars.py
# Expert embedded-systems solution for generating custom LCD character byte arrays.

import sys

# --- Font Data Definition ---
# This dictionary maps characters to their 5x8 pixel patterns.
# Each character is represented by a list/tuple of 8 integers (bytes).
# Each integer defines one row of the character's 5x8 pixel grid.
# The 5 least significant bits (rightmost bits, 0-4) of each byte
# correspond to the 5 pixels in that row (column 0 to column 4 on the LCD).
# A '1' bit means the pixel is ON, '0' means OFF.
# The 3 most significant bits (5, 6, 7) are typically 0 as LCD custom
# characters are 5 pixels wide.
#
# Example: Capital 'A'
#   Binary: 0b01110 (decimal 14)  ->   . X X X .  (Row 0)
#   Binary: 0b10001 (decimal 17)  ->   X . . . X  (Row 1)
#   Binary: 0b11111 (decimal 31)  ->   X X X X X  (Row 2)
#   Binary: 0b10001 (decimal 17)  ->   X . . . X  (Row 3)
#   Binary: 0b10001 (decimal 17)  ->   X . . . X  (Row 4)
#   Binary: 0b00000 (decimal 0)   ->   . . . . .  (Row 5)
#   Binary: 0b00000 (decimal 0)   ->   . . . . .  (Row 6)
#   Binary: 0b00000 (decimal 0)   ->   . . . . .  (Row 7)
#
# You can extend this dictionary with more characters by designing their
# 5x8 pixel patterns. Many online tools or simply grid paper can help.
# This dictionary includes common uppercase letters, numbers, and some symbols.

FONT_5X8 = {
    'A': [0b01110, 0b10001, 0b11111, 0b10001, 0b10001, 0b00000, 0b00000, 0b00000],
    'B': [0b11110, 0b10001, 0b11110, 0b10001, 0b11110, 0b00000, 0b00000, 0b00000],
    'C': [0b01110, 0b10000, 0b10000, 0b10000, 0b01110, 0b00000, 0b00000, 0b00000],
    'D': [0b11110, 0b10001, 0b10001, 0b10001, 0b11110, 0b00000, 0b00000, 0b00000],
    'E': [0b11111, 0b10000, 0b11110, 0b10000, 0b11111, 0b00000, 0b00000, 0b00000],
    'F': [0b11111, 0b10000, 0b11110, 0b10000, 0b10000, 0b00000, 0b00000, 0b00000],
    'G': [0b01110, 0b10000, 0b10110, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    'H': [0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b00000, 0b00000, 0b00000],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b01110, 0b00000, 0b00000, 0b00000],
    'J': [0b00111, 0b00010, 0b00010, 0b10010, 0b01100, 0b00000, 0b00000, 0b00000],
    'K': [0b10001, 0b10010, 0b11100, 0b10010, 0b10001, 0b00000, 0b00000, 0b00000],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b11111, 0b00000, 0b00000, 0b00000],
    'M': [0b10001, 0b11011, 0b10101, 0b10001, 0b10001, 0b00000, 0b00000, 0b00000],
    'N': [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b00000, 0b00000, 0b00000],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    'P': [0b11110, 0b10001, 0b11110, 0b10000, 0b10000, 0b00000, 0b00000, 0b00000],
    'Q': [0b01110, 0b10001, 0b10011, 0b10101, 0b01110, 0b00010, 0b00000, 0b00000], # Q has a descender-like tail
    'R': [0b11110, 0b10001, 0b11110, 0b10010, 0b10001, 0b00000, 0b00000, 0b00000],
    'S': [0b01111, 0b10000, 0b01110, 0b00001, 0b11110, 0b00000, 0b00000, 0b00000],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00000, 0b00000],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    'V': [0b10001, 0b10001, 0b01010, 0b01010, 0b00100, 0b00000, 0b00000, 0b00000],
    'W': [0b10001, 0b10001, 0b10101, 0b11011, 0b10001, 0b00000, 0b00000, 0b00000],
    'X': [0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b00000, 0b00000, 0b00000],
    'Y': [0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00000, 0b00000, 0b00000],
    'Z': [0b11111, 0b00010, 0b00100, 0b01000, 0b11111, 0b00000, 0b00000, 0b00000],
    
    '0': [0b01110, 0b10001, 0b10001, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b01110, 0b00000, 0b00000, 0b00000],
    '2': [0b01110, 0b10001, 0b00100, 0b01000, 0b11111, 0b00000, 0b00000, 0b00000],
    '3': [0b11111, 0b00001, 0b00110, 0b00001, 0b11111, 0b00000, 0b00000, 0b00000],
    '4': [0b00010, 0b00110, 0b01010, 0b11111, 0b00010, 0b00000, 0b00000, 0b00000],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b11110, 0b00000, 0b00000, 0b00000],
    '6': [0b01110, 0b10000, 0b11110, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b00000, 0b00000, 0b00000],
    '8': [0b01110, 0b10001, 0b01110, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000],
    '9': [0b01110, 0b10001, 0b01111, 0b00001, 0b01110, 0b00000, 0b00000, 0b00000],

    ' ': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000], # Space character
    '!': [0b00100, 0b00100, 0b00100, 0b00000, 0b00100, 0b00000, 0b00000, 0b00000],
    '.': [0b00000, 0b00000, 0b00000, 0b00000, 0b00100, 0b00000, 0b00000, 0b00000],
    ',': [0b00000, 0b00000, 0b00000, 0b00000, 0b01000, 0b00100, 0b00000, 0b00000],
    '?': [0b01110, 0b10001, 0b00100, 0b01000, 0b00100, 0b00000, 0b00000, 0b00000],
    '+': [0b00000, 0b00100, 0b01110, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000],
    '-': [0b00000, 0b00000, 0b01110, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    '=': [0b00000, 0b11111, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000],
    '/': [0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000, 0b00000, 0b00000],
    '\\': [0b10000, 0b01000, 0b00100, 0b00010, 0b00001, 0b00000, 0b00000, 0b00000],
    ':': [0b00000, 0b00100, 0b00000, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000],
    ';': [0b00000, 0b00100, 0b00000, 0b01000, 0b00100, 0b00000, 0b00000, 0b00000],
    '(': [0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00000, 0b00000, 0b00000],
    ')': [0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b00000, 0b00000, 0b00000],
    '[': [0b11110, 0b10000, 0b10000, 0b10000, 0b11110, 0b00000, 0b00000, 0b00000],
    ']': [0b01111, 0b00001, 0b00001, 0b00001, 0b01111, 0b00000, 0b00000, 0b00000],
    '<': [0b00010, 0b00100, 0b01000, 0b00100, 0b00010, 0b00000, 0b00000, 0b00000],
    '>': [0b01000, 0b00100, 0b00010, 0b00100, 0b01000, 0b00000, 0b00000, 0b00000],
    '@': [0b01110, 0b10011, 0b10101, 0b10111, 0b01110, 0b00000, 0b00000, 0b00000],
    '#': [0b00000, 0b01010, 0b11111, 0b01010, 0b00000, 0b00000, 0b00000, 0b00000], # Simplified hash
    '$': [0b00100, 0b01111, 0b01000, 0b00110, 0b11100, 0b00010, 0b00000, 0b00000], # Simplified dollar
    '%': [0b10001, 0b10011, 0b00100, 0b11001, 0b10001, 0b00000, 0b00000, 0b00000],
    '^': [0b00100, 0b01010, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    '&': [0b01110, 0b10000, 0b01110, 0b10001, 0b01110, 0b00000, 0b00000, 0b00000], # Simplified ampersand
    '*': [0b00000, 0b00100, 0b10101, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000],
    '_': [0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    '`': [0b00100, 0b01000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    '~': [0b01010, 0b10101, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],

    # Placeholder for unknown characters. If a character is not found in FONT_5X8,
    # this 'UNKNOWN' character (a question mark) will be used instead.
    'UNKNOWN': [0b01110, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b01110, 0b00000],
}

def generate_char_array(char_code, char_data):
    """
    Generates a C-style byte array string for a custom character definition.

    Args:
        char_code (int): The numerical index (0-7) for this custom character.
        char_data (list): A list of 8 integers representing the pixel pattern
                          for the 5x8 character.

    Returns:
        str: A string formatted as an Arduino C++ byte array definition,
             e.g., "byte custom0[8] = { 0b01110, ... };"
    """
    # Format each byte as its binary representation (e.g., 0b01110)
    # The '05b' format specifier ensures a minimum of 5 bits are shown,
    # padding with leading zeros if necessary.
    byte_strings = [f"0b{byte:05b}" for byte in char_data]
    
    # Join the binary strings with commas and format into the final C-style array
    return f"byte custom{char_code}[8] = {{ {', '.join(byte_strings)} }};"

def main():
    """
    Main function to parse command-line arguments and generate custom character arrays.
    It prints the generated C-style byte array definitions to standard output.
    """
    # Check if a text argument was provided
    if len(sys.argv) < 2:
        print("Usage: python3 generate_lcd_chars.py \"YOUR_TEXT_HERE\"", file=sys.stderr)
        print("Example: python3 generate_lcd_chars.py \"HELLO WORLD!\"", file=sys.stderr)
        print("\nNote: Only uppercase letters, numbers, and common symbols are supported by default.", file=sys.stderr)
        print("      Lowercase letters will be converted to uppercase. Refer to FONT_5X8 ", file=sys.stderr)
        print("      dictionary in the script to add or modify characters.", file=sys.stderr)
        sys.exit(1)

    # Get the input text from the command line and convert it to uppercase
    input_text = sys.argv[1].upper()
    char_count = 0 # Counter for custom character index (0-7)

    # Print instructions for copy-pasting into the Arduino sketch
    print("# --- Custom Character Byte Array Definitions (for Arduino sketch) ---")
    print("# Copy and paste these definitions into your Arduino sketch before setup().")
    print("# Each definition creates an 8-byte array representing a 5x8 custom character.")
    print("#")
    print("# Then, in your Arduino sketch's setup() function, map these arrays to ")
    print("# specific custom character locations (0-7) using `lcd.createChar()`:")
    print("# Example mapping:")
    print("#   lcd.createChar(0, custom0); // Maps 'custom0' array to character index 0")
    print("#   lcd.createChar(1, custom1); // Maps 'custom1' array to character index 1")
    print("#   // ... up to lcd.createChar(7, custom7);")
    print("#")
    print("# In your Arduino code, you can then display these custom characters by")
    print("# printing their corresponding byte index (e.g., '\\x00' for custom0, '\\x01' for custom1).")
    print()

    # Iterate through each character in the input text
    for char in input_text:
        # LCDs typically support a maximum of 8 custom characters (indices 0-7)
        if char_count >= 8:
            print(f"Warning: Maximum 8 custom characters supported by LCD. Skipping '{char}'.", file=sys.stderr)
            break # Stop generating characters if the limit is reached
        
        # Get the pixel data for the current character from the FONT_5X8 dictionary.
        # If the character is not found, use the 'UNKNOWN' placeholder.
        char_data = FONT_5X8.get(char, FONT_5X8['UNKNOWN'])
        
        # If the character was not found in the font, issue a warning
        if char not in FONT_5X8:
            print(f"Warning: Character '{char}' not found in FONT_5X8. Using '?' placeholder.", file=sys.stderr)

        # Print the generated C-style byte array definition
        print(generate_char_array(char_count, char_data))
        char_count += 1 # Increment the custom character index

    # Provide a detailed explanation of the byte array mapping using 'A' as an example
    print("\n# --- Explanation of a single letter to 8-byte array mapping ---")
    print("# Let's take Capital 'A' as an example.")
    print("# Its pixel pattern is defined as: [0b01110, 0b10001, 0b11111, 0b10001, 0b10001, 0b00000, 0b00000, 0b00000]")
    print("#")
    print("# Each '0b...' value represents one row of the character's 5x8 grid.")
    print("# There are 8 such values, one for each row (Row 0 to Row 7).")
    print("#")
    print("# The 5 least significant bits (rightmost bits, from bit 0 to bit 4) map directly")
    print("# to the 5 pixels in that specific row (from left to right, pixel 0 to pixel 4).")
    print("# A '1' in a bit position means the corresponding pixel is ON (lit).")
    print("# A '0' means the pixel is OFF (unlit).")
    print("#")
    print("# For the first byte, 0b01110 (which is decimal 14):")
    print("#   Bit 4 (most significant of the 5 pixels): 0 (Pixel at column 0 is OFF)")
    print("#   Bit 3: 1 (Pixel at column 1 is ON)")
    print("#   Bit 2: 1 (Pixel at column 2 is ON)")
    print("#   Bit 1: 1 (Pixel at column 3 is ON)")
    print("#   Bit 0 (least significant of the 5 pixels): 0 (Pixel at column 4 is OFF)")
    print("#")
    print("# This forms the top row of the 'A' character: '. X X X .' (where 'X' is a lit pixel and '.' is unlit).")
    print("# The bits 5, 6, and 7 (most significant bits of the 8-bit byte) are typically 0")
    print("# because standard LCD custom characters are only 5 pixels wide.")
    print("# You can design any custom character on a 5x8 grid, convert each row to its 5-bit")
    print("# binary representation, and then add it to the FONT_5X8 dictionary.")

# Ensure the main function runs only when the script is executed directly
if __name__ == "__main__":
    main()