# -*- coding: utf-8 -*-
"""Atlas Generation"""

import math
import os
import sys
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsRasterLayer
from qgis.core import QgsExpression
from qgis.core import QgsComposition
from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *


class VRPPrintComposer:
    """Atlas Generation"""
    def __init__(self, mapcanvas, gemname, coveragelayer, featurefilter, orthoimage, themen, templateqpt, pdfmap):
        self.canvas = mapcanvas
        self.map_renderer = self.canvas.mapRenderer()
        self.gem_name = gemname
        self.coverage_layer = coveragelayer
        self.feature_filter = featurefilter
        self.ortho = orthoimage
        self.ortho_lyr = None
        self.themen = themen
        self.template_qpt = templateqpt
        self.pdf_map = pdfmap

    def export_all_features_TEST(self):
        lyr = QgsVectorLayer('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Dornbirn/Flaechenwidmungsplan/fwp_flaeche.shp', 'flaeiw', 'ogr')
        lyr.loadNamedStyle('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Vorarlberg/Flaechenwidmungsplan/fwp_flaeche.qml')
        QgsMapLayerRegistry.instance().addMapLayer(lyr)

    def export_all_features(self):
        """Export map to pdf atlas style (one page per feature)"""
        if VRP_DEBUG is True: QgsMessageLog.logMessage(u'exporting map', DLG_CAPTION)
        try:

            result = self.__delete_pdf()
            if not result is None:
                return result

            ids = []
            exp = QgsExpression(self.feature_filter)
            if exp.hasParserError():
                raise Exception(exp.parserErrorString())
            exp.prepare(self.coverage_layer.pendingFields())
            for feature in self.coverage_layer.getFeatures():
                value = exp.evaluate(feature)
                if exp.hasEvalError():
                    raise ValueError(exp.evalErrorString())
                if bool(value):
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'export map, feature id:{0}'.format(feature.id()), DLG_CAPTION)
                    ids.append(feature.id())
            self.coverage_layer.select(ids)
            bbox = self.coverage_layer.boundingBoxOfSelected()
            self.canvas.zoomToSelected(self.coverage_layer)
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'bbox:{0}'.format(bbox.toString()), DLG_CAPTION)

            #self.map_renderer.setExtent(bbox)
            #self.map_renderer.updateScale()

            composition = QgsComposition(self.map_renderer)
            composition.setPlotStyle(QgsComposition.Print)

            error, xml_doc = self.__read_template()
            if not error is None:
                return error
            if composition.loadFromTemplate(xml_doc) is False:
                return u'Konnte Template nicht laden!\n{0}'.format(self.template_qpt)

            new_ext = bbox
            compmap = composition.composerMapItems()[0]
            #taken from QgsComposerMap::setNewAtlasFeatureExtent (not yet available in QGIS 2.0)
            #http://www.qgis.org/api/qgscomposermap_8cpp_source.html#l00610
            old_ratio = compmap.rect().width() / compmap.rect().height()
            new_ratio = new_ext.width() / new_ext.height()
            if old_ratio < new_ratio:
                new_height = new_ext.width() / old_ratio
                delta_height = new_height - new_ext.height()
                new_ext.setYMinimum( bbox.yMinimum() - delta_height / 2)
                new_ext.setYMaximum(bbox.yMaximum() + delta_height / 2)
            else:
                new_width = old_ratio * new_ext.height()
                delta_width = new_width - new_ext.width()
                new_ext.setXMinimum(bbox.xMinimum() - delta_width / 2)
                new_ext.setXMaximum(bbox.xMaximum() + delta_width / 2)

            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'bbox old:{0}'.format(compmap.extent().toString()), DLG_CAPTION)
            compmap.setNewExtent(new_ext)
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'bbox new:{0}'.format(compmap.extent().toString()), DLG_CAPTION)
            #round up to next 100
            compmap.setNewScale(math.ceil((compmap.scale()/100.0)) * 100.0)
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'bbox new (after scale):{0}'.format(compmap.extent().toString()), DLG_CAPTION)

            #add ORTHO after new extent -> performance
            if not self.ortho is None:
                self.ortho_lyr = self.__add_raster_layer(self.ortho)

            legend = composition.getComposerItemById('LEGENDE')
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'legende:{0}'.format(legend), DLG_CAPTION)
            if legend is not None:
                legend.updateLegend()
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(self.pdf_map)
            printer.setPaperSize(QSizeF(composition.paperWidth(), composition.paperHeight()), QPrinter.Millimeter)
            printer.setFullPage(True)
            printer.setColorMode(QPrinter.Color)
            printer.setResolution(composition.printResolution())

            pdf_painter = QPainter(printer)
            paper_rect_pixel = printer.pageRect(QPrinter.DevicePixel)
            paper_rect_mm = printer.pageRect(QPrinter.Millimeter)
            #DKM only
            if len(self.themen) < 1:
                composition.render(pdf_painter, paper_rect_pixel, paper_rect_mm)
            else:
                try:
                    pass
                    #lyr = QgsVectorLayer('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Dornbirn/Flaechenwidmungsplan/fwp_flaeche.shp', 'flaeiw', 'ogr')
                    #lyr.loadNamedStyle('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Vorarlberg/Flaechenwidmungsplan/fwp_flaeche.qml')
                    #QgsMapLayerRegistry.instance().addMapLayer(lyr)
                except:
                    QgsMessageLog.logMessage('new lyr:{0}'.format(sys.exc_info()[0]), DLG_CAPTION)
                #QgsMapLayerRegistry.instance().addMapLayer(lyr)
                cntr = 0
                for thema, sub_themen in self.themen.iteritems():
                    if VRP_DEBUG is True: QgsMessageLog.logMessage('drucke Thema:{0}'.format(thema.name), DLG_CAPTION)
                    if sub_themen is None:
                        layers = self.__add_layers(thema)
                        if cntr > 0:
                            printer.newPage()
                        composition.renderPage(pdf_painter, 0)
                        QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                        cntr += 1
                    if not sub_themen is None:
                        for sub_thema in sub_themen:
                            layers = self.__add_layers(sub_thema)
                            if cntr > 0:
                                printer.newPage()
                            composition.renderPage(pdf_painter, 0)
                            QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                            cntr += 1
            pdf_painter.end()
        except AttributeError as exae:
            ex_txt = u'{0}'.format(exae.message)
            msg = 'export pdf (all features style), catch all: {0}'.format(ex_txt)
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return msg
        except TypeError as exte:
            ex_txt = u'{0}'.format(exte.message)
            msg = 'export pdf (all features style), catch all: {0}'.format(ex_txt)
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return msg
        except:
            msg = 'export pdf (all features style), catch all: {0}'.format(sys.exc_info()[0])
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return msg
        return None

    def __add_raster_layer(self, rasterfile):
        fileinfo = QFileInfo(rasterfile)
        basename = fileinfo.baseName()
        lyr = QgsRasterLayer(rasterfile, basename)
        if not lyr.isValid():
            QgsMessageLog.logMessage( u'Raster [{0}] konnte nicht geladen werden:\n{1}'.format(rasterfile), DLG_CAPTION)
            return None
        QgsMapLayerRegistry.instance().addMapLayer(lyr)
        return lyr

    def __add_layers(self, thema):
        layers = []
        for quelle in thema.quellen:
            pfad = quelle.pfad.replace('{gem_name}', self.gem_name)
            qml = None
            if not quelle.qml is None:
                qml = quelle.qml.replace('{gem_name}', self.gem_name)
            if VRP_DEBUG is True: QgsMessageLog.logMessage('adding lyr:{0}'.format(pfad), DLG_CAPTION)
            if pfad.lower().endswith('.shp') is True:
                lyr = QgsVectorLayer(pfad, quelle.name, 'ogr')
            else:
                fileinfo = QFileInfo(pfad)
                basename = fileinfo.baseName()
                lyr = QgsRasterLayer(pfad, basename)
                if not lyr.isValid():
                    QgsMessageLog.logMessage( u'Raster [{0}] konnte nicht geladen werden:\n{1}'.format(thema.name, pfad), DLG_CAPTION)
                    continue
            if not qml is None:
                lyr.loadNamedStyle(qml)
            QgsMapLayerRegistry.instance().addMapLayer(lyr)
            layers.append(lyr)
        return layers

    def export_atlas(self):
        """Export map to pdf atlas style (one page per feature)"""
        if VRP_DEBUG is True: QgsMessageLog.logMessage(u'exporting map', DLG_CAPTION)
        try:
            result = self.__delete_pdf()
            if not result is None:
                return result
            composition = QgsComposition(self.map_renderer)
            composition.setPlotStyle(QgsComposition.Print)

            error, xml_doc = self.__read_template()
            if not error is None:
                return error
            if composition.loadFromTemplate(xml_doc) is False:
                return u'Konnte Template nicht laden!\n{0}'.format(self.template_qpt)

            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'creating atlas', DLG_CAPTION)
            atlas = composition.atlasComposition()
            atlas.setEnabled(True)
            atlas.setSingleFile(True)
            atlas.setCoverageLayer(self.coverage_layer)
            atlas.setFeatureFilter(self.feature_filter)
            atlas.setHideCoverage(False)

            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'creating printer', DLG_CAPTION)
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(self.pdf_map)
            printer.setPaperSize(QSizeF(composition.paperWidth(), composition.paperHeight()), QPrinter.Millimeter)
            printer.setFullPage(True)
            printer.setColorMode(QPrinter.Color)
            printer.setResolution(composition.printResolution())

            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'creating painter', DLG_CAPTION)
            pdf_painter = QPainter(printer)
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'atlas beginRender', DLG_CAPTION)
            atlas.beginRender()

            num_feats = atlas.numFeatures()
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'atlas features: {0}'.format(num_feats), DLG_CAPTION)
            for i in range(0, num_feats):
                if VRP_DEBUG is True: QgsMessageLog.logMessage(u'printing page: {0}/{1}'.format(i, num_feats), DLG_CAPTION)
                atlas.prepareForFeature(i)
                composition.renderPage(pdf_painter, 0)
                if i < num_feats - 1:
                    printer.newPage()
            atlas.endRender()
            pdf_painter.end()
        except:
            return 'export pdf (atlas style), catch all: {0}'.format(sys.exc_info()[0])
        return None

    def __delete_pdf(self):
        if os.path.isfile(self.pdf_map):
            try:
                os.remove(self.pdf_map)
            except:
                if VRP_DEBUG is True: QgsMessageLog.logMessage(u'delete error: {0}'.format(self.pdf_map), DLG_CAPTION)
                return u'Konnte Ausgabedatei nicht ĺöschen!\n{0}'.format(self.pdf_map)
        return None

    def __read_template(self):
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'reading template: {0}'.format(self.template_qpt), DLG_CAPTION)
            xml_file = QFile(self.template_qpt)
            if xml_file.open(QIODevice.ReadOnly) is False:
                return u'Konnte Template nicht öffnen!\n{0}'.format(self.template_qpt), None
            xml_doc = QDomDocument('mydoc')
            xml_doc.setContent(xml_file)
            return None, xml_doc
