from PyQt5 import QtWidgets, QtGui, QtWidgets, QtPrintSupport
import configparser
from window import Ui_Dialog
import sys
import sqlite3
import qrcode
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from synch import Synch
import barcode
from barcode.writer import ImageWriter

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_Dialog()

        self.ui.setupUi(self)

        self.con = sqlite3.connect("burda.db", check_same_thread=False)

        self.ui.confirm_button.clicked.connect(self.print_barcode)

        self.synch = Synch(application=self)

        self.config = configparser.ConfigParser()

        self.ui.status.setValue(0)

    def sql_run(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def print_barcode(self):

        # barcode = self.ui.line_barkod.displayText()
        all_results = self.sql_run(
            f'SELECT name,model,brand,size FROM barcodes WHERE bar_code = "{self.ui.line_barkod.displayText()}"')

        ean = barcode.get('ean13', self.ui.line_barkod.displayText(), writer=ImageWriter())
        filename = ean.save('barcode',options={"write_text": False})


        qr = ImageQt(filename)

        pix = QPixmap.fromImage(qr)

        pix = pix.scaledToWidth(110)

        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:

            painter = QtGui.QPainter()

            font_header = QtGui.QFont()
            font_header.setFamily('Helvetica')
            font_header.setPixelSize(20)

            font_body = QtGui.QFont()
            font_body.setFamily('Helvetica')
            font_body.setPixelSize(11)

            painter.begin(dialog.printer())

            painter.setFont(font_header)

            self.config.read('config/main.ini')

            painter.drawText(70, 15, all_results[0][2])

            painter.setFont(font_body)

            painter.drawText(
                5,
                35,
                "Продукт: {0}".format(
                    all_results[0][0]
                )
            )

            painter.drawText(
                5,
                55,
                "Размер: {0}".format(
                    all_results[0][3]
                )
            )

            painter.drawText(
                5,
                75,
                "Партия: {0}".format(
                    self.ui.line_part.displayText()
                )
            )

            painter.drawText(
                5,
                95,
                "Цех: {0}".format(
                    self.ui.line_guild.displayText()
                )
            )

            painter.drawText(
                5,
                115,
                "Art: {0}".format(
                    all_results[0][1]
                )
            )

            painter.drawPixmap(80, 40, pix)

            painter.end()
    

    def view_message(self, message, header):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle(header)
        msgBox.setText(message)
        msgBox.exec()



app = QtWidgets.QApplication([])

application = Window()

application.show()

sys.exit(app.exec())
