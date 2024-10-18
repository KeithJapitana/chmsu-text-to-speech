/*
Teaching Spelling to learners with intellectual disability thru audio-visual mat.
-This code was developed and written by K.J. Japitana & D. Japitana 
-Date: October 17, 2024
-Purpose: SNRESI Button - Text - Speech
*/

// Define the button pins for 26 buttons (A-Z)
const int buttonPins[26] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36};

// Define the corresponding letters for each button (A-Z)
const char buttonLetters[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

// Define variables for debounce
unsigned long lastDebounceTime[26];   // to store the last debounce time for each button
const unsigned long debounceDelay = 50; // debounce time in milliseconds
int buttonState[26];                  // current reading of each button
int lastButtonState[26];              // previous reading of each button
 
void setup() {
  // Start the serial communication
  Serial.begin(9600);

  // Set the button pins as input with pull-up resistors
  for (int i = 0; i < 26; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);  // Enable internal pull-up resistors
    lastButtonState[i] = HIGH;             // Initialize button state as HIGH (not pressed)
    lastDebounceTime[i] = 0;               // Initialize debounce time
  }
}

void loop() {
  // Check each button state with debounce
  for (int i = 0; i < 26; i++) {
    int reading = digitalRead(buttonPins[i]);  // Read the button state

    // Check if the button state has changed
    if (reading != lastButtonState[i]) {
      // Reset the debounce timer
      lastDebounceTime[i] = millis();
    }

    // Check if enough time has passed since the last state change
    if ((millis() - lastDebounceTime[i]) > debounceDelay) {
      // If the button state has stabilized
      if (reading != buttonState[i]) {
        buttonState[i] = reading;

        // Trigger only if the new button state is LOW (button pressed)
        if (buttonState[i] == LOW) {
          Serial.println(buttonLetters[i]);  // Print corresponding letter
        }
      }
    }

    // Save the reading for the next loop iteration
    lastButtonState[i] = reading;
  }
}
