from PyQt4.QtCore import QFile
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
import os

pdf_out = '/home/bergw/_TEMP/out.pdf'
if os.path.isfile(pdf_out):
   os.remove(pdf_out)
mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)
#print dir(c)
#c.setAtlasMode(QgsComposition.AtlasMode.ExportAtlas)

xml_file = QFile('/home/bergw/VoGIS-Raumplanung-Daten/A4_hoch_template.qpt')
if xml_file.open(QIODevice.ReadOnly) is False:
    throwError

doc = QDomDocument('mydoc')
doc.setContent(xml_file)
if c.loadFromTemplate(doc) is False:
    throwError

cov_lyr = iface.activeLayer()
print 'cov_lyr', cov_lyr.name()
ac = c.atlasComposition()
ac.setEnabled(True)
ac.setSingleFile(True)
ac.setCoverageLayer(cov_lyr)
#ac.setFeatureFilter('length("GNR") > 7 AND left("GNR",3)=\'120\'')
ac.setFeatureFilter('"GNR" = \'905\'')
ac.setHideCoverage(False)

print 'beginRender, feats:', ac.numFeatures()
ac.beginRender()
for i in range(0, ac.numFeatures()):
    print 'prepareForFeature', i
    ac.prepareForFeature(i)
    img = c.printPageAsRaster(0)
    tmp_file = '/home/bergw/_TEMP/' + str(i) + '.jpg'
    if os.path.isfile(tmp_file):
        os.remove(tmp_file)
    img.save(tmp_file)
ac.endRender()
print 'render finished'


#printer = QPrinter()
#printer.setOutputFormat(QPrinter.PdfFormat)
#printer.setOutputFileName(pdf_out)
#printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
#printer.setFullPage(True)
#printer.setColorMode(QPrinter.Color)
#printer.setResolution(c.printResolution())

#pdfPainter = QPainter(printer)
#paperRectMM = printer.pageRect(QPrinter.Millimeter)
#paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
#TODO: checken ob File vorhanden?
#LOESCHEN!!!
#c.render(pdfPainter, paperRectPixel, paperRectMM)
#pdfPainter.end()

print 'FERTIG'