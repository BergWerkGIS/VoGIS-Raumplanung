# -*- coding: utf-8 -*-
"""Business object for Layout"""

from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *


class VRPLayout:
    """Layout"""
    def __init__(self, js_layout):
        if VRP_DEBUG is True:
            QgsMessageLog.logMessage(u'Layout: {0}'.format(js_layout), DLG_CAPTION)
        self.name = js_layout['name']
        self.pfad = js_layout['pfad']

