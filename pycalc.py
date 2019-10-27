#! /usr/bin/env python3

"""A simple calculator app built using Python and PyQt5."""
import sys

from functools import partial

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QVBoxLayout
#Setup the calculator's GUI

class PyCalcUi(QMainWindow):
    """PyCalc's View GUI. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setFixedSize(235, 235)
        #Set the central widget and its layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        #Create the display and buttons
        self._createDisplay()
        self._createButtons()
    
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                  }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40,40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            self.generalLayout.addLayout(buttonsLayout)
    
    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()
    
    def displayText(self):
        """Get display's text."""
        return self.display.text()
    
    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')

ERROR_MSG = "ERROR"
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result
class PyCalcCtrl:
    """Controls for the calculator PyCalc class."""
    def __init__(self, model, view):
        self._view = view
        self._evaluate = model
        self._connectSignals()

    def _calculateResult(self, sub_exp):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    
    def _buildExpression(self, sub_exp):
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)


def main():
    """Main Function for the Calc."""
    #Create a instance of QApplication
    pycalc = QApplication([])
    #Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    #Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    #Execute the calculator's main loop.
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()



