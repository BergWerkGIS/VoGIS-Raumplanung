from PyQt4.QtCore import QFile
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter


http://www.qgis.org/en/docs/pyqgis_developer_cookbook/composer.html#output-using-map-composer
mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)

http://qt-project.org/doc/qt-4.8/qdomdocument.html#QDomDocument-2
xml_file = QFile('/home/user/VoGIS-Raumplanung-Daten/A4_hoch_template.qpt')
if xml_file.open(QIODevice.ReadOnly) is True:
    WEITER


doc = QDomDocument('mydoc')
doc.setContent(xml_file)
if c.loadFromTemplate(doc) is True:
    WEITER

