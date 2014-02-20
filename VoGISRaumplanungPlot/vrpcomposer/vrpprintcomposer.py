# -*- coding: utf-8 -*-
"""Atlas Generation"""

import math
import os
import sys
import traceback
from time import strftime
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import Qt
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QTreeWidget
import processing
from qgis.core import QgsComposerLabel
from qgis.core import QgsComposerLegend
from qgis.core import QgsComposition
from qgis.core import QgsExpression
from qgis.core import QgsFeatureRequest
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsMessageLog
from qgis.core import QgsRasterLayer
from qgis.core import QgsVectorLayer
from qgis.gui import QgsMessageBar
from ..vrpcore.constvals import *
from ..vrpbo.vrpbostatistik import VRPStatistik
from ..vrpbo.vrpbostatistiksubthema import VRPStatistikSubThema


class VRPPrintComposer:
    """Atlas Generation"""
    def __init__(
                 self,
                 iface,
                 gemname,
                 coveragelayer,
                 json_settings,
                 gnr_nbrs,
                 featurefilter,
                 orthoimage,
                 themen,
                 templateqpt,
                 pdfmap
                 ):
        self.iface = iface
        self.legiface = self.iface.legendInterface()
        self.toc = self.iface.mainWindow().findChild(QTreeWidget, 'theMapLegend')
        self.canvas = self.iface.mapCanvas()
        self.map_renderer = self.canvas.mapRenderer()
        self.gem_name = gemname
        self.coverage_layer = coveragelayer
        self.gnrs = gnr_nbrs
        self.settings = json_settings
        self.feature_filter = featurefilter
        self.ortho = orthoimage
        self.ortho_lyr = None
        self.themen = themen
        self.composition = None
        self.comp_textinfo = None
        self.template_qpt = templateqpt
        self.pdf_map = pdfmap
        self.lyrname_ortho = 'Luftbild'
        self.lyrname_dkm_gst = 'DKM'
        self.lyrname_dkm_gnr = 'DKM GNR'
        self.comp_leg = []
        self.comp_lbl = []
        self.statistics = {}

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

            #read plotlayout
            composition = QgsComposition(self.map_renderer)
            self.composition = composition
            composition.setPlotStyle(QgsComposition.Print)
            error, xml_doc = self.__read_template()
            if not error is None:
                return error
            if composition.loadFromTemplate(xml_doc) is False:
                return u'Konnte Template nicht laden!\n{0}'.format(self.template_qpt)

            #read textinfo layout
            self.comp_textinfo = QgsComposition(self.map_renderer)
            self.comp_textinfo.setPlotStyle(QgsComposition.Print)
            error, xml_doc = self.__read_template(True)
            if not error is None:
                return error
            if self.comp_textinfo.loadFromTemplate(xml_doc) is False:
                return u'Konnte Template nicht laden!\n{0}'.format(self.settings.textinfo_layout())


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

            self.comp_leg = self.__get_items(QgsComposerLegend)
            self.comp_lbl = self.__get_items(QgsComposerLabel)


            self.__update_composer_items('DKM')

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
                self.statistics = {}
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
                        self.__update_composer_items(thema.name)
                        composition.renderPage(pdf_painter, 0)
                        QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                        cntr += 1
                    if not sub_themen is None:
                        for sub_thema in sub_themen:
                            layers = self.__add_layers(sub_thema)
                            self.__calculate_statistics(sub_thema, layers)
                            if cntr > 0:
                                printer.newPage()
                            self.__reorder_layers()
                            self.__update_composer_items(thema.name)
                            composition.renderPage(pdf_painter, 0)
                            QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                            cntr += 1
            #output statistics
            if len(self.statistics) > 0:
                lbls = self.__get_items(QgsComposerLabel, self.comp_textinfo)
                self.__update_composer_items('', lbls)
                printer.newPage()
                self.comp_textinfo.renderPage(pdf_painter, 0)
            #end pdf export
            pdf_painter.end()
        except:
            msg = 'export pdf (catch all):\n\n{0}'.format(traceback.format_exc())
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            return msg
        if VRP_DEBUG is True:
            QgsMessageLog.logMessage(u'====== STATISTICS =========', DLG_CAPTION)
            for gnr, stats in self.statistics.iteritems():
                QgsMessageLog.logMessage(u'{0}:\n{1}'.format(gnr, stats.__unicode__()), DLG_CAPTION)
                QgsMessageLog.logMessage(u'- - - - - - - - - - - - - - - - - - - - - - - -', DLG_CAPTION)
            QgsMessageLog.logMessage(u'====== END - STATISTICS =========', DLG_CAPTION)

        return None

    def __calculate_statistics(self, thema, layers):
        features = processing.features(self.coverage_layer)
        for gstk in features:
            try:
                gnr = gstk[self.settings.fld_gnr()]
                flaeche = gstk.geometry().area()
                gstk_stats = VRPStatistik(gnr, flaeche, self.gem_name)
                for lyr in layers:
                    lyrname = lyr.name()
                    lyr_thema = self.__get_thema_by_layername(lyrname)
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'lyrname:{0}, lyr_thema:{1}'.format(lyrname, lyr_thema), DLG_CAPTION)
                    if lyr_thema is None: continue
                    skip = False
                    lyr_quelle = None
                    for quelle in lyr_thema.quellen:
                        if VRP_DEBUG is True: QgsMessageLog.logMessage(u'quelle:{0}, statistik:{1}'.format(quelle.name, quelle.statistik), DLG_CAPTION)
                        if quelle.name == lyrname and quelle.statistik is False:
                            skip = True
                            break
                        elif quelle.name == lyrname and quelle.statistik is True:
                            lyr_quelle = quelle
                            break
                    if skip is True: continue
                    text_flaeche = self.__get_text_flaeche(gstk, lyr, lyr_quelle.attribut)
                    sub_stat = VRPStatistikSubThema(lyrname, text_flaeche)
                    gstk_stats.add_subthema(sub_stat)
                if gnr in self.statistics:
                    self.statistics[gnr].subthemen.extend(gstk_stats.subthemen)
                else:
                    self.statistics[gnr] = gstk_stats
            except:
                msg = '__calculate_statistics:\n\n{0}'.format(traceback.format_exc())
                QgsMessageLog.logMessage(msg, DLG_CAPTION, QgsMessageLog.CRITICAL)
                self.iface.messageBar().pushMessage(msg,  QgsMessageBar.CRITICAL)
                return

    def __get_text_flaeche(self, gstk, layer, fld_name):
        text = {}
        #performance! filter by bb of gstk first
        feat_req = QgsFeatureRequest()
        feat_req.setFilterRect(gstk.geometry().boundingBox())
        for feat in layer.getFeatures(feat_req):
            if feat.geometry().intersects(gstk.geometry()):
                #no fld_name defined: means yes/no only
                if fld_name is None:
                    attr_val = u'Ja'
                else:
                    attr_val = feat[fld_name]
                flaeche = feat.geometry().intersection(gstk.geometry()).area()
                if fld_name in text:
                    text[attr_val] += flaeche
                else:
                    text[attr_val] = flaeche
        if len(text) < 1 and fld_name is None:
            text[u'Nein'] = 0
        elif len(text) < 1 and not fld_name is None:
            text[u'Nein'] = 0
        return text


    def __get_thema_by_layername(self, lyrname):
        for thema in self.themen:
            if thema.name == lyrname:
                return thema
            for subthema in thema.subthemen:
                if subthema.name == lyrname:
                    return subthema
                for quelle in subthema.quellen:
                    if quelle.name == lyrname:
                        return subthema
        return None

    def __update_composer_items(self, oberthema, labels=None):
        if labels is None:
            labels = self.comp_lbl
        for leg in self.comp_leg:
            leg.updateLegend()
        for lbl in labels:
            txt = lbl[1].replace('[Gemeindename]', self.gem_name)
            txt = txt.replace('[Oberthema]', oberthema)
            txt = txt.replace('[GNR]', ', '.join(self.gnrs))
            txt = txt.replace('[TODAY]', strftime("%d.%m.%Y"))
            txt = txt.replace('[DATE]', self.settings.dkm_stand())
            lbl[0].setText(txt)


    def __get_items(self, typ, composition=None):
        if composition is None:
            composition = self.composition
        items = []
        for item in composition.items():
            if isinstance(item, typ):
                #if label keep original text for placeholders
                if isinstance(item, QgsComposerLabel):
                    items.append([item, item.text()])
                else:
                    items.append(item)
        return items

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
                QgsMessageLog.logMessage( u'Raster [{0}] konnte nicht geladen werden!'.format(rasterfile), DLG_CAPTION)
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
                    if not quelle.filter is None:
                        if VRP_DEBUG is True: QgsMessageLog.logMessage('{0}'.format(quelle.filter), DLG_CAPTION)
                        #exp = QgsExpression(quelle.filter)
                        #if exp.hasParserError():
                        #    QgsMessageLog.logMessage( u'Filter ungültig!\nQuelle:[{0}]\nFilter:{1}'.format(quelle.name, quelle.filter), DLG_CAPTION)
                        #else:
                        #    exp.prepare(lyr.pendingFields())
                        lyr.setSubsetString(quelle.filter)
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

    def __delete_pdf(self):
        if os.path.isfile(self.pdf_map):
            try:
                os.remove(self.pdf_map)
            except:
                if VRP_DEBUG is True: QgsMessageLog.logMessage(u'delete error: {0}'.format(self.pdf_map), DLG_CAPTION)
                return u'Konnte Ausgabedatei nicht ĺöschen!\n{0}'.format(self.pdf_map)
        return None

    def __read_template(self, textinfo=False):
        if textinfo:
            filename = self.settings.textinfo_layout()
        else:
            filename = self.template_qpt
        if VRP_DEBUG is True: QgsMessageLog.logMessage(u'reading template: {0}'.format(filename), DLG_CAPTION)
        xml_file = QFile(filename)
        if xml_file.open(QIODevice.ReadOnly) is False:
            return u'Konnte Template nicht öffnen!\n{0}'.format(self.template_qpt), None
        xml_doc = QDomDocument('mydoc')
        xml_doc.setContent(xml_file)
        return None, xml_doc
