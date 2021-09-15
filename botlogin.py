from PyQt5 import QtCore, QtGui, QtWidgets
from BinanceBotPyQt5 import MainUi
import pyrebase
from wmi import WMI

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
try:
    emailpass = []
    with open('./bdata/loginuserinfo', 'r') as f:
        for line in f:
            part = line.strip()
            emailpass.append(part)
except:pass

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(350, 250)
        Dialog.setWindowIcon(QtGui.QIcon('./bdata/logo.ico'))
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(25, 10, 320, 80))
        self.label_1.setFont(QtGui.QFont('Arial',30))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 141, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 141, 21))
        self.label_3.setObjectName("label_3")
        self.email = QtWidgets.QLineEdit(Dialog)
        self.email.setGeometry(QtCore.QRect(110, 100, 210, 21))
        try:self.email.setText(emailpass[0])
        except:pass
        self.email.setObjectName("email")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(110, 140, 210, 21))
        try:self.password.setText(emailpass[1])
        except:pass
        self.password.setObjectName("password")
        self.login = QtWidgets.QPushButton(Dialog)
        self.login.setGeometry(QtCore.QRect(170, 200, 150, 21))
        self.login.clicked.connect(self.firebaselogin)
        self.login.setObjectName("login")
        self.clickhere = QtWidgets.QPushButton(Dialog)
        self.clickhere.setGeometry(QtCore.QRect(30, 200, 100, 21))
        self.clickhere.clicked.connect(self.lostpass)
        self.clickhere.setObjectName("clickhere")
        self.checkbox = QtWidgets.QCheckBox(Dialog)
        self.checkbox.setGeometry(QtCore.QRect(240, 170, 80, 20))
        self.checkbox.setObjectName("checkbox")
        self.error = QtWidgets.QLabel(Dialog)
        self.error.setGeometry(QtCore.QRect(30, 220, 320, 21))
        self.error.setObjectName("error")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Binance Spot Bot | Giriş Yap"))
        self.label_1.setText(_translate("Dialog", "Binance Spot Bot"))
        self.label_2.setText(_translate("Dialog", "E-posta"))
        self.label_3.setText(_translate("Dialog", "Şifre"))
        self.checkbox.setText(_translate("Dialog", "Beni Hatırla"))
        self.login.setText(_translate("Dialog", "Giriş Yap"))
        self.clickhere.setText(_translate("Dialog", "Şifremi Unuttum!"))

    def firebaselogin(self):
        _translate = QtCore.QCoreApplication.translate
        emailfile = open('./bdata/loginemail','w')
        emailfile.write(str(self.email.text()))
        emailfile.close()
        deviceuuid = WMI().Win32_ComputerSystemProduct()[0].UUID
        db = firebase.database()
        data = {'UUID' : str(deviceuuid)}
        email = self.email.text()
        db.child(email.split("@")[0]).set(data)
        if self.checkbox.isChecked() == True:
            savedemail = self.email.text()
            savedpass = self.password.text()
            f = open( './bdata/loginuserinfo', 'w' )
            f.write(str(savedemail)+'\n'+str(savedpass))
            f.close()
        if self.email.text() != "" and self.password.text() != "":
            try:
                user = auth.sign_in_with_email_and_password(email = self.email.text(),password = self.password.text())
                self.ui = MainUi()
                Dialog.close()
                self.ui.show()
            except:
                self.error.setText(_translate("Dialog","E-posta veya şifre yanlış!"))
        else:
            self.error.setText(_translate("Dialog","E-posta ve şifre giriniz!"))

    def lostpass(self):
        _translate = QtCore.QCoreApplication.translate
        if self.email.text() != "":
            user = auth.send_password_reset_email(email = self.email.text())
            self.error.setText(_translate("Dialog","Şifre sıfırlama linki e-posta adresinize gönderildi!"))
        else:
            self.error.setText(_translate("Dialog","Lütfen e-posta alanını doldurunuz!"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
