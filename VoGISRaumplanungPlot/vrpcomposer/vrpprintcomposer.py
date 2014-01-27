# -*- coding: utf-8 -*-
"""Atlas Generation"""

import os
from PyQt4.QtCore import QFile
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
from qgis.core import QgsComposition

class VRPPrintComposer:
    """Atlas Generation"""
    def __init(self, maprenderer, coveragelayer, featurefilter, templateqpt, pdfmap):
        self.map_renderer = maprenderer
        self.coverage_layer = coveragelayer
        self.feature_filter = featurefilter
        self.template_qpt = templateqpt
        self.pdf_map = pdfmap

    def export_map(self):
        """Export map to pdf"""
        if os.path.isfile(self.pdf_map):
            try:
                os.remove(self.pdf_map)
            except:
                return u'Konnte Ausgabedatei nicht ĺöschen!\n{0}'.format(self.pdf_map)
        composition = QgsComposition(self.map_renderer)
        composition.setPlotStyle(QgsComposition.Print)

        xml_file = QFile(self.template_qpt)
        if xml_file.open(QIODevice.ReadOnly) is False:
            return u'Konnte Template nicht öffnen!\n{0}'.format(self.template_qpt)
        xml_doc = QDomDocument('mydoc')
        xml_doc.setContent(xml_file)
        if composition.loadFromTemplate(xml_doc) is False:
            return u'Konnte Template nicht laden!\n{0}'.format(self.template_qpt)

        atlas = composition.atlasComposition()
        atlas.setEnabled(True)
        atlas.setSingleFile(True)
        atlas.setCoverageLayer(self.coverage_layer)
        atlas.setFeatureFilter(self.feature_filter)
        atlas.setHideCoverage(False)

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(self.pdf_map)
        printer.setPaperSize(QSizeF(composition.paperWidth(), composition.paperHeight()), QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setColorMode(QPrinter.Color)
        printer.setResolution(composition.printResolution())

        pdf_painter = QPainter(printer)
        atlas.beginRender()

        num_feats = atlas.numFeatures()
        for i in range(0, num_feats):
            atlas.prepareForFeature(i)
            composition.renderPage(pdf_painter, 0)
            if i < num_feats - 1:
                printer.newPage()
        atlas.endRender()
        pdf_painter.end()
