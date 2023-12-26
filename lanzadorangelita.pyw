import sys
import re
import os
import MySQLdb
from Tkinter import *
import tkMessageBox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Image
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak,
Image, Spacer)
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from datetime import date
import datetime
import ctypes
from sistemaangelita import *

class MiForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.mdiArea.addSubWindow(self.ui.ayuda)
        self.ui.mdiArea.addSubWindow(self.ui.modificarproductos)
        self.ui.mdiArea.addSubWindow(self.ui.controlstock)
        self.ui.mdiArea.addSubWindow(self.ui.ventadeproductosv2)
        self.ui.mdiArea.addSubWindow(self.ui.compraproductosv2)
        self.ui.mdiArea.addSubWindow(self.ui.altaproductos)
        self.ui.mdiArea.addSubWindow(self.ui.infomes)
        self.ui.mdiArea.addSubWindow(self.ui.modificarinsumos)
        self.ui.mdiArea.addSubWindow(self.ui.stockinsumos)
        self.ui.mdiArea.addSubWindow(self.ui.gastodeinsumos)
        self.ui.mdiArea.addSubWindow(self.ui.compradeinsumos)
        self.ui.mdiArea.addSubWindow(self.ui.altadeinsumos)
        self.ui.mdiArea.addSubWindow(self.ui.ventarotiseria)
        self.ui.mdiArea.addSubWindow(self.ui.inicio)
        QtCore.QObject.connect(self.ui.buttonaceptaralt, QtCore.SIGNAL('clicked()'), self.altaproductos)
        QtCore.QObject.connect(self.ui.buttonaceptarcs, QtCore.SIGNAL('clicked()'), self.controlstock)
        QtCore.QObject.connect(self.ui.radiomp, QtCore.SIGNAL('clicked()'), self.habilitarono)
        QtCore.QObject.connect(self.ui.buttonconsultarmp, QtCore.SIGNAL('clicked()'), self.consultarproductos)
        QtCore.QObject.connect(self.ui.buttonmodificarmp, QtCore.SIGNAL('clicked()'), self.modificarproductos)
        QtCore.QObject.connect(self.ui.buttonaceptarep, QtCore.SIGNAL('clicked()'), self.eliminarproductos)
        QtCore.QObject.connect(self.ui.buttoncomprasinf, QtCore.SIGNAL('clicked()'), self.informescompras)
        QtCore.QObject.connect(self.ui.buttonventasinf, QtCore.SIGNAL('clicked()'), self.informesventas)
        QtCore.QObject.connect(self.ui.linecodigoalt, QtCore.SIGNAL('returnPressed()'), self.vercodigoalt)
        QtCore.QObject.connect(self.ui.lineprecioalt, QtCore.SIGNAL('returnPressed()'), self.verprecioalt)
        QtCore.QObject.connect(self.ui.linecantidadalt, QtCore.SIGNAL('returnPressed()'), self.vercantidadalt)
        QtCore.QObject.connect(self.ui.linereposicionalt, QtCore.SIGNAL('returnPressed()'), self.verreposicionalt)
        QtCore.QObject.connect(self.ui.linecodigocom, QtCore.SIGNAL('returnPressed()'), self.vercodigocom)
        QtCore.QObject.connect(self.ui.linecantidadcom, QtCore.SIGNAL('returnPressed()'), self.vercantidadcom)
        QtCore.QObject.connect(self.ui.linecodigo, QtCore.SIGNAL('returnPressed()'), self.vercodigoven)
        QtCore.QObject.connect(self.ui.linecantidad, QtCore.SIGNAL('returnPressed()'), self.vercantidadven)
        QtCore.QObject.connect(self.ui.linecodigocs, QtCore.SIGNAL('returnPressed()'), self.vercodigocs)
        QtCore.QObject.connect(self.ui.linecodigocs, QtCore.SIGNAL('returnPressed()'), self.vercodigocs)
        QtCore.QObject.connect(self.ui.linecodigomp, QtCore.SIGNAL('returnPressed()'), self.vercodigomp)
        QtCore.QObject.connect(self.ui.linecodigocs, QtCore.SIGNAL('returnPressed()'), self.vercodigocs)
        QtCore.QObject.connect(self.ui.linepreciomp, QtCore.SIGNAL('returnPressed()'), self.verpreciomp)
        QtCore.QObject.connect(self.ui.linecantidadmp, QtCore.SIGNAL('returnPressed()'), self.vercantidadmp)
        QtCore.QObject.connect(self.ui.linereposicionmp, QtCore.SIGNAL('returnPressed()'), self.verreposicionmp)
        QtCore.QObject.connect(self.ui.linecodigocs, QtCore.SIGNAL('returnPressed()'), self.vercodigocs)
        QtCore.QObject.connect(self.ui.linecodigoep, QtCore.SIGNAL('returnPressed()'), self.vercodigoep)
        QtCore.QObject.connect(self.ui.linefechavr, QtCore.SIGNAL('returnPressed()'), self.fechahoy)
        QtCore.QObject.connect(self.ui.btnsumarvr, QtCore.SIGNAL('clicked()'), self.sumaritem)
        QtCore.QObject.connect(self.ui.btnborrarvr, QtCore.SIGNAL('clicked()'), self.borraritem)
        QtCore.QObject.connect(self.ui.btnborrartodovr, QtCore.SIGNAL('clicked()'), self.borrartodo)
        QtCore.QObject.connect(self.ui.btnveritemvr, QtCore.SIGNAL('clicked()'), self.veritem)
        QtCore.QObject.connect(self.ui.btnaceptarvr, QtCore.SIGNAL('clicked()'), self.ventasrotiseria)
        QtCore.QObject.connect(self.ui.btnaceptarvp2, QtCore.SIGNAL('clicked()'), self.ventasproductosv2)
        QtCore.QObject.connect(self.ui.btnsumarvp2, QtCore.SIGNAL('clicked()'), self.sumaritemvp2)
        QtCore.QObject.connect(self.ui.btnborrarvp2, QtCore.SIGNAL('clicked()'), self.borraritemvp2)
        QtCore.QObject.connect(self.ui.btnborrartodovp2, QtCore.SIGNAL('clicked()'), self.borrartodovp2)
        QtCore.QObject.connect(self.ui.btnaceptarvp2, QtCore.SIGNAL('returnPressed()'), self.ventasproductosv2)
        QtCore.QObject.connect(self.ui.linefechavp2, QtCore.SIGNAL('returnPressed()'), self.fechahoyvp2)
        QtCore.QObject.connect(self.ui.buttonrotiseriainf, QtCore.SIGNAL('clicked()'), self.informesrotiseria)
        QtCore.QObject.connect(self.ui.btnveritemvp2, QtCore.SIGNAL('clicked()'), self.veritemvp2)
        QtCore.QObject.connect(self.ui.btnsumarcp2, QtCore.SIGNAL('clicked()'), self.sumaritemcp2)
        QtCore.QObject.connect(self.ui.btnborrarcp2, QtCore.SIGNAL('clicked()'), self.borraritemcp2)
        QtCore.QObject.connect(self.ui.btnborrartodocp2, QtCore.SIGNAL('clicked()'), self.borrartodocp2)
        QtCore.QObject.connect(self.ui.btnveritemcp2, QtCore.SIGNAL('clicked()'), self.veritemcp2)
        QtCore.QObject.connect(self.ui.linefechacp2, QtCore.SIGNAL('returnPressed()'), self.fechahoycp2)
        QtCore.QObject.connect(self.ui.btnaceptarcp2, QtCore.SIGNAL('clicked()'), self.compraproductosv2)
        QtCore.QObject.connect(self.ui.linecodigoalt, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesalt)
        QtCore.QObject.connect(self.ui.linecodigomp, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescop)
        QtCore.QObject.connect(self.ui.radiomp, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesmop)
        QtCore.QObject.connect(self.ui.linecodigocs, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescos)
        QtCore.QObject.connect(self.ui.linefechad, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesinf)
        QtCore.QObject.connect(self.ui.linedescripcionvr, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesrot)
        QtCore.QObject.connect(self.ui.linecodigovp2, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesven)
        QtCore.QObject.connect(self.ui.linecodigocp2, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescom)
        QtCore.QObject.connect(self.ui.buttoncancelarcs, QtCore.SIGNAL('clicked()'), self.limpiarstock)
        QtCore.QObject.connect(self.ui.btncancelarcp2, QtCore.SIGNAL('clicked()'), self.limpiarlistacom)
        QtCore.QObject.connect(self.ui.btncancelarvp2, QtCore.SIGNAL('clicked()'), self.limpiarlistaven)
        QtCore.QObject.connect(self.ui.btncancelarvr, QtCore.SIGNAL('clicked()'), self.limpiarlistarot)
        QtCore.QObject.connect(self.ui.buttonaceptaraltins, QtCore.SIGNAL('clicked()'), self.altainsumos)
        QtCore.QObject.connect(self.ui.btnaceptarcomins, QtCore.SIGNAL('clicked()'), self.comprainsumos)
        QtCore.QObject.connect(self.ui.btnsumarcomins, QtCore.SIGNAL('clicked()'), self.sumaritemcomins)
        QtCore.QObject.connect(self.ui.btnborrarcomins, QtCore.SIGNAL('clicked()'), self.borraritemcomins)
        QtCore.QObject.connect(self.ui.btnborrartodocomins, QtCore.SIGNAL('clicked()'), self.borrartodocomins)
        QtCore.QObject.connect(self.ui.btncancelarcomins, QtCore.SIGNAL('clicked()'), self.limpiarlistacomins)
        QtCore.QObject.connect(self.ui.btnveritemcomins, QtCore.SIGNAL('clicked()'), self.veritemcomins)
        QtCore.QObject.connect(self.ui.linefechacomins, QtCore.SIGNAL('returnPressed()'), self.fechahoycomins)
        QtCore.QObject.connect(self.ui.btnsumargasins, QtCore.SIGNAL('clicked()'), self.sumaritemgasins)
        QtCore.QObject.connect(self.ui.btnborrargasins, QtCore.SIGNAL('clicked()'), self.borraritemgasins)
        QtCore.QObject.connect(self.ui.btnborrartodogasins, QtCore.SIGNAL('clicked()'), self.borrartodogasins)
        QtCore.QObject.connect(self.ui.btncancelargasins, QtCore.SIGNAL('clicked()'), self.limpiarlistagasins)
        QtCore.QObject.connect(self.ui.btnveritemgasins, QtCore.SIGNAL('clicked()'), self.veritemgasins)
        QtCore.QObject.connect(self.ui.linefechagasins, QtCore.SIGNAL('returnPressed()'), self.fechahoygasins)
        QtCore.QObject.connect(self.ui.btnaceptargasins, QtCore.SIGNAL('clicked()'), self.gastoinsumos)
        QtCore.QObject.connect(self.ui.buttonaceptarcsi, QtCore.SIGNAL('clicked()'), self.controlstockinsumos)
        QtCore.QObject.connect(self.ui.buttonciinf, QtCore.SIGNAL('clicked()'), self.informecomprasinsumos)
        QtCore.QObject.connect(self.ui.buttongiinf, QtCore.SIGNAL('clicked()'), self.informegastosinsumos)
        QtCore.QObject.connect(self.ui.radiomi, QtCore.SIGNAL('clicked()'), self.habilitaronoins)
        QtCore.QObject.connect(self.ui.buttonconsultarmi, QtCore.SIGNAL('clicked()'), self.consultarinsumos)
        QtCore.QObject.connect(self.ui.buttonmodificarmi, QtCore.SIGNAL('clicked()'), self.modificarinsumos)
        QtCore.QObject.connect(self.ui.linecodigoaltins, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesaltins)
        QtCore.QObject.connect(self.ui.linecodigocomins, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescomins)
        QtCore.QObject.connect(self.ui.linecodigogasins, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesgasins)
        QtCore.QObject.connect(self.ui.linecodigocsi, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescosins)
        QtCore.QObject.connect(self.ui.linecodigomi, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplescopins)
        QtCore.QObject.connect(self.ui.radiomi, QtCore.SIGNAL('editingFinished()'), self.operacionesmultiplesmopins)
        QtCore.QObject.connect(self.ui.buttoncancelarmp, QtCore.SIGNAL('clicked()'), self.habilitarcodigomp)
        QtCore.QObject.connect(self.ui.buttoncancelarmi, QtCore.SIGNAL('clicked()'), self.habilitarcodigomi)

    def habilitarcodigomp(self):
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linecodigomp.setFocus()
        self.ui.radiomp.setEnabled(False)
        self.ui.buttonconsultarmp.setEnabled(True)
        self.ui.buttonmodificarmp.setEnabled(False)
        self.ui.buttoncancelarmp.setEnabled(True)

    def habilitarcodigomi(self):
        self.ui.linecodigomi.setEnabled(True)
        self.ui.linecodigomi.setFocus()
        self.ui.radiomi.setEnabled(False)
        self.ui.buttonconsultarmi.setEnabled(True)
        self.ui.buttonmodificarmi.setEnabled(False)
        self.ui.buttoncancelarmi.setEnabled(True)

    def vercodigoalt(self):
        aux = self.ui.linecodigoalt.text()
        if not re.match("^[0-9]{13}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo de 13 digitos")
            self.ui.mdiArea.setEnabled(True)


    def verprecioalt(self):
        aux = self.ui.lineprecioalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar precio entero o decimal positivo")
            self.ui.mdiArea.setEnabled(True)

    def vercantidadalt(self):
        aux = self.ui.linecantidadalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar cantidad entera o decimal positiva")
            self.ui.mdiArea.setEnabled(True)

    def verreposicionalt(self):
        aux = self.ui.linereposicionalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar reposicion entera o decimal positiva")
            self.ui.mdiArea.setEnabled(True)

    def vercodigocom(self):
        aux = self.ui.linecodigocom.text()
        if not re.match("^[0-9]{13}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo entero de 13 digitos positivo")
            self.ui.mdiArea.setEnabled(True)

    def vercantidadcom(self):
        aux = self.ui.linecantidadcom.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar cantidad entera o decimal positiva")
            self.ui.mdiArea.setEnabled(True)

    def vercodigoven(self):
        aux = self.ui.linecodigo.text()
        if not re.match("^[0-9]{13}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo entero de 13 digitos positivo")
           self.ui.mdiArea.setEnabled(True)

    def vercantidadven(self):
        aux = self.ui.linecantidad.text()
        if not re.match("^[0-9.]{1,6}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar cantidad entera o decimal positiva")
           self.ui.mdiArea.setEnabled(True)


    def vercodigocs(self):
        aux = self.ui.linecodigocs.text()
        if not re.match("^[0-9]{13}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo entero de 13 digitos positivo")
           self.ui.mdiArea.setEnabled(True)

    def vercodigomp(self):
        aux = self.ui.linecodigomp.text()
        if not re.match("^[0-9]{13}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo entero de 13 digitos positivo")
           self.ui.mdiArea.setEnabled(True)

    def verpreciomp(self):
        aux = self.ui.linepreciomp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar precio entero o decimal positivo")
           self.ui.mdiArea.setEnabled(True)

    def vercantidadmp(self):
        aux = self.ui.linecantidadmp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar cantidad entera o decimal positiva")
           self.ui.mdiArea.setEnabled(True)

    def verreposicionmp(self):
        aux = self.ui.linereposicionmp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar reposicion entera o decimal positiva")
           self.ui.mdiArea.setEnabled(True)

    def vercodigoep(self):
        aux = self.ui.linecodigoep.text()
        if not re.match("^[0-9]{13}$", aux):
           self.ui.mdiArea.setEnabled(False)
           window = Tk()
           window.wm_withdraw()
           tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar codigo entero de 13 digitos positivo")
           self.ui.mdiArea.setEnabled(True)

    def limpiarstock(self):
        self.ui.linecodigovistacs.setText('')
        self.ui.linedescripcioncs.setText('')
        self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText('')
        self.ui.linereponeronocs.setText('')
        self.ui.linecodigocs.setFocus()

    def limpiarlistacom(self):
        self.ui.listwidgetcp2.clear()
        listacom[:] = []
        self.ui.linepretotcp2.setText('')
        self.ui.lineitemcp2.setText('')

    def limpiarlistaven(self):
        self.ui.listwidgetvp2.clear()
        lista[:] = []
        self.ui.linepretotvp2.setText('')
        self.ui.lineitemvp2.setText('')

    def limpiarlistarot(self):
        self.ui.listwidgetvr.clear()
        listarot[:] = []
        self.ui.linepretotvr.setText('')
        self.ui.lineitemvr.setText('')

    def altaproductos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        ade = ''
        apr = ''
        aca = ''
        are = ''
        aux = self.ui.linecodigoalt.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo, '
        aux = self.ui.linedescripcionalt.text()
        if aux == '':
            ade = 'descripcion, '
        aux = self.ui.lineprecioalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            apr = 'precio, '
        aux = self.ui.linecantidadalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad, '
        aux = self.ui.linereposicionalt.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            are = 'reposicion'
        if ade != '' or aco != '' or apr != '' or aca != '' or are != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + aco + ade + apr + aca + are)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigoalt.setFocus()
        else:
            cod = int(self.ui.linecodigoalt.text())
            des = self.ui.linedescripcionalt.text()
            pre = float(self.ui.lineprecioalt.text())
            can = float(self.ui.linecantidadalt.text())
            rep = float(self.ui.linereposicionalt.text())
            try:
                cursor.execute("Select *from productos where pro_cod=%d" % cod)
                row = cursor.fetchone()
                if row is not None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="Ya existe un producto con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                else:
                    cursor.execute("""
                    INSERT INTO productos(pro_cod, pro_des, pro_pre, pro_can, pro_rep)
                    VALUES(%d,'%s', %d, %d, %d)
                    """ % (cod, des, pre, can, rep))
                    conn.commit()
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="El producto ha ingresado correctamente")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigoalt.setText("")
                    self.ui.linedescripcionalt.setText("")
                    self.ui.lineprecioalt.setText("")
                    self.ui.linecantidadalt.setText("")
                    self.ui.linereposicionalt.setText("")
                    self.ui.linecodigoalt.setFocus()
            except MySQLdb.Error:
                    conn.rollback()
                    sys.exit(1)
            cursor.close()
            conn.close()

    def altainsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        ade = ''
        apr = ''
        aca = ''
        are = ''
        aux = self.ui.linecodigoaltins.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo, '
        aux = self.ui.linedescripcionaltins.text()
        if aux == '':
            ade = 'descripcion, '
        aux = self.ui.lineprecioaltins.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            apr = 'precio, '
        aux = self.ui.linecantidadaltins.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad, '
        aux = self.ui.linereposicionaltins.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            are = 'reposicion'
        if ade != '' or aco != '' or apr != '' or aca != '' or are != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + aco + ade + apr + aca + are)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigoalt.setFocus()
        else:
            cod = int(self.ui.linecodigoaltins.text())
            des = self.ui.linedescripcionaltins.text()
            pre = float(self.ui.lineprecioaltins.text())
            can = float(self.ui.linecantidadaltins.text())
            rep = float(self.ui.linereposicionaltins.text())
            try:
                cursor.execute("Select *from insumos where ins_cod=%d" % cod)
                row = cursor.fetchone()
                if row is not None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="Ya existe un insumo con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                else:
                    cursor.execute("""
                    INSERT INTO insumos(ins_cod, ins_des, ins_pre, ins_can, ins_rep)
                    VALUES(%d,'%s', %d, %d, %d)
                    """ % (cod, des, pre, can, rep))
                    conn.commit()
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="El insumo ha ingresado correctamente")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigoaltins.setText("")
                    self.ui.linedescripcionaltins.setText("")
                    self.ui.lineprecioaltins.setText("")
                    self.ui.linecantidadaltins.setText("")
                    self.ui.linereposicionaltins.setText("")
                    self.ui.linecodigoaltins.setFocus()
            except MySQLdb.Error:
                    conn.rollback()
                    sys.exit(1)
            cursor.close()
            conn.close()

    def controlstock(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigocs.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocs.setFocus()
        else:
            cod = int(self.ui.linecodigocs.text())
            try:
                cursor.execute("Select *from productos where pro_cod=%d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun producto con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigocs.setFocus()
                else:
                    self.ui.linecodigovistacs.setText(str(row[0]))
                    self.ui.linedescripcioncs.setText(str(row[1]))
                    self.ui.linestockcs.setText(str(row[3]))
                    self.ui.linepuntoreposicioncs.setText(str(row[4]))
                    aux = row[3] - row[4]
                    if aux > 0:
                        self.ui.linereponeronocs.setText("No reponer producto: " + str(aux))
                    else:
                        self.ui.linereponeronocs.setText("Reponer producto: " + str(aux))
                    self.ui.linecodigocs.setText('')
                    self.ui.linecodigocs.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def controlstockinsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigocsi.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocsi.setFocus()
        else:
            cod = int(self.ui.linecodigocsi.text())
            try:
                cursor.execute("Select *from insumos where ins_cod=%d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun insumo con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigocsi.setFocus()
                else:
                    self.ui.linecodigovistacsi.setText(str(row[0]))
                    self.ui.linedescripcioncsi.setText(str(row[1]))
                    self.ui.linestockcsi.setText(str(row[3]))
                    self.ui.linepuntoreposicioncsi.setText(str(row[4]))
                    aux = row[3] - row[4]
                    if aux > 0:
                        self.ui.linereponeronocsi.setText("No reponer insumo: " + str(aux))
                    else:
                        self.ui.linereponeronocsi.setText("Reponer insumo: " + str(aux))
                    self.ui.linecodigocsi.setText('')
                    self.ui.linecodigocsi.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def habilitarono(self):
        if self.ui.radiomp.isChecked()== True:
            self.ui.buttonmodificarmp.setEnabled(True)
            self.ui.buttonconsultarmp.setEnabled(False)
            self.ui.linecodigomp.setEnabled(False)
            self.ui.linenombremp.setEnabled(True)
            self.ui.linepreciomp.setEnabled(True)
            self.ui.linecantidadmp.setEnabled(True)
            self.ui.linereposicionmp.setEnabled(True)
            self.ui.buttoncancelarmp.setEnabled(False)
        else:
            self.ui.buttonmodificarmp.setEnabled(False)
            self.ui.buttonconsultarmp.setEnabled(True)
            self.ui.linecodigomp.setEnabled(False)
            self.ui.linenombremp.setEnabled(False)
            self.ui.linepreciomp.setEnabled(False)
            self.ui.linecantidadmp.setEnabled(False)
            self.ui.linereposicionmp.setEnabled(False)
            self.ui.buttoncancelarmp.setEnabled(True)
            if self.ui.linecodigomp.text()== '':
                self.ui.radiomp.setEnabled(False)

    def habilitaronoins(self):
        if self.ui.radiomi.isChecked()== True:
            self.ui.buttonmodificarmi.setEnabled(True)
            self.ui.buttonconsultarmi.setEnabled(False)
            self.ui.linecodigomi.setEnabled(False)
            self.ui.linenombremi.setEnabled(True)
            self.ui.linepreciomi.setEnabled(True)
            self.ui.linecantidadmi.setEnabled(True)
            self.ui.linereposicionmi.setEnabled(True)
            self.ui.buttoncancelarmi.setEnabled(False)
        else:
            self.ui.buttonmodificarmi.setEnabled(False)
            self.ui.buttonconsultarmi.setEnabled(True)
            self.ui.linecodigomi.setEnabled(False)
            self.ui.linenombremi.setEnabled(False)
            self.ui.linepreciomi.setEnabled(False)
            self.ui.linecantidadmi.setEnabled(False)
            self.ui.linereposicionmi.setEnabled(False)
            self.ui.buttoncancelarmi.setEnabled(True)
            if self.ui.linecodigomi.text()== '':
                self.ui.radiomi.setEnabled(False)

    def consultarproductos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigomp.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigomp.setFocus()
        else:
            cod = int(self.ui.linecodigomp.text())
            try:
                cursor.execute("Select *from productos where pro_cod=%d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun producto")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigomp.setFocus()
                else:
                    self.ui.linecodigomp.setEnabled(False)
                    self.ui.radiomp.setEnabled(True)
                    self.ui.linenombremp.setText(str(row[1]))
                    self.ui.linepreciomp.setText(str(row[2]))
                    self.ui.linecantidadmp.setText(str(row[3]))
                    self.ui.linereposicionmp.setText(str(row[4]))
                    self.ui.radiomp.setChecked(0)
                    self.ui.buttonconsultarmp.setEnabled(False)
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def consultarinsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigomi.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigomi.setFocus()
        else:
            cod = int(self.ui.linecodigomi.text())
            try:
                cursor.execute("Select *from insumos where ins_cod=%d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun insumo")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigomi.setFocus()
                else:
                    self.ui.linecodigomi.setEnabled(False)
                    self.ui.radiomi.setEnabled(True)
                    self.ui.linenombremi.setText(str(row[1]))
                    self.ui.linepreciomi.setText(str(row[2]))
                    self.ui.linecantidadmi.setText(str(row[3]))
                    self.ui.linereposicionmi.setText(str(row[4]))
                    self.ui.radiomi.setChecked(0)
                    self.ui.buttonconsultarmi.setEnabled(False)
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def modificarproductos(self):
        #conn = conectar()
        #cursor = conn.cursor()
        aco = ''
        apr = ''
        aca = ''
        are = ''
        aux = self.ui.linecodigomp.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        aux = self.ui.linepreciomp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            apr = 'precio'
        aux = self.ui.linecantidadmp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad'
        aux = self.ui.linereposicionmp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            are = 'reposicion'
        if aco != '' or apr != '' or aca != '' or are != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco + ',' +apr + ',' + aca + ',' + are)
            self.ui.mdiArea.setEnabled(True)
        else:
            #conn2 = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="angelita")
            conn2 = conectar()
            cursor2 = conn2.cursor()
            cod = int(self.ui.linecodigomp.text())
            nom = str(self.ui.linenombremp.text())
            pre = float(self.ui.linepreciomp.text())
            can = float(self.ui.linecantidadmp.text())
            rep = float(self.ui.linereposicionmp.text())
            try:
                cursor2.execute("Update productos set pro_des='%s', pro_pre=%d, pro_can=%d, pro_rep=%d where pro_cod=%d" % (
                    nom, pre, can, rep, cod))
                conn2.commit()
                self.ui.linecodigomp.setText('')
                self.ui.linenombremp.setText('')
                self.ui.linepreciomp.setText('')
                self.ui.linecantidadmp.setText('')
                self.ui.linereposicionmp.setText('')
                self.ui.buttonmodificarmp.setEnabled(False)
                self.ui.buttonconsultarmp.setEnabled(True)
                self.ui.buttoncancelarmp.setEnabled(True)
                self.ui.radiomp.setEnabled(False)
                self.ui.linecodigomp.setEnabled(True)
                self.ui.linenombremp.setEnabled(False)
                self.ui.linepreciomp.setEnabled(False)
                self.ui.linecantidadmp.setEnabled(False)
                self.ui.linereposicionmp.setEnabled(False)
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El producto se modifico correctamente")
                self.ui.mdiArea.setEnabled(True)
                self.ui.linecodigomp.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor2.close()
            conn2.close()

    def modificarinsumos(self):
        #conn = conectar()
        #cursor = conn.cursor()
        aco = ''
        apr = ''
        aca = ''
        are = ''
        aux = self.ui.linecodigomi.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        aux = self.ui.linepreciomi.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            apr = 'precio'
        aux = self.ui.linecantidadmi.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad'
        aux = self.ui.linereposicionmi.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            are = 'reposicion'
        if aco != '' or apr != '' or aca != '' or are != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco + ',' +apr + ',' + aca + ',' + are)
            self.ui.mdiArea.setEnabled(True)
        else:
            #conn2 = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="angelita")
            conn2 = conectar()
            cursor2 = conn2.cursor()
            cod = int(self.ui.linecodigomi.text())
            nom = str(self.ui.linenombremi.text())
            pre = float(self.ui.linepreciomi.text())
            can = float(self.ui.linecantidadmi.text())
            rep = float(self.ui.linereposicionmi.text())
            try:
                cursor2.execute("Update insumos set ins_des='%s', ins_pre=%d, ins_can=%d, ins_rep=%d where ins_cod=%d" % (
                    nom, pre, can, rep, cod))
                conn2.commit()
                self.ui.linecodigomi.setText('')
                self.ui.linenombremi.setText('')
                self.ui.linepreciomi.setText('')
                self.ui.linecantidadmi.setText('')
                self.ui.linereposicionmi.setText('')
                self.ui.buttonmodificarmi.setEnabled(False)
                self.ui.buttonconsultarmi.setEnabled(True)
                self.ui.buttoncancelarmi.setEnabled(True)
                self.ui.radiomi.setEnabled(False)
                self.ui.linecodigomi.setEnabled(True)
                self.ui.linenombremi.setEnabled(False)
                self.ui.linepreciomi.setEnabled(False)
                self.ui.linecantidadmi.setEnabled(False)
                self.ui.linereposicionmi.setEnabled(False)
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El insumo se modifico correctamente")
                self.ui.mdiArea.setEnabled(True)
                self.ui.linecodigomi.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor2.close()
            conn2.close()

    def eliminarproductos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigoep.text()
        if not re.match("^[0-9]{13}$", aux):
            aco = 'codigo'
        if aco != '':
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
        else:
            cod = int(self.ui.linecodigoep.text())
            try:
                cursor.execute("Delete from productos where pro_cod=%d" % cod)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El producto se elimino correctamente.")
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.commit()
            conn.close()

    def informescompras(self):
        conn = conectar()
        cursor = conn.cursor()
        #story=[]
        fechad= self.ui.linefechad.text()
        fechah= self.ui.linefechah.text()
        fec = verificar(fechad, fechah)
        if(fec!=""):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar las fechas:"+fec)
            self.ui.mdiArea.setEnabled(True)
        else:
            fechadlis= fechad.split('/')
            fechahlis= fechah.split('/')
            lon= longitudysolonumeros(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
            if(lon!=""):
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe completar bien: "+lon)
                self.ui.mdiArea.setEnabled(True)
            else:
                erf= errorfecha(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
                if(erf!=""):
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message=erf)
                    self.ui.mdiArea.setEnabled(True)
                else:
                    lafechad= '-'.join([str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0])])
                    lafechah= '-'.join([str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0])])
                    try:
                        ssql = "SELECT coc_nro, DATE_FORMAT(coc_fec,'%d/%m/20%y')as fec FROM comcab "
                        ssql+= "WHERE coc_fec >= '" + lafechad + "' AND coc_fec <= '" + lafechah + "' ORDER BY coc_fec, coc_nro"
                        cursor.execute(ssql)
                        rows = cursor.fetchall()
                        print rows
                        if len(rows)== 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="No se encontro ninguna compra.")
                            self.ui.mdiArea.setEnabled(True)
                        else:
                            tot = 0
                            sut = 0
                            suc = 0
                            tco = 0
                            ant = rows[0][1]
                            ant2 = rows[0][0]
                            estilo = getSampleStyleSheet()
                            story = []
                            fichero_imagen = "logoinf.png"
                            imagen_logo = Image(os.path.realpath(fichero_imagen),width=108,height=34)
                            story.append(imagen_logo)
                            cabecera = estilo['Heading4']
                            cabecera.pageBreakBefore=0
                            cabecera.keepWithNext=0
                            cabecera.backColor=colors.red
                            fecha = datetime.date.today()
                            hoy = fecha.strftime("%d/%m/20%y")
                            titulo = "INFORME DE COMPRAS DE PRODUCTOS, FECHA: " + str(hoy)
                            parrafo = Paragraph(titulo ,cabecera)
                            story.append(parrafo)
                            t=Table([["","","",""]],colWidths=120, rowHeights=30)
                            story.append(t)
                            t=Table([['Fecha: ',ant,'','']],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            for row in rows:
                                if row[1]!= ant:
                                    t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    t=Table([['Fecha: ',row[1],'','']],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                                    story.append(t)
                                    tot = tot + sut
                                    suc = 0
                                    sut = 0
                                    ant= row[1]
                                t=Table([['Nro de compra: ',row[0],'','']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                t=Table([['Descripcion','Cantidad','Precio','Subtotal']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                nco = int(row[0])
                                ssql2 = "SELECT pro_des, com_can, com_pre, com_can * com_pre AS sub "
                                ssql2+= "FROM compras INNER JOIN productos ON com_pro = pro_cod WHERE com_nco = %d" % nco
                                cursor.execute(ssql2)
                                rows2 = cursor.fetchall()
                                print rows2[0][0]
                                for row2 in rows2:
                                    t=Table([[row2[0],row2[1],row2[2],row2[3]]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),])
                                    story.append(t)
                                    suc = suc + float(row2[3])
                                t=Table([['','','Subtotal:',suc]],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                sut = sut + suc
                                suc = 0
                                tco = tco + 1
                            t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                            story.append(t)
                            tot = tot + sut
                            t=Table([["","","Monto Total:",tot]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Total de Compras:",tco]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Promedio:",round(tot/tco,2)]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            os.chdir('C:/Users/Lenovo/Desktop/informes')
                            doc=SimpleDocTemplate("comprassaborfeliz.pdf",pagesize=A4)
                            doc.build(story)
                            os.system('comprassaborfeliz.pdf')
                    except MySQLdb.Error:
                           print "Error"
                           sys.exit(1)
                    cursor.close()
                    conn.close()

    def informesventas(self):
        conn = conectar()
        cursor = conn.cursor()
        story=[]
        fechad= self.ui.linefechad.text()
        fechah= self.ui.linefechah.text()
        fec = verificar(fechad, fechah)
        if(fec!=""):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar las fechas:"+fec)
            self.ui.mdiArea.setEnabled(True)
        else:
            fechadlis= fechad.split('/')
            fechahlis= fechah.split('/')
            lon= longitudysolonumeros(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
            if(lon!=""):
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe completar bien: "+lon)
                self.ui.mdiArea.setEnabled(True)
            else:
                erf= errorfecha(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
                if(erf!=""):
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message=erf)
                    self.ui.mdiArea.setEnabled(True)
                else:
                    lafechad= '-'.join([str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0])])
                    lafechah= '-'.join([str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0])])
                    try:
                        ssql = "SELECT vec_nro, DATE_FORMAT(vec_fec,'%d/%m/20%y')as fec FROM vencab "
                        ssql+= "WHERE vec_fec >= '" + lafechad + "' AND vec_fec <= '" + lafechah + "' ORDER BY vec_fec, vec_nro"
                        cursor.execute(ssql)
                        rows = cursor.fetchall()
                        print rows
                        if len(rows)== 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="No se encontro ninguna venta.")
                            self.ui.mdiArea.setEnabled(True)
                        else:
                            tot = 0
                            sut = 0
                            suv = 0
                            tve = 0
                            ant = rows[0][1]
                            ant2 = rows[0][0]
                            estilo = getSampleStyleSheet()
                            story = []
                            fichero_imagen = "logoinf.png"
                            imagen_logo = Image(os.path.realpath(fichero_imagen),width=108,height=34)
                            story.append(imagen_logo)
                            cabecera = estilo['Heading4']
                            cabecera.pageBreakBefore=0
                            cabecera.keepWithNext=0
                            cabecera.backColor=colors.red
                            fecha = datetime.date.today()
                            hoy = fecha.strftime("%d/%m/20%y")
                            titulo = "INFORME DE VENTAS DE PRODUCTOS, FECHA: " + str(hoy)
                            parrafo = Paragraph(titulo ,cabecera)
                            story.append(parrafo)
                            t=Table([["","","",""]],colWidths=120, rowHeights=30)
                            story.append(t)
                            t=Table([['Fecha: ',ant,'','']],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            for row in rows:
                                if row[1]!= ant:
                                    t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    t=Table([['Fecha: ',row[1],'','']],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                                    story.append(t)
                                    tot = tot + sut
                                    suv = 0
                                    sut = 0
                                    ant= row[1]
                                t=Table([['Numero de venta: ',row[0],'','']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                t=Table([['Descripcion','Cantidad','Precio','Subtotal']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),])
                                story.append(t)
                                nve = int(row[0])
                                ssql2 = "SELECT pro_des, ven_can, ven_pre, ven_can * ven_pre AS sub "
                                ssql2+= "FROM ventas INNER JOIN productos ON ven_pro = pro_cod WHERE ven_nve = %d" % nve
                                cursor.execute(ssql2)
                                rows2 = cursor.fetchall()
                                print rows2[0][0]
                                for row2 in rows2:
                                    t=Table([[row2[0],row2[1],row2[2],row2[3]]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    suv = suv + float(row2[3])
                                t=Table([['','','Subtotal:',suv]],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                sut = sut + suv
                                suv = 0
                                tve = tve + 1
                            t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                            story.append(t)
                            tot = tot + sut
                            t=Table([["","","Monto Total:",tot]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Total de Ventas:",tve]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Promedio:",round(tot/tve,2)]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            os.chdir('C:/Users/Lenovo/Desktop/informes')
                            doc=SimpleDocTemplate("ventassaborfeliz.pdf",pagesize=A4)
                            doc.build(story)
                            os.system('ventassaborfeliz.pdf')
                    except MySQLdb.Error:
                           print "Error"
                           sys.exit(1)
                    cursor.close()
                    conn.close()

    def informesrotiseria(self):
        conn = conectar()
        cursor = conn.cursor()
        story=[]
        fechad= self.ui.linefechad.text()
        fechah= self.ui.linefechah.text()
        fec = verificar(fechad, fechah)
        if(fec!=""):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar las fechas:"+fec)
            self.ui.mdiArea.setEnabled(True)
        else:
            fechadlis= fechad.split('/')
            fechahlis= fechah.split('/')
            lon= longitudysolonumeros(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
            if(lon!=""):
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe completar bien: "+lon)
                self.ui.mdiArea.setEnabled(True)
            else:
                erf= errorfecha(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
                if(erf!=""):
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message=erf)
                    self.ui.mdiArea.setEnabled(True)
                else:
                    lafechad= '-'.join([str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0])])
                    lafechah= '-'.join([str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0])])
                    try:
                        ssql = "SELECT rot_nro, rot_des, rot_pto, DATE_FORMAT(rot_fec,'%d/%m/20%y')as fec FROM rotiseria "
                        ssql+= "WHERE rot_fec >= '" + lafechad + "' AND rot_fec <= '" + lafechah + "' ORDER BY rot_fec, rot_nro"
                        cursor.execute(ssql)
                        rows = cursor.fetchall()
                        print rows
                        if len(rows)== 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="No se encontro ninguna venta.")
                            self.ui.mdiArea.setEnabled(True)
                        else:
                            tot = 0
                            sut = 0
                            suv = 0
                            tse= 0
                            ant = rows[0][3]
                            estilo = getSampleStyleSheet()
                            story = []
                            fichero_imagen = "logoinf.png"
                            imagen_logo = Image(os.path.realpath(fichero_imagen),width=108,height=34)
                            story.append(imagen_logo)
                            cabecera = estilo['Heading4']
                            cabecera.pageBreakBefore=0
                            cabecera.keepWithNext=0
                            cabecera.backColor=colors.red
                            fecha = datetime.date.today()
                            hoy = fecha.strftime("%d/%m/20%y")
                            titulo = "INFORME DE VENTAS DE ROTISERIA, FECHA: " + str(hoy)
                            parrafo = Paragraph(titulo ,cabecera)
                            story.append(parrafo)
                            t=Table([["","","",""]],colWidths=120, rowHeights=30)
                            story.append(t)
                            t=Table([['Fecha: ',ant,'']],colWidths=170, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([['Numero de Venta','Descripcion','Subtotal']],colWidths=170, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                            story.append(t)
                            for row in rows:
                                if row[3]!= ant:
                                    t=Table([['','Subtotal: ',sut]],colWidths=170, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    t=Table([['Fecha: ',row[3],'']],colWidths=170, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                                    story.append(t)
                                    t=Table([['Numero de Venta','Descripcion','Subtotal']],colWidths=170, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    tot = tot + sut
                                    sut = 0
                                    ant= row[3]
                                t=Table([[row[0],row[1],row[2]]],colWidths=170, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),])
                                story.append(t)
                                sut = sut + float(row[2])
                                tse = tse + 1
                            tot = tot + sut
                            t=Table([["","Monto Total:",tot]],colWidths=170, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            t=Table([["","Total de Servicio:",tse]],colWidths=170, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            t=Table([["","Promedio:",round(tot/tse,2)]],colWidths=170, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            os.chdir('C:/Users/Lenovo/Desktop/informes')
                            doc=SimpleDocTemplate("rotiseriasaborfeliz.pdf",pagesize=A4)
                            doc.build(story)
                            os.system('rotiseriasaborfeliz.pdf')
                    except MySQLdb.Error:
                           print "Error"
                           sys.exit(1)
                    cursor.close()
                    conn.close()

    def informecomprasinsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        #story=[]
        fechad= self.ui.linefechad.text()
        fechah= self.ui.linefechah.text()
        fec = verificar(fechad, fechah)
        if(fec!=""):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar las fechas:"+fec)
            self.ui.mdiArea.setEnabled(True)
        else:
            fechadlis= fechad.split('/')
            fechahlis= fechah.split('/')
            lon= longitudysolonumeros(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
            if(lon!=""):
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe completar bien: "+lon)
                self.ui.mdiArea.setEnabled(True)
            else:
                erf= errorfecha(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
                if(erf!=""):
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message=erf)
                    self.ui.mdiArea.setEnabled(True)
                else:
                    lafechad= '-'.join([str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0])])
                    lafechah= '-'.join([str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0])])
                    try:
                        ssql = "SELECT cic_nro, DATE_FORMAT(cic_fec,'%d/%m/20%y')as fec FROM cominscab "
                        ssql+= "WHERE cic_fec >= '" + lafechad + "' AND cic_fec <= '" + lafechah + "' ORDER BY cic_fec, cic_nro"
                        cursor.execute(ssql)
                        rows = cursor.fetchall()
                        print rows
                        if len(rows)== 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="No se encontro ninguna compra de insumos.")
                            self.ui.mdiArea.setEnabled(True)
                        else:
                            tot = 0
                            sut = 0
                            suc = 0
                            tco = 0
                            ant = rows[0][1]
                            ant2 = rows[0][0]
                            estilo = getSampleStyleSheet()
                            story = []
                            fichero_imagen = "logoinf.png"
                            imagen_logo = Image(os.path.realpath(fichero_imagen),width=108,height=34)
                            story.append(imagen_logo)
                            cabecera = estilo['Heading4']
                            cabecera.pageBreakBefore=0
                            cabecera.keepWithNext=0
                            cabecera.backColor=colors.red
                            fecha = datetime.date.today()
                            hoy = fecha.strftime("%d/%m/20%y")
                            titulo = "INFORME DE COMPRAS DE INSUMOS, FECHA: " + str(hoy)
                            parrafo = Paragraph(titulo ,cabecera)
                            story.append(parrafo)
                            t=Table([["","","",""]],colWidths=120, rowHeights=30)
                            story.append(t)
                            t=Table([['Fecha: ',ant,'','']],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            for row in rows:
                                if row[1]!= ant:
                                    t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    t=Table([['Fecha: ',row[1],'','']],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                                    story.append(t)
                                    tot = tot + sut
                                    suc = 0
                                    sut = 0
                                    ant= row[1]
                                t=Table([['Nro de compra: ',row[0],'','']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                t=Table([['Descripcion','Cantidad','Precio','Subtotal']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                nco = int(row[0])
                                ssql2 = "SELECT ins_des, cid_can, cid_pre, cid_can * cid_pre AS sub "
                                ssql2+= "FROM cominsdet INNER JOIN insumos ON cid_ins = ins_cod WHERE cid_nco = %d" % nco
                                cursor.execute(ssql2)
                                rows2 = cursor.fetchall()
                                print rows2[0][0]
                                for row2 in rows2:
                                    t=Table([[row2[0],row2[1],row2[2],row2[3]]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),])
                                    story.append(t)
                                    suc = suc + float(row2[3])
                                t=Table([['','','Subtotal:',suc]],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                sut = sut + suc
                                suc = 0
                                tco = tco + 1
                            t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                            story.append(t)
                            tot = tot + sut
                            t=Table([["","","Monto Total:",tot]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Total de Compras:",tco]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Promedio:",round(tot/tco,2)]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            os.chdir('C:/Users/Lenovo/Desktop/informes')
                            doc=SimpleDocTemplate("comprasinsumossaborfeliz.pdf",pagesize=A4)
                            doc.build(story)
                            os.system('comprasinsumossaborfeliz.pdf')
                    except MySQLdb.Error:
                           print "Error"
                           sys.exit(1)
                    cursor.close()
                    conn.close()

    def informegastosinsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        story=[]
        fechad= self.ui.linefechad.text()
        fechah= self.ui.linefechah.text()
        fec = verificar(fechad, fechah)
        if(fec!=""):
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Debe ingresar las fechas:"+fec)
            self.ui.mdiArea.setEnabled(True)
        else:
            fechadlis= fechad.split('/')
            fechahlis= fechah.split('/')
            lon= longitudysolonumeros(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
            if(lon!=""):
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe completar bien: "+lon)
                self.ui.mdiArea.setEnabled(True)
            else:
                erf= errorfecha(str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0]),str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0]))
                if(erf!=""):
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message=erf)
                    self.ui.mdiArea.setEnabled(True)
                else:
                    lafechad= '-'.join([str(fechadlis[2]), str(fechadlis[1]),str(fechadlis[0])])
                    lafechah= '-'.join([str(fechahlis[2]), str(fechahlis[1]),str(fechahlis[0])])
                    try:
                        ssql = "SELECT gic_nro, DATE_FORMAT(gic_fec,'%d/%m/20%y')as fec FROM gasinscab "
                        ssql+= "WHERE gic_fec >= '" + lafechad + "' AND gic_fec <= '" + lafechah + "' ORDER BY gic_fec, gic_nro"
                        cursor.execute(ssql)
                        rows = cursor.fetchall()
                        print rows
                        if len(rows)== 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun gasto de insumos.")
                            self.ui.mdiArea.setEnabled(True)
                        else:
                            tot = 0
                            sut = 0
                            suv = 0
                            tve = 0
                            ant = rows[0][1]
                            ant2 = rows[0][0]
                            estilo = getSampleStyleSheet()
                            story = []
                            fichero_imagen = "logoinf.png"
                            imagen_logo = Image(os.path.realpath(fichero_imagen),width=108,height=34)
                            story.append(imagen_logo)
                            cabecera = estilo['Heading4']
                            cabecera.pageBreakBefore=0
                            cabecera.keepWithNext=0
                            cabecera.backColor=colors.red
                            fecha = datetime.date.today()
                            hoy = fecha.strftime("%d/%m/20%y")
                            titulo = "INFORME DE GASTOS DE INSUMOS, FECHA: " + str(hoy)
                            parrafo = Paragraph(titulo ,cabecera)
                            story.append(parrafo)
                            t=Table([["","","",""]],colWidths=120, rowHeights=30)
                            story.append(t)
                            t=Table([['Fecha: ',ant,'','']],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            for row in rows:
                                if row[1]!= ant:
                                    t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    t=Table([['Fecha: ',row[1],'','']],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                                    story.append(t)
                                    tot = tot + sut
                                    suv = 0
                                    sut = 0
                                    ant= row[1]
                                t=Table([['Numero de gasto: ',row[0],'','']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                t=Table([['Descripcion','Cantidad','Precio','Subtotal']],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),])
                                story.append(t)
                                nve = int(row[0])
                                ssql2 = "SELECT ins_des, gid_can, gid_pre, gid_can * gid_pre AS sub "
                                ssql2+= "FROM gasinsdet INNER JOIN insumos ON gid_ins = ins_cod WHERE gid_nga = %d" % nve
                                cursor.execute(ssql2)
                                rows2 = cursor.fetchall()
                                print rows2[0][0]
                                for row2 in rows2:
                                    t=Table([[row2[0],row2[1],row2[2],row2[3]]],colWidths=120, rowHeights=30)
                                    t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                    story.append(t)
                                    suv = suv + float(row2[3])
                                t=Table([['','','Subtotal:',suv]],colWidths=120, rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                                story.append(t)
                                sut = sut + suv
                                suv = 0
                                tve = tve + 1
                            t=Table([["","","Subtotal:",sut]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.red)])
                            story.append(t)
                            tot = tot + sut
                            t=Table([["","","Monto Total:",tot]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Total de Ventas:",tve]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('BACKGROUND', (0, 0), (-1, 0), colors.yellow)])
                            story.append(t)
                            t=Table([["","","Promedio:",round(tot/tve,2)]],colWidths=120, rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND', (0, 0), (-1, -0), colors.yellow)])
                            story.append(t)
                            os.chdir('C:/Users/Lenovo/Desktop/informes')
                            doc=SimpleDocTemplate("gastosinsumossaborfeliz.pdf",pagesize=A4)
                            doc.build(story)
                            os.system('gastosinsumossaborfeliz.pdf')
                    except MySQLdb.Error:
                           print "Error"
                           sys.exit(1)
                    cursor.close()
                    conn.close()

    def sumaritemcp2(self):
        conn = conectar()
        cursor = conn.cursor()
        cco = ''
        cca = ''
        pto = 0
        aux = self.ui.linecodigocp2.text()
        if not re.match("^[0-9]{13}$", aux):
            cco = 'codigo'
        aux = self.ui.linecantidadcp2.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            cca = 'cantidad'
        if cco != '' or cca != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + cco + ',' + cca)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocp2.setFocus()
        else:
            cod = int(self.ui.linecodigocp2.text())
            can = float(self.ui.linecantidadcp2.text())
            try:
                cursor.execute("Select *from productos where pro_cod = %d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun producto.")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigocp2.setFocus()
                else:
                    m = 'n'
                    for x in range(len(listacom)):
                        if cod == int(listacom[x][0]):
                            m = 's'
                            break
                    if m == 's':
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="El producto ya fue ingresado.")
                        self.ui.mdiArea.setEnabled(True)
                        row = self.ui.listwidgetcp2.currentRow()
                        self.ui.lineitemcp2.setText(str(listacom[row][6]))
                        self.ui.linecodigocp2.setFocus()
                    else :
                        pre = float(row[2])
                        sto = float(row[3])
                        rep = float(row[4])
                        sut = can * pre
                        itl = str(row[1]) + " - " + str(sut)
                        self.ui.listwidgetcp2.addItem(itl)
                        item = "Codigo = " + str(cod) + ", Cantidad = " + str(can)+ ", Precio = " +  str(pre)
                        item += ", Stock = " + str(row[3]) + ", Reposicion = " + str(row[4])
                        listacom.append([])
                        row2 = len(listacom)
                        listacom[row2 - 1].append(cod)
                        listacom[row2 - 1].append(row[1])
                        listacom[row2 - 1].append(can)
                        listacom[row2 - 1].append(sut)
                        listacom[row2 - 1].append(sto)
                        listacom[row2 - 1].append(rep)
                        listacom[row2 - 1].append(item)
                        listacom[row2 - 1].append(pre)
                        print lista
                        for x in range(len(listacom)):
                            pto = pto + float(listacom[x][3])
                            print pto
                        self.ui.linepretotcp2.setText(str(pto))
                        self.ui.linecodigocp2.setText('')
                        self.ui.linecantidadcp2.setText('1')
                        self.ui.linecodigocp2.setFocus()
                        #row2 = self.ui.listwidgetcp2.currentRow()
                        self.ui.lineitemcp2.setText(str(listacom[row2 - 1][6]))
                        self.ui.linecodigocp2.setFocus()
            except MySQLdb.Error:
               sys.exit(1)
            cursor.close()
            conn.close()

    def borraritemcp2(self):
        if len(listacom) == 0 and self.ui.listwidgetcp2.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar")
            self.ui.mdiArea.setEnabled(True)
        else:
            pto = 0
            row = self.ui.listwidgetcp2.currentRow()
            self.ui.listwidgetcp2.takeItem(row)
            for x in range(len(listacom)):
                if x == row:
                    listacom.pop(x)
                    break
            for x in range(len(listacom)):
                pto = pto + float(listacom[x][3])
            if pto == 0:
                self.ui.linepretotcp2.setText('')
            else:
                self.ui.linepretotcp2.setText(str(pto))
            row = self.ui.listwidgetcp2.currentRow()
            self.ui.lineitemcp2.setText(str(listacom[row][6]))

    def borrartodocp2(self):
        if len(listacom) == 0 and self.ui.listwidgetcp2.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar.")
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocp2.setFocus()
        else:
            self.ui.listwidgetcp2.clear()
            listacom[:] = []
            self.ui.linepretotcp2.setText('')
            self.ui.lineitemcp2.setText('')
            self.ui.linecodigocp2.setFocus()

    def fechahoycp2(self):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%yy")
        self.ui.linefechacp2.setText(str(hoy))

    def veritemcp2(self):
        row = self.ui.listwidgetcp2.currentRow()
        self.ui.lineitemcp2.setText(str(listacom[row][6]))

    def compraproductosv2(self):
        conn = conectar()
        cursor = conn.cursor()
        fecha = self.ui.linefechacp2.text()
        fechalis = fecha.split('/')
        inf = ""
        mpr = ""
        mco = ""
        coc = self.ui.linecodigocp2.text()
        if coc != '':
            mco = "Codigo"
        if len(listacom) == 0:
            mpr = "Lista"
        afe= longitudysolonumeroscv(str(fechalis[2]), str(fechalis[1]),str(fechalis[0]),str(fecha))
        if mco != '' or afe != '' or mpr !='':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar o ingresar en la lista: " + afe + ', '+ mpr + ', ' + mco)
            self.ui.mdiArea.setEnabled(True)
        else:
            try:
                lafecha= '-'.join([str(fechalis[2]), str(fechalis[1]),str(fechalis[0])])
                cursor.execute("SELECT * FROM comcab ORDER BY coc_nro DESC LIMIT 1")
                row = cursor.fetchone()
                if row is None:
                    nc = 1
                else:
                    nc = row[0] + 1
                cursor.execute("INSERT INTO comcab(coc_nro, coc_fec) VALUES(%d, '%s')" %(nc, lafecha))
                inf = "Nro de compra = " + str(nc) + "\n"
                for x in range (len(listacom)):
                    cod = int(listacom[x][0])
                    des = listacom[x][1]
                    can = float(listacom[x][2])
                    sut = float(listacom[x][3])
                    sto = float(listacom[x][4])
                    rep = float(listacom[x][5])
                    pre = float(listacom[x][7])
                    can_act = sto + can
                    cursor.execute("UPDATE productos SET pro_can = %d WHERE pro_cod = %d" % (can_act, cod))
                    cursor.execute("""
                    INSERT INTO compras(com_nco, com_pro, com_can, com_pre)
                    VALUES(%d, %d, %d, %d)
                    """ %(nc, cod, can, pre))
                    inf+= "Descripcion = " + str(des) + ", Stock = " + str(can_act)
                    inf+= ", Reposicion = " + str(rep) + "\n"
                conn.commit()
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Las compra se ingreso correctamente.\n\n" + inf)
                self.ui.mdiArea.setEnabled(True)
                self.ui.listwidgetcp2.clear()
                listacom[:] = []
                self.ui.linepretotcp2.setText('')
                self.ui.linefechacp2.setText('')
                self.ui.linecodigocp2.setText('')
                self.ui.linecantidadcp2.setText('1')
                self.ui.lineitemcp2.setText('')
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
            cursor.close()
            conn.close()

    def comprainsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        fecha = self.ui.linefechacomins.text()
        fechalis = fecha.split('/')
        inf = ""
        mpr = ""
        mco = ""
        coc = self.ui.linecodigocomins.text()
        if coc != '':
            mco = "Codigo"
        if len(listacomins) == 0:
            mpr = "Lista"
        afe= longitudysolonumeroscv(str(fechalis[2]), str(fechalis[1]),str(fechalis[0]),str(fecha))
        if mco != '' or afe != '' or mpr !='':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar o ingresar en la lista: " + afe + ', '+ mpr + ', ' + mco)
            self.ui.mdiArea.setEnabled(True)
        else:
            try:
                lafecha= '-'.join([str(fechalis[2]), str(fechalis[1]),str(fechalis[0])])
                cursor.execute("SELECT * FROM cominscab ORDER BY cic_nro DESC LIMIT 1")
                row = cursor.fetchone()
                if row is None:
                    nc = 1
                else:
                    nc = row[0] + 1
                cursor.execute("INSERT INTO cominscab(cic_nro, cic_fec) VALUES(%d, '%s')" %(nc, lafecha))
                inf = "Nro de compra = " + str(nc) + "\n"
                for x in range (len(listacomins)):
                    cod = int(listacomins[x][0])
                    des = listacomins[x][1]
                    can = float(listacomins[x][2])
                    sut = float(listacomins[x][3])
                    sto = float(listacomins[x][4])
                    rep = float(listacomins[x][5])
                    pre = float(listacomins[x][7])
                    can_act = sto + can
                    cursor.execute("UPDATE insumos SET ins_can = %d WHERE ins_cod = %d" % (can_act, cod))
                    cursor.execute("""
                    INSERT INTO cominsdet(cid_nco, cid_ins, cid_can, cid_pre)
                    VALUES(%d, %d, %d, %d)
                    """ %(nc, cod, can, pre))
                    inf+= "Descripcion = " + str(des) + ", Stock = " + str(can_act)
                    inf+= ", Reposicion = " + str(rep) + "\n"
                conn.commit()
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Las compra se ingreso correctamente.\n\n" + inf)
                self.ui.mdiArea.setEnabled(True)
                self.ui.listwidgetcomins.clear()
                listacomins[:] = []
                self.ui.linepretotcomins.setText('')
                self.ui.linefechacomins.setText('')
                self.ui.linecodigocomins.setText('')
                self.ui.linecantidadcomins.setText('1')
                self.ui.lineitemcomins.setText('')
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
            cursor.close()
            conn.close()

    def sumaritemcomins(self):
        conn = conectar()
        cursor = conn.cursor()
        cco = ''
        cca = ''
        pto = 0
        aux = self.ui.linecodigocomins.text()
        if not re.match("^[0-9]{13}$", aux):
            cco = 'codigo'
        aux = self.ui.linecantidadcomins.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            cca = 'cantidad'
        if cco != '' or cca != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + cco + ',' + cca)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocp2.setFocus()
        else:
            cod = int(self.ui.linecodigocomins.text())
            can = float(self.ui.linecantidadcomins.text())
            try:
                cursor.execute("Select *from insumos where ins_cod = %d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun insumo.")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigocomins.setFocus()
                else:
                    m = 'n'
                    for x in range(len(listacomins)):
                        if cod == int(listacomins[x][0]):
                            m = 's'
                            break
                    if m == 's':
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="El insumo ya fue ingresado.")
                        self.ui.mdiArea.setEnabled(True)
                        row = self.ui.listwidgetcomins.currentRow()
                        self.ui.lineitemcomins.setText(str(listacom[row][6]))
                        self.ui.linecodigocomins.setFocus()
                    else :
                        pre = float(row[2])
                        sto = float(row[3])
                        rep = float(row[4])
                        sut = can * pre
                        itl = str(row[1]) + " - " + str(sut)
                        self.ui.listwidgetcomins.addItem(itl)
                        item = "Codigo = " + str(cod) + ", Cantidad = " + str(can)+ ", Precio = " +  str(pre)
                        item += ", Stock = " + str(row[3]) + ", Reposicion = " + str(row[4])
                        listacomins.append([])
                        row2 = len(listacomins)
                        listacomins[row2 - 1].append(cod)
                        listacomins[row2 - 1].append(row[1])
                        listacomins[row2 - 1].append(can)
                        listacomins[row2 - 1].append(sut)
                        listacomins[row2 - 1].append(sto)
                        listacomins[row2 - 1].append(rep)
                        listacomins[row2 - 1].append(item)
                        listacomins[row2 - 1].append(pre)
                        print lista
                        for x in range(len(listacomins)):
                            pto = pto + float(listacomins[x][3])
                            print pto
                        self.ui.linepretotcomins.setText(str(pto))
                        self.ui.linecodigocomins.setText('')
                        self.ui.linecantidadcomins.setText('1')
                        self.ui.linecodigocomins.setFocus()
                        #row2 = self.ui.listwidgetcp2.currentRow()
                        self.ui.lineitemcomins.setText(str(listacomins[row2 - 1][6]))
                        self.ui.linecodigocomins.setFocus()
            except MySQLdb.Error:
               sys.exit(1)
            cursor.close()
            conn.close()

    def borraritemcomins(self):
        if len(listacomins) == 0 and self.ui.listwidgetcomins.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar")
            self.ui.mdiArea.setEnabled(True)
        else:
            pto = 0
            row = self.ui.listwidgetcomins.currentRow()
            self.ui.listwidgetcomins.takeItem(row)
            for x in range(len(listacomins)):
                if x == row:
                    listacomins.pop(x)
                    break
            for x in range(len(listacomins)):
                pto = pto + float(listacomins[x][3])
            if pto == 0:
                self.ui.linepretotcomins.setText('')
            else:
                self.ui.linepretotcomins.setText(str(pto))
            #row = self.ui.listwidgetcomins.currentRow()
            self.ui.lineitemcomins.setText('')
            self.ui.linecodigocomins.setFocus()

    def borrartodocomins(self):
        if len(listacomins) == 0 and self.ui.listwidgetcomins.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar.")
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigocomins.setFocus()
        else:
            self.ui.listwidgetcomins.clear()
            listacomins[:] = []
            self.ui.linepretotcomins.setText('')
            self.ui.lineitemcomins.setText('')
            self.ui.linecodigocomins.setFocus()

    def veritemcomins(self):
        row = self.ui.listwidgetcomins.currentRow()
        self.ui.lineitemcomins.setText(str(listacomins[row][6]))

    def fechahoycomins(self):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%yy")
        self.ui.linefechacomins.setText(str(hoy))

    def limpiarlistacomins(self):
        self.ui.listwidgetcomins.clear()
        listacomins[:] = []
        self.ui.linepretotcomins.setText('')
        self.ui.lineitemcomins.setText('')

    def sumaritemvp2(self):
        conn = conectar()
        cursor = conn.cursor()
        vco = ''
        vca = ''
        pto = 0
        aux = self.ui.linecodigovp2.text()
        if not re.match("^[0-9]{13}$", aux):
            vco = 'codigo'
        aux = self.ui.linecantidadvp2.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            vca = 'cantidad'
        if vco != '' or vca != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + vco + ',' + vca)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigovp2.setFocus()
        else:
            cod = int(self.ui.linecodigovp2.text())
            can = float(self.ui.linecantidadvp2.text())
            try:
                cursor.execute("Select *from productos where pro_cod = %d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun producto.")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigovp2.setFocus()
                else:
                    m = 'n'
                    for x in range(len(lista)):
                        if cod == int(lista[x][0]):
                            m = 's'
                            break
                    if m == 's':
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="El producto ya fue ingresado.")
                        self.ui.mdiArea.setEnabled(True)
                        row = self.ui.listwidgetvp2.currentRow()
                        self.ui.lineitemvp2.setText(str(lista[row][6]))
                        self.ui.linecodigovp2.setFocus()
                    else:
                        if row[3] == 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="Stock vacio. No se puede vender el producto.")
                            self.ui.mdiArea.setEnabled(True)
                            self.ui.linecodigovp2.setFocus()
                        else:
                            if can > row[3]:
                                self.ui.mdiArea.setEnabled(False)
                                window = Tk()
                                window.wm_withdraw()
                                tkMessageBox.showinfo(title="Mensaje",message="Cantidad a vender es mayor que el stock.")
                                self.ui.mdiArea.setEnabled(True)
                                self.ui.linecodigovp2.setFocus()
                            else :
                                pre = float(row[2])
                                sto = float(row[3])
                                rep = float(row[4])
                                sut = can * pre
                                itl = str(row[1]) + " - " + str(sut)
                                self.ui.listwidgetvp2.addItem(itl)
                                item = "Codigo = " + str(cod) + ", Cantidad = " + str(can)+ ", Precio = " +  str(pre)
                                item += ", Stock = " + str(row[3]) + ", Reposicion = " + str(row[4])
                                lista.append([])
                                row2 = len(lista)
                                lista[row2 - 1].append(cod)
                                lista[row2 - 1].append(row[1])
                                lista[row2 - 1].append(can)
                                lista[row2 - 1].append(sut)
                                lista[row2 - 1].append(sto)
                                lista[row2 - 1].append(rep)
                                lista[row2 - 1].append(item)
                                lista[row2 - 1].append(pre)
                                for x in range(len(lista)):
                                    pto = pto + float(lista[x][3])
                                    print pto
                                self.ui.linepretotvp2.setText(str(pto))
                                self.ui.linecodigovp2.setText('')
                                self.ui.linecantidadvp2.setText('1')
                                self.ui.linecodigovp2.setFocus()
                                #row2 = self.ui.listwidgetvp2.currentRow()
                                self.ui.lineitemvp2.setText(str(lista[row2 - 1][6]))
            except MySQLdb.Error:
               sys.exit(1)
            cursor.close()
            conn.close()

    def borraritemvp2(self):
        if len(lista) == 0 and self.ui.listwidgetvp2.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar")
            self.ui.mdiArea.setEnabled(True)
        else:
            pto = 0
            row = self.ui.listwidgetvp2.currentRow()
            self.ui.listwidgetvp2.takeItem(row)
            for x in range(len(lista)):
                if x == row:
                    lista.pop(x)
                    break
            for x in range(len(lista)):
                pto = pto + float(lista[x][3])
            if pto == 0:
                self.ui.linepretotvp2.setText('')
            else:
                self.ui.linepretotvp2.setText(str(pto))
            self.ui.linepretotvp2.setText(str(pto))
            row = self.ui.listwidgetvp2.currentRow()
            self.ui.lineitemvp2.setText(str(lista[row][6]))

    def borrartodovp2(self):
        if len(lista) == 0 and self.ui.listwidgetvp2.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar.")
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigovp2.setFocus()
        else:
            self.ui.listwidgetvp2.clear()
            lista[:] = []
            self.ui.linepretotvp2.setText('')
            self.ui.lineitemvp2.setText('')
            self.ui.linecodigovp2.setFocus()

    def ventasproductosv2(self):
        conn = conectar()
        cursor = conn.cursor()
        fecha = self.ui.linefechavp2.text()
        fechalis = fecha.split('/')
        inf = ""
        mco = ""
        mpr = ""
        cov = self.ui.linecodigovp2.text()
        if cov != '':
            mco = "Codigo"
        if len(lista) == 0:
            mpr = "Lista"
        afe= longitudysolonumeroscv(str(fechalis[2]), str(fechalis[1]),str(fechalis[0]),str(fecha))
        if afe != '' or mco != '' or mpr != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar o ingresar en la lista: " + afe + ', ' + mco + ', ' + mpr)
            self.ui.mdiArea.setEnabled(True)
        else:
            try:
                lafecha= '-'.join([str(fechalis[2]), str(fechalis[1]),str(fechalis[0])])
                cursor.execute("SELECT * FROM vencab ORDER BY vec_nro DESC LIMIT 1")
                row = cursor.fetchone()
                if row is None:
                    nv = 1
                else:
                    nv = row[0] + 1
                cursor.execute("INSERT INTO vencab(vec_nro, vec_fec) VALUES(%d, '%s')" %(nv, lafecha))
                inf+= "Nro de venta = " + str(nv) + "\n"
                for x in range (len(lista)):
                    cod = int(lista[x][0])
                    des = lista[x][1]
                    can = float(lista[x][2])
                    sut = float(lista[x][3])
                    sto = float(lista[x][4])
                    rep = float(lista[x][5])
                    pre = float(lista[x][7])
                    can_act = sto - can
                    cursor.execute("UPDATE productos SET pro_can = %d WHERE pro_cod = %d" % (can_act, cod))
                    cursor.execute("""
                    INSERT INTO ventas(ven_nve, ven_pro, ven_can, ven_pre)
                    VALUES(%d, %d, %d, %d)
                    """ %(nv, cod, can, pre))
                    inf+= "Descripcion = " + str(des) + ", Stock = " + str(can_act)
                    inf+= ", Reposicion = " + str(rep) + "\n"
                conn.commit()
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Las venta se ingreso correctamente.\n\n" + inf)
                self.ui.mdiArea.setEnabled(True)
                self.ui.listwidgetvp2.clear()
                lista[:] = []
                self.ui.linepretotvp2.setText('')
                self.ui.linefechavp2.setText('')
                self.ui.linecodigovp2.setText('')
                self.ui.linecantidadvp2.setText('1')
                self.ui.lineitemvp2.setText('')
                self.ui.linecodigovp2.setFocus()
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
            cursor.close()
            conn.close()

    def fechahoyvp2(self):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%yy")
        self.ui.linefechavp2.setText(str(hoy))

    def veritemvp2(self):
        row = self.ui.listwidgetvp2.currentRow()
        self.ui.lineitemvp2.setText(str(lista[row][6]))

    def sumaritem(self):
        apr = ''
        aca = ''
        pto = 0
        aux = self.ui.linepreciovr.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            apr = 'precio'
        aux = self.ui.linecantidadvr.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad'
        if apr != '' or aca != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + apr + ',' + aca)
            self.ui.linepreciovr.setFocus()
            self.ui.mdiArea.setEnabled(True)
        else:
            pre = float(self.ui.linepreciovr.text())
            can = float(self.ui.linecantidadvr.text())
            sut =  pre * can
            self.ui.listwidgetvr.addItem(str(sut))
            item = "Precio = " + str(pre) + ", Cantidad = " + str(can)
            listarot.append([])
            row = len(listarot)
            listarot[row - 1].append(item)
            listarot[row - 1].append(sut)
            for x in range(0,len(listarot)):
                pto = pto + float(listarot[x][1])
            self.ui.linepretotvr.setText(str(pto))
            self.ui.linepretotingvr.setText(str(pto))
            self.ui.linepreciovr.setText('')
            self.ui.linecantidadvr.setText('1')
            self.ui.linepreciovr.setFocus()
            self.ui.lineitemvr.setText(str(listarot[row - 1][0]))

    def borraritem(self):
        if len(listarot)== 0 and self.ui.listwidgetvr.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elemento para borrar")
            self.ui.mdiArea.setEnabled(True)
        else:
            pto = 0
            row = self.ui.listwidgetvr.currentRow()
            self.ui.listwidgetvr.takeItem(row)
            for x in range(len(listarot)):
                if x == row:
                    listarot.pop(x)
                    break
            for x in range(len(listarot)):
                pto = pto + float(listarot[x][1])
            if pto == 0:
                self.ui.linepretotvr.setText('')
                self.ui.linepretoting.setText('')
            else:
                self.ui.linepretotvr.setText(str(pto))
                self.ui.linepretotingvr.setText(str(pto))
            self.ui.linepretotvr.setText(str(pto))
            row = self.ui.listwidgetvr.currentRow()
            self.ui.lineitemvr.setText(str(listarot[row][0]))

    def veritem(self):
        row = self.ui.listwidgetvr.currentRow()
        self.ui.lineitemvr.setText(str(listarot[row][0]))

    def borrartodo(self):
        if len(listarot) == 0 and self.ui.listwidgetvr.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar")
            self.ui.mdiArea.setEnabled(True)
            self.ui.linepreciovr.setFocus()
        else:
            self.ui.listwidgetvr.clear()
            listarot[:] = []
            self.ui.linepretotvr.setText('')
            self.ui.linepretotingvr.setText('')
            self.ui.lineitemvr.setText('')
            self.ui.linepreciovr.setFocus()

    def fechahoy(self):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%yy")
        self.ui.linefechavr.setText(str(hoy))

    def ventasrotiseria(self):
        conn = conectar()
        cursor = conn.cursor()
        vrd = ''
        vrp = ''
        mpr = ''
        aud = self.ui.linedescripcionvr.text()
        if aud == '':
            vrd = 'descripcion'
        aux = self.ui.linepretotingvr.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            vrp = "Precio"
        pre = self.ui.linepreciovr.text()
        if pre != '':
            mpr = "Precio"
        fecha= self.ui.linefechavr.text()
        fechalis= fecha.split('/')
        vrf= longitudysolonumeroscv(str(fechalis[2]), str(fechalis[1]),str(fechalis[0]),str(fecha))
        if vrd != '' or vrp!= '' or vrf != '' or mpr != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar los campos: " + vrd + ', ' + vrp + ', ' + vrf + ', ' + mpr)
            self.ui.mdiArea.setEnabled(True)
        else:
            try:
                des = self.ui.linedescripcionvr.text()
                pre = float(self.ui.linepretotingvr.text())
                lafecha= '-'.join([str(fechalis[2]), str(fechalis[1]),str(fechalis[0])])
                cursor.execute("SELECT * FROM rotiseria ORDER BY rot_nro DESC LIMIT 1")
                row = cursor.fetchone()
                if row is None:
                    nvr = 1
                else:
                    nvr = row[0] + 1
                    cursor.execute("""
                    Insert into rotiseria(rot_nro, rot_des, rot_pto, rot_fec)
                    values(%d, '%s', %d, '%s')
                    """ %(nvr, des, pre, lafecha))
                    conn.commit()
                    inf = "\n Nro de venta = " + str(nvr)
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="La venta ingreso correctamente" + inf)
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linedescripcionvr.setText('')
                    self.ui.linefechavr.setText('')
                    self.ui.linepretotingvr.setText('')
                    self.ui.lineitemvr.setText('')
                    self.ui.linepreciovr.setText('')
                    self.ui.linecantidad.setText('1')
                    self.ui.listwidgetvr.clear()
                    listarot[:] = []
                    self.ui.linepretotvr.setText('')
                    self.ui.linedescripcionvr.setFocus()
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
            cursor.close()
            conn.close()

    def sumaritemgasins(self):
        conn = conectar()
        cursor = conn.cursor()
        vco = ''
        vca = ''
        pto = 0
        aux = self.ui.linecodigogasins.text()
        if not re.match("^[0-9]{13}$", aux):
            vco = 'codigo'
        aux = self.ui.linecantidadgasins.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            vca = 'cantidad'
        if vco != '' or vca != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + vco + ',' + vca)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigogasins.setFocus()
        else:
            cod = int(self.ui.linecodigogasins.text())
            can = float(self.ui.linecantidadgasins.text())
            try:
                cursor.execute("Select *from insumos where ins_cod = %d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se ha encontrado ningun insumo.")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigogasins.setFocus()
                else:
                    m = 'n'
                    for x in range(len(listagasins)):
                        if cod == int(listagasins[x][0]):
                            m = 's'
                            break
                    if m == 's':
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="El insumo ya fue ingresado.")
                        self.ui.mdiArea.setEnabled(True)
                        row = self.ui.listwidgetgasins.currentRow()
                        self.ui.lineitemgasins.setText(str(listagasins[row][6]))
                        self.ui.linecodigogasins.setFocus()
                    else:
                        if row[3] == 0:
                            self.ui.mdiArea.setEnabled(False)
                            window = Tk()
                            window.wm_withdraw()
                            tkMessageBox.showinfo(title="Mensaje",message="Stock vacio. No se puede ocupar el insumo.")
                            self.ui.mdiArea.setEnabled(True)
                            self.ui.linecodigogasins.setFocus()
                        else:
                            if can > row[3]:
                                self.ui.mdiArea.setEnabled(False)
                                window = Tk()
                                window.wm_withdraw()
                                tkMessageBox.showinfo(title="Mensaje",message="Cantidad a usar es mayor que el stock.")
                                self.ui.mdiArea.setEnabled(True)
                                self.ui.linecodigogasins.setFocus()
                            else :
                                pre = float(row[2])
                                sto = float(row[3])
                                rep = float(row[4])
                                sut = can * pre
                                itl = str(row[1]) + " - " + str(sut)
                                self.ui.listwidgetgasins.addItem(itl)
                                item = "Codigo = " + str(cod) + ", Cantidad = " + str(can)+ ", Precio = " +  str(pre)
                                item += ", Stock = " + str(row[3]) + ", Reposicion = " + str(row[4])
                                listagasins.append([])
                                row2 = len(lista)
                                listagasins[row2 - 1].append(cod)
                                listagasins[row2 - 1].append(row[1])
                                listagasins[row2 - 1].append(can)
                                listagasins[row2 - 1].append(sut)
                                listagasins[row2 - 1].append(sto)
                                listagasins[row2 - 1].append(rep)
                                listagasins[row2 - 1].append(item)
                                listagasins[row2 - 1].append(pre)
                                for x in range(len(listagasins)):
                                    pto = pto + float(listagasins[x][3])
                                    print pto
                                self.ui.linepretotgasins.setText(str(pto))
                                self.ui.linecodigogasins.setText('')
                                self.ui.linecantidadgasins.setText('1')
                                self.ui.linecodigogasins.setFocus()
                                #row2 = self.ui.listwidgetvp2.currentRow()
                                self.ui.lineitemgasins.setText(str(listagasins[row2 - 1][6]))
            except MySQLdb.Error:
               sys.exit(1)
            cursor.close()
            conn.close()

    def borraritemgasins(self):
        if len(listagasins) == 0 and self.ui.listwidgetgasins.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar")
            self.ui.mdiArea.setEnabled(True)
        else:
            pto = 0
            row = self.ui.listwidgetgasins.currentRow()
            self.ui.listwidgetgasins.takeItem(row)
            for x in range(len(listagasins)):
                if x == row:
                    listagasins.pop(x)
                    break
            for x in range(len(listagasins)):
                pto = pto + float(listagasins[x][3])
            if pto == 0:
                self.ui.linepretotgasins.setText('')
            else:
                self.ui.linepretotgasins.setText(str(pto))
            self.ui.linepretotgasins.setText(str(pto))
            row = self.ui.listwidgetgasins.currentRow()
            self.ui.lineitemgasins.setText(str(lista[row][6]))

    def borrartodogasins(self):
        if len(listagasins) == 0 and self.ui.listwidgetgasins.count == 0:
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="No existe elementos para borrar.")
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigogasins.setFocus()
        else:
            self.ui.listwidgetgasins.clear()
            listagasins[:] = []
            self.ui.linepretotgasins.setText('')
            self.ui.lineitemgasins.setText('')
            self.ui.linecodigogasins.setFocus()

    def gastoinsumos(self):
        conn = conectar()
        cursor = conn.cursor()
        fecha = self.ui.linefechagasins.text()
        fechalis = fecha.split('/')
        inf = ""
        mco = ""
        mpr = ""
        cov = self.ui.linecodigogasins.text()
        if cov != '':
            mco = "Codigo"
        if len(listagasins) == 0:
            mpr = "Lista"
        afe= longitudysolonumeroscv(str(fechalis[2]), str(fechalis[1]),str(fechalis[0]),str(fecha))
        if afe != '' or mco != '' or mpr != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar o ingresar en la lista: " + afe + ', ' + mco + ', ' + mpr)
            self.ui.mdiArea.setEnabled(True)
        else:
            lafecha= '-'.join([str(fechalis[2]), str(fechalis[1]),str(fechalis[0])])
            try:
                cursor.execute("SELECT * FROM gasinscab ORDER BY gic_nro DESC LIMIT 1")
                row = cursor.fetchone()
                if row is None:
                    ng = 1
                else:
                    ng = row[0] + 1
                cursor.execute("INSERT INTO gasinscab(gic_nro, gic_fec) VALUES(%d, '%s')" %(ng, lafecha))
                inf+= "Nro de gasto = " + str(ng) + "\n"
                for x in range (len(listagasins)):
                    cod = int(listagasins[x][0])
                    des = listagasins[x][1]
                    can = float(listagasins[x][2])
                    sut = float(listagasins[x][3])
                    sto = float(listagasins[x][4])
                    rep = float(listagasins[x][5])
                    pre = float(listagasins[x][7])
                    can_act = sto - can
                    cursor.execute("UPDATE insumos SET ins_can = %d WHERE ins_cod = %d" % (can_act, cod))
                    cursor.execute("""
                    INSERT INTO gasinsdet(gid_nga, gid_ins, gid_can, gid_pre)
                    VALUES(%d, %d, %d, %d)
                    """ %(ng, cod, can, pre))
                    inf+= "Descripcion = " + str(des) + ", Stock = " + str(can_act)
                    inf+= ", Reposicion = " + str(rep) + "\n"
                conn.commit()
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El gasto se ingreso correctamente.\n\n" + inf)
                self.ui.mdiArea.setEnabled(True)
                self.ui.listwidgetgasins.clear()
                listagasins[:] = []
                self.ui.linepretotgasins.setText('')
                self.ui.linefechagasins.setText('')
                self.ui.linecodigogasins.setText('')
                self.ui.linecantidadgasins.setText('1')
                self.ui.lineitemgasins.setText('')
                self.ui.linecodigogasins.setFocus()
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
            cursor.close()
            conn.close()

    def fechahoygasins(self):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%yy")
        self.ui.linefechagasins.setText(str(hoy))

    def veritemgasins(self):
        row = self.ui.listwidgetgasins.currentRow()
        self.ui.lineitemgasins.setText(str(lista[row][6]))

    def limpiarlistagasins(self):
        self.ui.listwidgetgasins.clear()
        listagasins[:] = []
        self.ui.linepretotgasins.setText('')
        self.ui.lineitemgasins.setText('')

    def operacionesmultiplesrot(self):
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesven(self):
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescom(self):
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesalt(self):
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesinf(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescos(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescop(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.linecodigocs.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesmop(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.settext(''); self.ui.linefechah.setText('')
        self.ui.linecodigocs.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesaltins(self):
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescomins(self):
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesgasins(self):
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1')
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText('')
        self.ui.linecantidadvp2.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescosins(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.linecodigomp.setText('')
        self.ui.linenombremp.setText(''); self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText('')
        self.ui.linereposicionmp.setText(''); self.ui.radiomp.setChecked(0)
        self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocs.setText(''); self.ui.linecodigomi.setText(''); self.ui.linenombremi.setText('')
        self.ui.linepreciomi.setText(''); self.ui.linecantidadmi.setText(''); self.ui.linereposicionmi.setText('')
        self.ui.radiomi.setChecked(0); self.ui.linecodigomi.setEnabled(True)
        self.ui.linenombremi.setEnabled(False); self.ui.linepreciomi.setEnabled(False)
        self.ui.linecantidadmi.setEnabled(False); self.ui.linereposicionmi.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplescopins(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.setText(''); self.ui.linefechah.setText('')
        self.ui.linecodigocs.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomp.setText(''); self.ui.linenombremp.setText('')
        self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText(''); self.ui.linereposicionmp.setText('')
        self.ui.radiomp.setChecked(0); self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

    def operacionesmultiplesmopins(self):
        self.ui.linecodigoalt.setText(''); self.ui.linedescripcionalt.setText(''); self.ui.lineprecioalt.setText('')
        self.ui.linecantidadalt.setText(''); self.ui.linereposicionalt.setText('')
        self.ui.listwidgetvp2.clear(); lista[:] = []
        self.ui.linecodigovp2.setText(''); self.ui.linefechavp2.setText(''); self.ui.linecantidadvp2.text()!= '1'
        self.ui.linepretotingvr.setText(''); self.ui.linepretotvr.setText('')
        self.ui.linedescripcionvr.setText(''); self.ui.linefechavr.setText(''); self.ui.linepreciovr.setText('')
        self.ui.linecantidadvr.setText('1')
        self.ui.listwidgetcp2.clear(); listacom[:] = []
        self.ui.linecodigocp2.setText(''); self.ui.linefechacp2.setText('')
        self.ui.linecantidadcp2.setText('1'); self.ui.linefechad.settext(''); self.ui.linefechah.setText('')
        self.ui.linecodigocs.setText('')
        self.ui.listwidgetcomins.clear(); listacomins[:] = []
        self.ui.linecodigocomins.setText(''); self.ui.linefechacomins.setText('')
        self.ui.linecantidadcomins.setText('1')
        self.ui.listwidgetgasins.clear(); listagasins[:] = []
        self.ui.linecodigogasins.setText(''); self.ui.linefechagasins.setText('')
        self.ui.linecantidadgasins.setText('1')
        self.ui.linecodigocsi.setText(''); self.ui.linecodigomp.setText(''); self.ui.linenombremp.setText('')
        self.ui.linepreciomp.setText(''); self.ui.linecantidadmp.setText(''); self.ui.linereposicionmp.setText('')
        self.ui.radiomp.setChecked(0); self.ui.linecodigomp.setEnabled(True)
        self.ui.linenombremp.setEnabled(False); self.ui.linepreciomp.setEnabled(False)
        self.ui.linecantidadmp.setEnabled(False); self.ui.linereposicionmp.setEnabled(False)
        self.ui.linecodigoaltins.setText(''); self.ui.linedescripcionaltins.setText(''); self.ui.lineprecioaltins.setText('')
        self.ui.linecantidadaltins.setText(''); self.ui.linereposicionaltins.setText('')
        self.ui.linecodigovistacs.setText(''); self.ui.linedescripcioncs.setText(''); self.ui.linestockcs.setText('')
        self.ui.linepuntoreposicioncs.setText(''); self.ui.linereponeronocs.setText('')
        self.ui.linecodigovistacsi.setText(''); self.ui.linedescripcioncsi.setText(''); self.ui.linestockcsi.setText('')
        self.ui.linepuntoreposicioncsi.setText(''); self.ui.linereponeronocsi.setText('')

def conectar():
        conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="angelita")
        return conn

def verificar(lafechad, lafechah):
    fec=""
    if lafechad == "//":
        fec ="fechad "
    if lafechah == "//":
        fec+="y fechah"
    return fec

def errorfecha(aniod, mesd, diad, anioh,mesh,diah):
    msg=""
    if (aniod> anioh):
        msg= "anio desde mayor que anio hasta"
    else:
            if(aniod == anioh):
                if (mesd > mesh):
                    msg="mes desde mayor que mes hasta"
                else:
                    if (mesd == mesh):
                        if (diad > diah):
                            msg="dia desde mayor que el dia hasta"
    return msg

def longitudysolonumeros(aniod, mesd, diad, anioh, mesh, diah):
    msg=""
    if not re.match("^[0-9]{4}$", aniod):
            msg = 'aniod, '
    if (not re.match("^[0-9]{2}$", mesd)) or(int(mesd) == 00) or (int(mesd) > 12):
            msg+= 'mesd, '
    if (not re.match("^[0-9]{2}$", diad)) or (int(diad) == 00) or (int(diad) > 31):
            msg+= 'diad, '
    if not re.match("^[0-9]{4}$", anioh):
            msg+= 'anioh, '
    if (not re.match("^[0-9]{2}$", mesh)) or (int(mesh) == 00) or (int(mesh) > 12):
            msg+= 'mesh, '
    if (not re.match("^[0-9]{2}$", diah)) or (int(diah) == 00) or (int(diah) > 31):
            msg+= 'diah, '
    return msg

def longitudysolonumeroscv(anio, mes, dia, fecha):
    msg=""
    if fecha == "//":
        msg ="fecha"
    else:
        if not re.match("^[0-9]{4}$", anio):
                msg = 'anio, '
        if (not re.match("^[0-9]{2}$", mes)) or(int(mes) == 00) or (int(mes) > 12):
                msg+= 'mes, '
        if (not re.match("^[0-9]{2}$", dia)) or (int(dia) == 00) or (int(dia) > 31):
                msg+= 'dia, '
    return msg

if __name__ == "__main__":
    lista = []
    listacom = []
    listarot = []
    listacomins = []
    listagasins = []
    app = QtGui.QApplication(sys.argv)
    myapp = MiForm()
    myapp.show()
    sys.exit(app.exec_())







