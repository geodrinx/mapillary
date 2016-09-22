# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapillary_dialog_base.ui'
#
# Created: Tue Jan 20 15:08:14 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mapillaryDialogBase(object):
    def setupUi(self, mapillaryDialogBase):
        mapillaryDialogBase.setObjectName(_fromUtf8("mapillaryDialogBase"))
        mapillaryDialogBase.resize(400, 300)
        self.button_box = QtGui.QDialogButtonBox(mapillaryDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(mapillaryDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), mapillaryDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), mapillaryDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(mapillaryDialogBase)

    def retranslateUi(self, mapillaryDialogBase):
        mapillaryDialogBase.setWindowTitle(_translate("mapillaryDialogBase", "mapillary", None))

