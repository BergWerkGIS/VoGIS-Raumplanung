# -*- coding: utf-8 -*-
"""Atlas Generation"""

import math
import os
import sys
import traceback
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import Qt
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QTreeWidget
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsRasterLayer
from qgis.core import QgsExpression
from qgis.core import QgsComposition
from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *


class VRPPrintComposer:
    """Atlas Generation"""
    def __init__(self, iface, gemname, coveragelayer, featurefilter, orthoimage, themen, templateqpt, pdfmap):
        self.iface = iface
        self.legiface = self.iface.legendInterface()
        self.toc = self.iface.mainWindow().findChild(QTreeWidget, 'theMapLegend')
        self.canvas = self.iface.mapCanvas()
        self.map_renderer = self.canvas.mapRenderer()
        self.gem_name = gemname
        self.coverage_layer = coveragelayer
        self.feature_filter = featurefilter
        self.ortho = orthoimage
        self.ortho_lyr = None
        self.themen = themen
        self.template_qpt = templateqpt
        self.pdf_map = pdfmap
        self.lyrname_ortho = 'Luftbild'
        self.lyrname_dkm_gst = 'DKM'
        self.lyrname_dkm_gnr = 'DKM GNR'
        self.comp_leg = None

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
                self.ortho_lyr = self.__add_raster_layer(self.ortho, self.lyrname_ortho)
                self.__reorder_layers()
                self.__update_composer_items()

            self.comp_leg = composition.getComposerItemById('LEGENDE')
            self.__update_composer_items()

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
                        self.__reorder_layers()
                        self.__update_composer_items()
                        composition.renderPage(pdf_painter, 0)
                        QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                        cntr += 1
                    if not sub_themen is None:
                        for sub_thema in sub_themen:
                            layers = self.__add_layers(sub_thema)
                            if cntr > 0:
                                printer.newPage()
                            self.__reorder_layers()
                            self.__update_composer_items()
                            composition.renderPage(pdf_painter, 0)
                            QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                            cntr += 1
            pdf_painter.end()
        except:
            msg = 'export pdf (catch all):\n\n{0}'.format(traceback.format_exc())
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return msg
        return None

    def __update_composer_items(self):
        if self.comp_leg is not None:
            self.comp_leg.updateLegend()

    def __reorder_layers(self):
        #move ortho to bottom
        if not self.ortho_lyr is None:
            for idx in range(0, self.toc.topLevelItemCount()):
                if self.toc.topLevelItem(idx).text(0) == self.lyrname_ortho:
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'idx {0}:{1}'.format(self.lyrname_ortho, idx), DLG_CAPTION)
                    item = self.toc.takeTopLevelItem(idx)
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'topLevelItemCount:{0}'.format(self.toc.topLevelItemCount()), DLG_CAPTION)
                    self.toc.insertTopLevelItem(self.toc.topLevelItemCount(), item)
                    #legiface.refreshLayerSymbology(self.ortho_lyr)
                    #self.canvas.setDirty(True)
                    #self.canvas.refresh()
                    #!!!!HACK TO REFRESH DRAWING ORDER
                    #With Python there is no possibility to change oder of layer
                    #in legend (=TOC)
                    #http://gis.stackexchange.com/a/42007
                    #Currently, using Python, there is limited functionality
                    #for manipulating the QgsLegend. There is the QgsLegendInterface
                    #but this does not have all the goodies that are present
                    #in the QgsLegend, QgsLegendLayer, the inherited QgsLegendItem,
                    #or any of the other classes associated with QgsLegend.
                    self.legiface.setLayerVisible(self.ortho_lyr, False)
                    self.legiface.setLayerVisible(self.ortho_lyr, True)
                    if VRP_DEBUG is True:
                        tmp = [lyr.name() for lyr in self.canvas.layers()]
                        QgsMessageLog.logMessage(u'layers:{0}'.format(tmp), DLG_CAPTION)
                    break
            #o = self.toc.findItems(self.lyrname_ortho, Qt.MatchExactly)[0]
            #QgsMessageLog.logMessage('toc:{0}'.format(dir(o)), DLG_CAPTION)
            #toc.sortItems(0, Qt.AscendingOrder)
        #move dkm to top
        lyr_dkm_gst = self.__get_layer(self.lyrname_dkm_gst)
        lyr_dkm_gnr = self.__get_layer(self.lyrname_dkm_gnr)
        if lyr_dkm_gst is None or lyr_dkm_gnr is None:
            return
        #gst to top
        for idx in range(0, self.toc.topLevelItemCount()):
            if self.toc.topLevelItem(idx).text(0) == self.lyrname_dkm_gst:
                item = self.toc.takeTopLevelItem(idx)
                self.toc.insertTopLevelItem(0, item)
                self.legiface.setLayerVisible(lyr_dkm_gst, False)
                self.legiface.setLayerVisible(lyr_dkm_gst, True)
                break
        #move gnr to top
        for idx in range(0, self.toc.topLevelItemCount()):
            if self.toc.topLevelItem(idx).text(0) == self.lyrname_dkm_gnr:
                item = self.toc.takeTopLevelItem(idx)
                self.toc.insertTopLevelItem(0, item)
                self.legiface.setLayerVisible(lyr_dkm_gnr, False)
                self.legiface.setLayerVisible(lyr_dkm_gnr, True)
                break

    def __get_layer(self, lyrname):
        for lyr in self.legiface.layers():
            if lyr.name() == lyrname:
                return lyr
        return None

    def __add_raster_layer(self, rasterfile, legend_name=None):
        try:
            if VRP_DEBUG is True: QgsMessageLog.logMessage('export pdf (__add_raster_layer): {0}'.format(rasterfile), DLG_CAPTION)
            if legend_name is None:
                fileinfo = QFileInfo(rasterfile)
                basename = fileinfo.baseName()
            else:
                basename = legend_name
            lyr = QgsRasterLayer(rasterfile, basename)
            if not lyr.isValid():
                QgsMessageLog.logMessage( u'Raster [{0}] konnte nicht geladen werden:\n{1}'.format(rasterfile), DLG_CAPTION)
                return None
            QgsMapLayerRegistry.instance().addMapLayer(lyr)
            return lyr
        except:
            msg = 'export pdf (__add_raster_layer): {0}'.format(traceback.format_exc())
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return None

    def __add_layers(self, thema):
        try:
            layers = []
            for quelle in thema.quellen:
                pfad = quelle.pfad.replace('{gem_name}', self.gem_name)
                qml = None
                if not quelle.qml is None:
                    qml = quelle.qml.replace('{gem_name}', self.gem_name)
                if VRP_DEBUG is True: QgsMessageLog.logMessage('adding lyr:\n{0}\n{1}'.format(pfad, qml), DLG_CAPTION)
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
        except:
            msg = 'export pdf (__add_layers): {0}'.format(sys.exc_info()[0])
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return None

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
