from PyQt4.QtCore import QFile
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
import os
import subprocess

pdf_out = '/home/bergw/_TEMP/out.pdf'
if os.path.isfile(pdf_out):
   os.remove(pdf_out)
mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)

xml_file = QFile('/home/bergw/VoGIS-Raumplanung-Daten/A4_hoch_template.qpt')
if xml_file.open(QIODevice.ReadOnly) is False:
    throwError

doc = QDomDocument('mydoc')
doc.setContent(xml_file)
if c.loadFromTemplate(doc) is False:
    throwError

if QGis.QGIS_VERSION_INT > 20200:
    #compmaps = self.__get_items(QgsComposerMap)
    #compmap = compmaps[0]
    pass
else:
    compmap = c.composerMapItems()[0]

c.setPlotStyle(QgsComposition.Print)
compmap.setPreviewMode(QgsComposerMap.Render)
#compmap.updateItem()
#emit compmap.itemChanged();
#compmap.extentChanged();
#compmap.toggleAtlasPreview()
#compmap.setNewScale(compmap.scale()+1)
#c.setPrintResolution(150)
#print c.printResolution()
c.setPrintAsRaster(False)

printer = QPrinter()
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName(pdf_out)
printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
printer.setFullPage(True)
printer.setColorMode(QPrinter.Color)
printer.setResolution(c.printResolution())

pdfPainter = QPainter(printer)
paperRectMM = printer.pageRect(QPrinter.Millimeter)
paperRectPixel = printer.pageRect(QPrinter.DevicePixel)

QgsPaintEngineHack.fixEngineFlags(printer.paintEngine())

#c.renderPage(pdfPainter, 0)
c.doPrint(printer,pdfPainter)

pdfPainter.end()
subprocess.call(('xdg-open', pdf_out))

print 'FERTIG'