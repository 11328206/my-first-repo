import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
window = QLabel("Hello, PyQt6!")
window.resize(200, 150)
window.show()
sys.exit(app.exec())