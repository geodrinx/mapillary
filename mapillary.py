# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mapillary
                                 A QGIS plugin
 mapillary
                              -------------------
        begin                : 2015-01-20
        git sha              : $Format:%H$
        copyright            : (C) 2015 by geodrinx
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from mapillary_dialog import mapillaryDialog
import os.path

from qgis.core import *
from qgis.gui import *
import qgis
from PyQt4.QtCore import QFileInfo

class mapillary:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'mapillary_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = mapillaryDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&mapillary')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'mapillary')
        self.toolbar.setObjectName(u'mapillary')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('mapillary', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/mapillary/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'mapillary'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&mapillary'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):


            import urllib2

            mapCanvas = self.iface.mapCanvas()
            
# Prendo le coordinate della finestra attuale---------------------------------------

            mapRect = mapCanvas.extent()

            mapRenderer = mapCanvas.mapRenderer() 
            
            x1 = mapRect.xMinimum()
            y1 = mapRect.yMinimum()            
            
            x2 = mapRect.xMaximum()
            y2 = mapRect.yMaximum()                   
                
            srs = mapRenderer.destinationCrs()
            crsSrc = srs  
            crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
            xform = QgsCoordinateTransform(crsSrc, crsDest)

            pt1 = xform.transform(QgsPoint(x1, y1))				
            pt2 = xform.transform(QgsPoint(x2, y2))
            
            x1,y1 = pt1.x(),pt1.y()
            x2,y2 = pt2.x(),pt2.y()


            stringa1 = "http://api.mapillary.com/v1/im/search?"
#            stringa1 = "http://api.mapillary.com/v1/s/search?"            
            stringa2 = ("min-lat=%s") %(y1) 
            stringa3 = ("&max-lat=%s") %(y2)
            stringa4 = ("&min-lon=%s") %(x1) 
            stringa5 = ("&max-lon=%s") %(x2)
#            stringa7 = ("&max-results=100&geojson=true")        
            stringa7 = ("&geojson=true")
            
            stringaUrl = stringa1 + stringa2 + stringa3 + stringa4 + stringa5 + stringa7

            print stringaUrl
            
            response = urllib2.urlopen(stringaUrl)
            geojson = response.read()

            tempDir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "python/plugins/mapillary/temp/"
            
            nomegeojson = tempDir + "mapillary.geojson"
            f = open(nomegeojson, 'w')				
            f.write(str(geojson) + '\n')
            f.close()

            
            vlayer = QgsVectorLayer(nomegeojson, "Mapillary", "ogr")

            trovato = 0
            for iLayer in range(mapCanvas.layerCount()):
               layer = mapCanvas.layer(iLayer)
               if layer.name() == "Mapillary":
                  trovato = 1

            if (trovato == 0):        
               QgsMapLayerRegistry.instance().addMapLayer(vlayer)                                       

#  Mapillary_vector
# Your applications
# mapillary_qgis_plugin
# geodrinx
# a QGIS plugin
# Client ID
#  T0tZc2stUldfRE5PNGhybGllbVFSdzozMWI2NWE0ZjQ0NWU1MmUw
# Client Secret
#  YzFiMGI4MDhhNzk4ZTBjYzk5OGQwYTJlOGY2YzBlZjU=
# Number of users: 0


# https://d2munx5tg0hw47.cloudfront.net/tiles/{z}/{x}/{y}.mapbox
#   https://d2munx5tg0hw47.cloudfront.net/tiles/{10}/{16.615851}/{40.206951}.mapbox

# http://www.mapillary.com/connect?client_id=<CLIENT_ID>&response_type=token&scope=user:email%20org:read&redirect_uri=http:%2F%2Fexample.com

# <Error><Code>AccessDenied</Code><Message>Access Denied</Message><RequestId>A3EEA36689C8D032</RequestId><HostId>FHx+77P1ZWAhTKT4SEvE9yHvA7UZRWdZdmVVIJ9ZX7BOPzx09Y5eWb7UEBaADYk6EzqO30CYXuw=</HostId></Error>

            z = 10
##            stringa1 = "https://d2munx5tg0hw47.cloudfront.net/tiles/"            
            stringa1 = "http://www.mapillary.com/connect?client_id=T0tZc2stUldfRE5PNGhybGllbVFSdzozMWI2NWE0ZjQ0NWU1MmUw&response_type=token&scope=user:geodrinx:read&redirect_uri=https://d2munx5tg0hw47.cloudfront.net/tiles/"
            stringa2 = ("{%s}/") %(z) 
            stringa3 = ("{%s}/") %(x1)
            stringa4 = ("{%s}.mapbox") %(y1) 

            stringaUrl = stringa1 + stringa2 + stringa3 + stringa4

            print stringaUrl
            
#            response = urllib2.urlopen(stringaUrl)
#            geojson = response.read()
#
#            tempDir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "python/plugins/mapillary/temp/"
#            
#            nomegeojson = tempDir + "mapillary_vector.geojson"
#            f = open(nomegeojson, 'w')				
#            f.write(str(geojson) + '\n')
#            f.close()
#
#            
#            vlayer = QgsVectorLayer(nomegeojson, "Mapillary", "ogr")
#            
#            trovato = 0
#            for iLayer in range(mapCanvas.layerCount()):
#               layer = mapCanvas.layer(iLayer)
#               if layer.name() == "Mapillary":
#                  trovato = 1
#
#            if (trovato == 0):        
#               QgsMapLayerRegistry.instance().addMapLayer(vlayer)              
