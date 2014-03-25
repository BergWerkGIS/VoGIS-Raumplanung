# -*- coding: utf-8 -*-
"""Atlas Generation"""

from PyQt4.QtCore import pyqtRemoveInputHook
import pdb
import math
import os
import sys
import traceback
from time import strftime
from collections import OrderedDict
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import Qt
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QSizeF
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QTreeWidget
#import processing
from qgis.core import QGis
from qgis.core import QgsComposerMap
from qgis.core import QgsComposerLabel
from qgis.core import QgsComposerLegend
from qgis.core import QgsComposition
from qgis.core import QgsExpression
from qgis.core import QgsFeatureRequest
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsMessageLog
from qgis.core import QgsPaintEngineHack
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
        self.composermap = None
        self.comp_textinfo = None
        self.template_qpt = templateqpt
        self.pdf_map = pdfmap
        dkmgem = self.settings.dkm_gemeinde(gemname)
        self.lyrname_ortho = self.settings.luftbild_lyrname()
        self.lyrname_dkm_gst = dkmgem['lyrnamegstk']
        self.lyrname_dkm_gnr = dkmgem['lyrnamegnr']
        self.comp_leg = []
        self.comp_lbl = []
        self.statistics = OrderedDict()

    def export_all_features_TEST(self):
        lyr = QgsVectorLayer('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Dornbirn/Flaechenwidmungsplan/fwp_flaeche.shp', 'flaeiw', 'ogr')
        lyr.loadNamedStyle('/home/bergw/VoGIS-Raumplanung-Daten/Geodaten/Raumplanung/Flaechenwidmung/Vorarlberg/Flaechenwidmungsplan/fwp_flaeche.qml')
        QgsMapLayerRegistry.instance().addMapLayer(lyr)

    def export_all_features(self):
        pdf_painter = None
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
            if QGis.QGIS_VERSION_INT > 20200:
                compmaps = self.__get_items(QgsComposerMap)
                if len(compmaps) < 1:
                    return u'Kein Kartenfenster im Layout vorhanden!'
                compmap = compmaps[0]
            else:
                if len(composition.composerMapItems()) < 1:
                    return u'Kein Kartenfenster im Layout vorhanden!'
                compmap = composition.composerMapItems()[0]

            self.composermap = compmap
            #self.composermap.setPreviewMode(QgsComposerMap.Render)
            #self.composermap.setPreviewMode(QgsComposerMap.Rectangle)
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
            #round up to next 1000
            compmap.setNewScale(math.ceil((compmap.scale()/1000.0)) * 1000.0)
            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'bbox new (after scale):{0}'.format(compmap.extent().toString()), DLG_CAPTION)

            #add ORTHO after new extent -> performance
            if not self.ortho is None:
                self.ortho_lyr = self.__add_raster_layer(self.ortho, self.lyrname_ortho)
                self.__reorder_layers()

            self.comp_leg = self.__get_items(QgsComposerLegend)
            self.comp_lbl = self.__get_items(QgsComposerLabel)


            self.__update_composer_items(self.settings.dkm_gemeinde(self.gem_name)['lyrnamegstk'])

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
            QgsPaintEngineHack.fixEngineFlags(printer.paintEngine())
            #DKM only
            if len(self.themen) < 1:
                composition.render(pdf_painter, paper_rect_pixel, paper_rect_mm)
            else:
                self.statistics = OrderedDict()
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
                        self.__calculate_statistics(thema, thema, layers)
                        #no qml -> not visible -> means no map
                        if self.__at_least_one_visible(layers) is True:
                            if cntr > 0:
                                printer.newPage()
                            self.__reorder_layers()
                            self.__update_composer_items(thema.name, layers=layers)
                            composition.renderPage(pdf_painter, 0)
                            QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                            cntr += 1
                        else:
                            QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                    if not sub_themen is None:
                        for sub_thema in sub_themen:
                            if VRP_DEBUG is True: QgsMessageLog.logMessage(u'drucke SubThema:{0}'.format(sub_thema.name), DLG_CAPTION)
                            layers = self.__add_layers(sub_thema)
                            self.__calculate_statistics(thema, sub_thema, layers)
                            #no qml -> not visible -> means no map
                            if self.__at_least_one_visible(layers) is True:
                                if cntr > 0:
                                    printer.newPage()
                                self.__reorder_layers()
                                self.__update_composer_items(thema.name, subthema=sub_thema.name, layers=layers)
                                composition.renderPage(pdf_painter, 0)
                                QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
                                cntr += 1
                            else:
                                QgsMapLayerRegistry.instance().removeMapLayers([lyr.id() for lyr in layers])
            #output statistics
            if len(self.statistics) > 0:
                tabelle = self.__get_item_byid(self.comp_textinfo, 'TABELLE')
                if tabelle is None:
                    self.iface.messageBar().pushMessage(u'Layout (Textinfo): Kein Textelement mit ID "TABELLE" vorhanden.', QgsMessageBar.CRITICAL)
                else:
                    try:
                        str_flaechen = ''
                        idx = 0
                        for gnr, stats in self.statistics.iteritems():
                            comma = ', ' if idx > 0 else ''
                            str_flaechen += u'{0}{1} ({2:.2f}m²)'.format(comma, gnr, stats[0].flaeche)
                            idx += 1
                        lbls = self.__get_items(QgsComposerLabel, self.comp_textinfo)
                        self.__update_composer_items('', labels=lbls, gnrflaeche=str_flaechen)
                        html = tabelle.text()
                        html += u'<table>'
                        #gnrcnt = 0
                        for gnr, stats in self.statistics.iteritems():
                            #if gnrcnt > 0:
                            #    html += u'<tr class="abstand"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>'
                            html += u'<tr><th class="gnr"></th><th class="gnr">{0}</th><th class="gnr"></th></tr>'.format(gnr)
                            #html += u'<tr class="abstand"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>'
                            curr_thema = ''
                            for stat in stats:
                                if stat.thema != curr_thema:
                                    html += u'<tr><th class="thema"></th><th class="thema">{0}</th><th class="thema"></th></tr>'.format(stat.thema)
                                curr_thema = stat.thema
                                for thema, subthema in stat.subthemen.iteritems():
                                    for quelle in subthema:
                                        html += u'<tr><td class="col1">{0}</td>'.format(quelle.name)
                                        attr_val = ''
                                        attr_area = ''
                                        for text, area in quelle.txt_area.iteritems():
                                            attr_val += u'{0}<br />'.format(text)
                                            attr_area += u'{0:.2f}m² <br />'.format(area)
                                        html += u'<td class="col2">{0}</td><td class="col3">{1}</td></tr>'.format(attr_val, attr_area)
                            #gnrcnt += 1
                        html += u'</table>'
                        tabelle.setText(html)
                        printer.newPage()
                        self.comp_textinfo.renderPage(pdf_painter, 0)
                    except:
                        msg = 'Statistikausgabe:\n\n{0}'.format(traceback.format_exc())
                        QgsMessageLog.logMessage(msg, DLG_CAPTION)
                        self.iface.messageBar().pushMessage(msg, QgsMessageBar.CRITICAL)
        except:
            msg = 'export pdf (catch all):\n\n{0}'.format(traceback.format_exc())
            QgsMessageLog.logMessage(msg, DLG_CAPTION)
            self.iface.messageBar().pushMessage(msg.replace(u'\n', u''), QgsMessageBar.CRITICAL)
            return msg
        finally:
            #end pdf
            if not pdf_painter is None:
                pdf_painter.end()
        return None

    def __at_least_one_visible(self, layers):
        """
        check, if at least one layer is visible
        layers are not visible, if they don't have a qml
        if there is no visible layer, there must not be an extra plot page
        """
        one_visible = False
        for lyr in layers:
            if self.legiface.isLayerVisible(lyr):
                one_visible = True
        return one_visible

    def __calculate_statistics(self, thema, subthema, layers):
        #features = processing.features(self.coverage_layer)
        features = self.coverage_layer.selectedFeatures()
        for gstk in features:
            try:
                gnr = gstk[self.settings.fld_gnr()]
                flaeche = gstk.geometry().area()
                gstk_stats = VRPStatistik(gnr, thema.name, flaeche, self.gem_name)
                #pyqtRemoveInputHook()
                #pdb.set_trace()
                #go thru all data sources of subthema
                for quelle in subthema.quellen:
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'quelle:{0}'.format(quelle.name), DLG_CAPTION)
                    #only use those with statistik == True
                    if quelle.statistik is False:
                        continue
                    lyr_curr_quelle = None
                    for lyr in layers:
                        if quelle.name == lyr.name():
                            lyr_curr_quelle = lyr
                    if lyr_curr_quelle is None:
                        continue
                    text_flaeche = self.__get_text_flaeche(quelle, gstk, lyr_curr_quelle, quelle.attribut)
                    sub_stat = VRPStatistikSubThema(quelle.name, text_flaeche)
                    gstk_stats.add_subthema(thema.name, sub_stat)
                if gnr in self.statistics:
                    self.statistics[gnr].append(gstk_stats)
                else:
                    self.statistics[gnr] = [gstk_stats]
            except:
                msg = '__calculate_statistics:\n\n{0}'.format(traceback.format_exc())
                QgsMessageLog.logMessage(msg, DLG_CAPTION, QgsMessageLog.CRITICAL)
                msg = msg.replace('\n', '')
                self.iface.messageBar().pushMessage(msg,  QgsMessageBar.CRITICAL)
                return

    def __get_text_flaeche(self, quelle, gstk, layer, fld_name):
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
                    #convert everything to string
                    #JSON only allows for string keys -> settingsfile
                    if isinstance( attr_val, (int, long)):
                        attr_val = unicode(attr_val)
                    elif isinstance(attr_val, float):
                        attr_val = u'{0:.0f}'.format(attr_val)
                #replace attribute values with mapping text from settings file
                if not quelle.text is None:
                    if attr_val in quelle.text:
                        attr_val = quelle.text[attr_val]
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

    def __update_composer_items(self, oberthema, subthema=None, labels=None, gnrflaeche=None, layers=None):
        if labels is None:
            labels = self.comp_lbl
        for leg in self.comp_leg:
            #if not layers is None:
                #leg_model = leg.model()
