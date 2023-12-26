__author__ = 'Lenovo'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
c = canvas.Canvas("Informe de compras.pdf", pagesize=A4)
c.drawString(50, 500, "Informe de compras")
c.showPage()
c.save()
