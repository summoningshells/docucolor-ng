import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, 
                             QPushButton, QLabel, QCheckBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DocuColorDecoder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DocuColor Tracking Dot Decoder')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        self.checkboxes = {}

        # grid labels
        for col in range(1, 16):
            grid_layout.addWidget(QLabel(str(col)), 0, col, alignment=Qt.AlignmentFlag.AlignCenter)

        row_labels = ['col parity', '64', '32', '16', '8', '4', '2', '1']
        for row in range(8):
            grid_layout.addWidget(QLabel(row_labels[row]), row + 1, 0, alignment=Qt.AlignmentFlag.AlignRight)

        # checkboxes
        for row in range(8):
            for col in range(1, 16):
                checkbox = QCheckBox()
                self.checkboxes[(col, 7 - row)] = checkbox
                grid_layout.addWidget(checkbox, row + 1, col, alignment=Qt.AlignmentFlag.AlignCenter)

        # buttons
        button_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)

        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear_checkboxes)
        button_layout.addWidget(clear_button)

        decode_button = QPushButton('Decode')
        decode_button.clicked.connect(self.decode)
        button_layout.addWidget(decode_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Courier"))
        main_layout.addWidget(self.result_text)

    def clear_checkboxes(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
        self.result_text.clear()

    def decode(self):
        dots = {(x, y): int(self.checkboxes[(x, y)].isChecked()) for x in range(1, 16) for y in range(8)}
        
        result = self.perform_decoding(dots)
        self.result_text.setPlainText(result)

    def perform_decoding(self, dots):
        result = []

        # show dot pattern
        result.append("Dot Pattern:")
        result.append(self.print_matrix(dots))
        result.append("")

        # Verify row parity
        bad_rows = self.verify_row_parity(dots)
        if bad_rows:
            for row in bad_rows:
                result.append(f"Parity mismatch for row {row}.")
        else:
            result.append("Row parity verified correctly.")

        # Verify column parity
        bad_cols = self.verify_column_parity(dots)
        if bad_cols:
            for col in bad_cols:
                result.append(f"Parity mismatch for column {col}.")
        else:
            result.append("Column parity verified correctly.")

        # Try to correct input errors
        correction_made = self.correct_errors(dots, bad_rows, bad_cols)
        if correction_made:
            result.append("Correction made. Processing corrected matrix:")
            result.append(self.print_matrix(dots))
        
        result.append("")

        # Decode serial number
        serial_short = f"{self.column_value(dots, 13):02d}{self.column_value(dots, 12):02d}{self.column_value(dots, 11):02d}"
        serial_long = f"{self.column_value(dots, 14):02d}{self.column_value(dots, 13):02d}{self.column_value(dots, 12):02d}{self.column_value(dots, 11):02d}"
        result.append(f"Printer serial number: {serial_short} [or {serial_long}]")

        # Decode date and time
        year = self.decode_year(dots)
        month = self.decode_month(dots)
        day = self.decode_day(dots)
        result.append(f"Date: {month} {day}, {year}")

        hour = self.column_value(dots, 5)
        minute = self.column_value(dots, 2)
        result.append(f"Time: {hour:02d}:{minute:02d}")

        # Decode unknown column 15
        result.append(f"Column 15 value: {self.column_value(dots, 15)}")

        return "\n".join(result)

    def print_matrix(self, dots):
        matrix = []
        row_labels = ['col parity', '64', '32', '16', '8', '4', '2', '1']
        for y in range(7, -1, -1):
            line = f"{row_labels[7-y]:<10}" + "".join("o" if dots[(x, y)] else "." for x in range(1, 16))
            matrix.append(line)
        
        # column numbers 
        col_numbers = "  " + "".join(f"{i:2d}" for i in range(1, 16))
        matrix.insert(0, col_numbers)
        
        return "\n".join(matrix)

    def verify_row_parity(self, dots):
        return [row for row in range(7) if sum(dots[(col, row)] for col in range(1, 16)) % 2 == 0]

    def verify_column_parity(self, dots):
        return [col for col in range(1, 16) if sum(dots[(col, row)] for row in range(8)) % 2 == 0]

    def correct_errors(self, dots, bad_rows, bad_cols):
        if len(bad_cols) == 1 and len(bad_rows) == 0:
            dots[(bad_cols[0], 7)] = not dots[(bad_cols[0], 7)]
            return True
        elif len(bad_cols) == 1 and len(bad_rows) == 1:
            dots[(bad_cols[0], bad_rows[0])] = not dots[(bad_cols[0], bad_rows[0])]
            return True
        return False

    def column_value(self, dots, col):
        return sum(dots[(col, y)] * 2**y for y in range(7))

    def decode_year(self, dots):
        year = self.column_value(dots, 8)
        return year + 2000 if year < 70 else year + 1900

    def decode_month(self, dots):
        month_names = [
            "(no month specified)", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month = self.column_value(dots, 7)
        return month_names[month] if 0 <= month < len(month_names) else f"(invalid month {month})"

    def decode_day(self, dots):
        day = self.column_value(dots, 6)
        if day == 0:
            return "(no day specified)"
        elif day > 31:
            return f"(invalid day {day})"
        return str(day)

def main():
    app = QApplication(sys.argv)
    ex = DocuColorDecoder()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()