from pymodbus.client import ModbusTcpClient
from PyQt5.QtWidgets import *
from PyQt5 import uic

import time

form_class=uic.loadUiType(f"./ui/ui_main.ui")[0]


class MainUi(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.client=None


        self.pb_connect.clicked.connect(self.connect)
        self.pb_w.pressed.connect(self.moveW);self.pb_w.released.connect(self.moveStop)
        self.pb_a.pressed.connect(self.moveA);self.pb_a.released.connect(self.moveStop)
        self.pb_s.pressed.connect(self.moveS);self.pb_s.released.connect(self.moveStop)
        self.pb_d.pressed.connect(self.moveD);self.pb_d.released.connect(self.moveStop)
        self.pb_space.pressed.connect(self.moveSpace)
        self.pb_l.pressed.connect(self.turnLeft);self.pb_l.released.connect(self.moveStop)
        self.pb_r.pressed.connect(self.turnRight);self.pb_r.released.connect(self.moveStop)

        



    def closeEvent(self,evt):
        if self.client != None:
            self.client.close()
            self.client=None


    def connect(self):
        if self.client != None:
            try:
                self.client.close()
                self.client = None
                self.gbox_control.setDisabled(True)
            except:
                self.label_network.setText("Network : 종료 오류, 재시도 요망")
        try:
            self.client=ModbusTcpClient(self.lineEdit_ip.text(),int(self.lineEdit_port.text()))
            self.client.connect()
            self.label_network.setText(f"Network : 연결됨({self.lineEdit_ip.text()}, {self.lineEdit_port.text()}")
            self.gbox_control.setEnabled(True)
            self.client.write_registers(130,0)
        except:
            self.label_network.setText("Network : 접속 오류, 재시도 요망")


    def moveStop(self):
        self.client.write_registers(130,0)
        print("stop!")

    def moveW(self):
        print("W")
        self.client.write_registers(130,1)

    def moveA(self):
        print("A")
        self.client.write_registers(130,2)

    def moveS(self):
        self.client.write_registers(130,3)

    def moveD(self):
        self.client.write_registers(130,4)

    def moveSpace(self):
        self.client.write_registers(130,5)
        print("space 행동!")

    def turnLeft(self):
        self.client.write_registers(130,6)

    def turnRight(self):
        self.client.write_registers(130,7)

if __name__=="__main__":
    app=QApplication([])
    w=MainUi()
    w.show()
    app.exec()