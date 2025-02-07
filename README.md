# docucolor-ng
Simple local GUI tool for forensic yellowdot pattern analysis (MIC) based on this reasearch by the EFF: https://w2.eff.org/Privacy/printers/docucolor/


Preview
![alt text](image.png)


## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/docucolor-tracking-dot-decoder.git
   cd docucolor-tracking-dot-decoder
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.9+ installed. Install required packages using pip:
   ```bash
   pip install PyQt6
   ```

3. **Run the Program**:
   Execute the program with:
   ```bash
   python main.py
   ```

---

## Usage

1. Launch the program by running `main.py`.
2. Use the grid interface to input the dot pattern:
   - Checkboxes represent dots (checked = dot present, unchecked = no dot).
3. Click **Decode** to process the input pattern:
   - The decoded results will appear in the text box below, including parity checks, serial number, date, and time.
4. If needed, click **Clear** to reset all inputs.



## Decoding Details

The program decodes information from DocuColor tracking dots as follows:

- **Printer Serial Number**:
  - Extracted from columns 11–14.
- **Date of Printing**:
  - Year: Decoded from column 8.
  - Month: Decoded from column 7.
  - Day: Decoded from column 6.
- **Time of Printing**:
  - Hour: Decoded from column 5.
  - Minute: Decoded from column 2.
