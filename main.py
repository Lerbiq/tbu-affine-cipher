import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic, QtGui

import util

qtCreatorFile = "main.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


char_map = {
        " ": "XSPACEX",
        "!": "XEMARKX",
        "?": "XQUESTIONX",
        ",": "XCOMMAX",
        ".": "XDOTX",
        "0": "XNULAX",
        "1": "XJEDNAX",
        "2": "XDVAX",
        "3": "XTRIX",
        "4": "XCTRYRIX",
        "5": "XPETX",
        "6": "XSESTX",
        "7": "XSEDUMX",
        "8": "XOSUMX",
        "9": "XDEVETX"
    }

source_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class MyApp(QMainWindow, Ui_MainWindow):

    text_encrypt_labelInput = "Zadejte text k zašifrování:"
    text_decrypt_labelInput = "Zadejte text k rozšifrování:"

    text_encrypt_labelOutput = "Zašifrovaný text:"
    text_decrypt_labelOutput = "Rozšifrovaný text:"

    def __init__(self):
       QMainWindow.__init__(self)
       Ui_MainWindow.__init__(self)
       self.setupUi(self)
       self.radioButtonEncrypt.toggled.connect(self.handle_option_change)
       self.buttonDoStuff.clicked.connect(self.handle_do_stuff)

    def display_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Chyba")
        msg.setInformativeText(text)
        msg.setWindowTitle("Chyba")
        msg.exec_()

    def handle_option_change(self):
        if not self.radioButtonEncrypt.isChecked():
            self.labelFiltered.hide()
            self.textEditFiltered.hide()
            self.labelInput.setText(self.text_decrypt_labelInput)
            self.labelOutput.setText(self.text_decrypt_labelOutput)
            self.textEditFiltered.setPlainText("")
            input_text = self.textEditInput.toPlainText()
            output_text = self.textEditOutput.toPlainText()
            self.textEditInput.setPlainText(output_text)
            self.textEditOutput.setPlainText(input_text)
        else:
            self.labelFiltered.show()
            self.textEditFiltered.show()
            self.labelInput.setText(self.text_encrypt_labelInput)
            self.labelOutput.setText(self.text_encrypt_labelOutput)
            input_text = self.textEditInput.toPlainText()
            output_text = self.textEditOutput.toPlainText()
            self.textEditInput.setPlainText(output_text)
            self.textEditOutput.setPlainText(input_text)

    def handle_do_stuff(self):
        if self.radioButtonEncrypt.isChecked():
            self.handle_crypt()
        elif self.radioButtonDecrypt.isChecked():
            self.handle_decrypt()
        else:
            self.display_error("Nebyla vybrána žádná možnost!")

    def get_verified_keys(self):
        a = None
        b = None

        if not util.is_int(self.spinBoxKeyA.cleanText()):
            self.display_error("A není celé číslo")
            return a, b

        if not util.is_int(self.spinBoxKeyB.cleanText()):
            self.display_error("B není celé číslo")
            return a, b

        if util.gcd(int(self.spinBoxKeyA.cleanText()), 26) != 1:
            self.display_error("Číslo A je soudělné s 26")
            return a, b

        return int(self.spinBoxKeyA.cleanText()), int(self.spinBoxKeyB.cleanText())

    def handle_crypt(self):
        a, b = self.get_verified_keys()
        if a is None:
            return

        normalized = util.normalize(self.textEditInput.toPlainText(), char_map)
        encrypted = self.crypt(normalized, a, b)

        self.textEditFiltered.setPlainText(normalized)
        self.textEditOutput.setPlainText(util.format_encrypted(encrypted))

    def handle_decrypt(self):
        a, b = self.get_verified_keys()
        if a is None:
            return

        plain = self.decrypt(self.textEditInput.toPlainText(), a, b)

        self.textEditOutput.setPlainText(util.denormalize(plain, char_map))

    def crypt(self, text, a, b):
        encrypted = ""
        for char in text:
            encrypted += source_alphabet[(a * source_alphabet.find(char) + b) % 26]
        return encrypted

    def decrypt(self, text, a, b):
        decrypted = ""
        for char in text.replace(" ", ""):
            decrypted += source_alphabet[((source_alphabet.find(char) - b) * pow(a, -1, 26)) % 26]
        return decrypted


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.setWindowIcon(QtGui.QIcon("assets/lock_icon.svg"))
    window.setWindowFilePath("assets/lock_icon.svg")
    window.show()
    sys.exit(app.exec_())