#                QgsMessageLog.logMessage(u'layerSet:{0}'.format(leg.composerMap().layerSet()), DLG_CAPTION)
#                for lyr in layers:
#                    QgsMessageLog.logMessage(u'LYR(ID):{0}'.format(lyr.id()), DLG_CAPTION)
#                    leg_model.removeLayer(lyr.id())
                #QgsMessageLog.logMessage(u'maprenderer layerSet:{0}'.format(self.map_renderer.layerSet()), DLG_CAPTION)
                #QgsMessageLog.logMessage(u'legmodel:{0}'.format(dir(leg_model)), DLG_CAPTION)
                #leg_model.setLayerSet([lyr.id() for lyr in layers])
                #for lyr in layers:
                #    leg_model.addLayer(lyr)
            leg.updateLegend()
            if not layers is None:
                lyr_names = [lyr.name() for lyr in layers]
                leg_model = leg.model()
                row_count = leg_model.rowCount() - 1
                for idx in xrange(row_count, -1, -1):
                    leg_row = leg_model.item(idx)
                    if not leg_row.text() in lyr_names:
                        leg_model.removeRow(idx)
                leg.adjustBoxSize()
        for lbl in labels:
            txt = lbl[1].replace('[Gemeindename]', self.gem_name)
            txt = txt.replace('[Oberthema]', oberthema)
            if not subthema is None:
                txt = txt.replace('[Subthema]', subthema)
            txt = txt.replace('[GNR]', ', '.join(self.gnrs))
            if not gnrflaeche is None:
                txt = txt.replace('[GNRFLAECHE]', gnrflaeche)
            txt = txt.replace('[TODAY]', strftime("%d.%m.%Y"))
            txt = txt.replace('[DATE]', self.settings.dkm_stand())
            lbl[0].setText(txt)
        #self.composermap.updateItem()
        #self.composermap.updateCachedImage()
        self.composermap.mapRenderer().updateFullExtent ()


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

    def __get_item_byid(self, composition, item_id):
        return composition.getComposerItemById(item_id)

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
                #turn off layer, if no qml present
                #for layer that should not be displayed but should be
                #used for statistics
                if qml is None:
                    self.legiface.setLayerVisible(lyr, False)
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
        #if xml_file.exists() is False:
        #    return u'\nTemplate ist nicht vorhanden!\n\n{0}'.format(self.template_qpt), None
        if xml_file.open(QIODevice.ReadOnly) is False:
            return u'\nKonnte Template nicht öffnen!\n\n{0}\n\n{1}: {2}'.format(filename, xml_file.error(), xml_file.errorString()), None
        xml_doc = QDomDocument('mydoc')
        xml_doc.setContent(xml_file)
        return None, xml_doc
