# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import math
import os
import random
import sys
import requests
from functools import partial


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_display_label = QtWidgets.QLabel(self.centralwidget)
        self.map_display_label.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.map_display_label.setText("")
        self.map_display_label.setObjectName("map_display_label")
        self.map_type_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.map_type_combobox.setGeometry(QtCore.QRect(610, 0, 111, 22))
        self.map_type_combobox.setObjectName("map_type_combobox")
        self.request_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.request_lineEdit.setGeometry(QtCore.QRect(610, 110, 280, 20))
        self.request_lineEdit.setObjectName("request_lineEdit")
        self.SeekForRequest_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.SeekForRequest_pushButton.setGeometry(QtCore.QRect(610, 130, 75, 25))
        self.SeekForRequest_pushButton.setObjectName("SeekForRequest_pushButton")
        self.clearRequestResult_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearRequestResult_pushButton.setGeometry(QtCore.QRect(740, 130, 150, 25))
        self.clearRequestResult_pushButton.setObjectName("clearRequestResult_pushButton")
        self.zoomPowerSlider = QtWidgets.QSlider(self.centralwidget)
        self.zoomPowerSlider.setGeometry(QtCore.QRect(830, 390, 22, 160))
        self.zoomPowerSlider.setMinimum(1)
        self.zoomPowerSlider.setMaximum(10)
        self.zoomPowerSlider.setOrientation(QtCore.Qt.Vertical)
        self.zoomPowerSlider.setObjectName("zoomPowerSlider")
        self.zoomPowerLabel = QtWidgets.QLabel(self.centralwidget)
        self.zoomPowerLabel.setGeometry(QtCore.QRect(800, 370, 91, 20))
        self.zoomPowerLabel.setObjectName("zoomPowerLabel")
        self.address_TextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.address_TextEdit.setGeometry(QtCore.QRect(610, 190, 271, 121))
        self.address_TextEdit.setObjectName("address_TextEdit")
        self.ShowIndex_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.ShowIndex_comboBox.setGeometry(QtCore.QRect(610, 160, 171, 22))
        self.ShowIndex_comboBox.setObjectName("ShowIndex_comboBox")
        self.org_type_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.org_type_lineEdit.setGeometry(QtCore.QRect(610, 340, 211, 21))
        self.org_type_lineEdit.setObjectName("org_type_lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(610, 320, 201, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.address_TextEdit.setReadOnly(True)
        self.ShowIndex_comboBox.addItem('Показывать почтовый индекс')
        self.ShowIndex_comboBox.addItem('Не показывать почтовый индекс')
        self.map_type_combobox.addItem('map')
        self.map_type_combobox.addItem('map,trf')
        self.map_type_combobox.addItem('sat')
        self.map_type_combobox.addItem('sat,skl')
        self.map_type_combobox.addItem('sat,trf')
        self.map_type_combobox.addItem('sat,trf,skl')
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.SeekForRequest_pushButton.clicked.connect(self.change_map)
        self.clearRequestResult_pushButton.clicked.connect(self.clear_point)
        self.setMouseTracking(True)
        self.ShowIndex_comboBox.currentTextChanged.connect(self.update_adress)
        self.json = 0
        self.map_params = {}
        self.delta_0 = 0
        self.delta_1 = 0
        self.ll_0 = 0
        self.ll_1 = 0
        self.request_lineEdit.setText('Барнаул')
        self.change_map()

    def lonlat_distance(self, a, b):
        degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
        a_lon, a_lat = a
        b_lon, b_lat = b

        # Берем среднюю по широте точку и считаем коэффициент для нее.
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)

        # Вычисляем смещения в метрах по вертикали и горизонтали.
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor

        # Вычисляем расстояние между точками.
        distance = math.sqrt(dx * dx + dy * dy)

        return distance

    def convert_pos_to_spn(self, upper, lower):
        upper = list(map(lambda x: float(x), upper.split()))
        lower = list(map(lambda x: float(x), lower.split()))
        return [abs(upper[0] - lower[0]) / 10, abs(upper[1] - lower[1]) / 10]

    def return_api(self, adress):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": adress,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        self.json = json_response
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.ll_0, self.ll_1 = list(map(lambda x: float(x), toponym["Point"]["pos"].split()))
        self.delta_0, self.delta_1 = self.convert_pos_to_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                                                             toponym['boundedBy']['Envelope']['upperCorner'])
        self.pt = f'{",".join(toponym["Point"]["pos"].split())},pm2dgl'
        self.map_params = {
            "ll": f'{self.ll_0},{self.ll_1}',
            "spn": f"{self.delta_0},{self.delta_1}",
            "l": f"{self.map_type_combobox.currentText()}",
            'pt': self.pt
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.update_adress()
        return requests.get(map_api_server, params=self.map_params)

    def update_adress(self):
        try:
            self.address_TextEdit.clear()
            if 'Не' in self.ShowIndex_comboBox.currentText():
                self.address_TextEdit.setPlainText(
                    f'Текущий адрес: {self.json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]}')
            else:
                self.address_TextEdit.setPlainText(
                    f'Текущий адрес: {self.json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]}, Почтовый индекс: {self.json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}')
        except BaseException:
            self.address_TextEdit.setPlainText(f'Текущий адрес: {self.request_lineEdit.text()}')

    def update_map(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.map_params = {
            "ll": f'{self.ll_0},{self.ll_1}',
            "spn": f"{self.delta_0},{self.delta_1}",
            "l": f"{self.map_type_combobox.currentText()}",
            'pt': self.pt
        }
        with open(f"map.png", "wb") as file:
            file.write(requests.get(map_api_server, params=self.map_params).content)
            file.close()
        self.map_display_label.setPixmap(QtGui.QPixmap("map.png"))

    def change_map(self):
        with open(f"map.png", "wb") as file:
            file.write(self.return_api(self.request_lineEdit.text()).content)
            file.close()
        self.map_display_label.setPixmap(QtGui.QPixmap("map.png"))

    def clear_point(self):
        self.pt = ''
        self.address_TextEdit.clear()
        self.address_TextEdit.setPlainText('Текущий адрес:')
        self.update_map()

    def keyPressEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        if event.key() == QtCore.Qt.Key_PageUp:
            self.delta_0 += 0.01 * self.zoomPowerSlider.value()
            self.delta_1 += 0.01 * self.zoomPowerSlider.value()
            self.update_map()
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.delta_0 > 0.01 * self.zoomPowerSlider.value() and self.delta_1 > 0.01 * self.zoomPowerSlider.value():
                self.delta_0 -= 0.01 * self.zoomPowerSlider.value()
                self.delta_1 -= 0.01 * self.zoomPowerSlider.value()
                self.update_map()
            else:
                self.delta_0 = 0.001
                self.delta_1 = 0.001
                self.update_map()
        elif event.key() == QtCore.Qt.Key_Left:
            self.ll_0 -= self.delta_0
            self.update_map()
        elif event.key() == QtCore.Qt.Key_Right:
            self.ll_0 += self.delta_0
            self.update_map()
        elif event.key() == QtCore.Qt.Key_Up:
            self.ll_1 += self.delta_1
            self.update_map()
        elif event.key() == QtCore.Qt.Key_Down:
            self.ll_1 -= self.delta_1
            self.update_map()

    def mousePressEvent(self, event):
        if 0 <= event.x() <= 600 and 0 <= event.y() <= 450:
            new_ll_0 = (self.ll_0 - self.delta_0 / 2) + (self.delta_0 / 600) * event.x()
            new_ll_1 = (self.ll_1 + self.delta_1 / 2) - (self.delta_1 / 450) * event.y()
            if event.button() == QtCore.Qt.LeftButton:
                geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

                geocoder_params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": f"{new_ll_0},{new_ll_1}",
                    "format": "json",
                    "kind": 'house'}

                response = requests.get(geocoder_api_server, params=geocoder_params)
                json_response = response.json()
                self.json = json_response
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

                self.pt = f'{",".join(toponym["Point"]["pos"].split())},pm2dgl'
                self.update_map()
                self.update_adress()
            if event.button() == QtCore.Qt.RightButton:
                search_api_server = "https://search-maps.yandex.ru/v1/"
                api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

                address_ll = f'{new_ll_0},{new_ll_1}'

                search_params = {
                    "apikey": api_key,
                    'text': self.org_type_lineEdit.text(),
                    "lang": "ru_RU",
                    "ll": address_ll,
                    "type": "biz"
                }

                response = requests.get(search_api_server, params=search_params)
                json_response = response.json()
                organization = json_response["features"][0]
                point = organization["geometry"]["coordinates"]
                if self.lonlat_distance([new_ll_0, new_ll_1], [point[0], point[1]]) < 51:
                    self.pt = f'{point[0]},{point[1]},pm2dgl'
                    self.update_map()
                    self.address_TextEdit.clear()
                    self.address_TextEdit.setPlainText('Текущий адрес:')
                else:
                    self.pt = ''
                    self.update_map()
                    self.address_TextEdit.clear()
                    self.address_TextEdit.setPlainText('Текущий адрес:')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SeekForRequest_pushButton.setText(_translate("MainWindow", "Искать"))
        self.clearRequestResult_pushButton.setText(_translate("MainWindow", "Сброс результатов поиска"))
        self.zoomPowerLabel.setText(_translate("MainWindow", "Сила отдаления"))
        self.address_TextEdit.setPlainText(_translate("MainWindow", "Текущий адрес:"))
        self.org_type_lineEdit.setText(_translate("MainWindow", "Аптека"))
        self.label.setText(_translate("MainWindow", "Тип организации для поиска"))
