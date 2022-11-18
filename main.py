import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog
from random import randint

from ui import Ui_Form

class Example(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.paint)
        self.do_paint = False

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw(qp)
            qp.end()

    def paint(self):
        self.do_paint = True
        self.repaint()

    def draw(self, qp):
        qp.setBrush(QColor(255, 255, 0))
        radius = randint(0, self.height())
        qp.drawEllipse(QRect(randint(0, self.width()), randint(0, self.height()), radius,
                             radius))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
