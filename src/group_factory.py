# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapServices
                                 A QGIS plugin
 Collection of internet map services
                              -------------------
        begin                : 2014-11-21
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.org
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
import os
from ConfigParser import ConfigParser
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMenu, QIcon

CURR_PATH = os.path.dirname(__file__)
GROUP_PATHS = [
    os.path.join(CURR_PATH, 'groups'),
    os.path.join(CURR_PATH, 'groups_contrib'),
]


class GroupFactory():

    def __init__(self):
        self.groups = {}
        self._fill_groups_list()

    def _fill_groups_list(self):
        self.groups = {}
        for gr_path in GROUP_PATHS:
            for root, dirs, files in os.walk(gr_path):
                for ini_file in [f for f in files if f.endswith('.ini')]:
                    self._read_ini_file(root, ini_file)

    def _read_ini_file(self, root, ini_file):
        try:
            parser = ConfigParser()
            parser.read(os.path.join(root, ini_file))
            group_id = parser.get('general', 'id')
            group_alias = parser.get('ui', 'alias')
            group_icon_path = os.path.join(root, parser.get('ui', 'icon'))
            self.groups[group_id] = QMenu(self.tr(group_alias))
            self.groups[group_id].setIcon(QIcon(group_icon_path))
        except:
            pass

    def get_group(self, group_id):
        if group_id in self.groups:
            return self.groups[group_id]
        else:
            menu = QMenu(group_id)
            self.groups[group_id] = menu
            return menu


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapServices', message)