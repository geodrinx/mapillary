# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mapillary
                                 A QGIS plugin
 mapillary
                             -------------------
        begin                : 2015-01-20
        copyright            : (C) 2015 by geodrinx
        email                : geodrinx@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load mapillary class from file mapillary.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mapillary import mapillary
    return mapillary(iface)
