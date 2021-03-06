#!/usr/bin/python3
###!
# \file         __init__.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
#
# GALLERY VIEW ROUTINES
#
# def show_imaging_server(request, server_id):
# def show_group(request, server_id, group_id):
# def show_project(request, server_id, project_id):
# def show_dataset(request, server_id, dataset_id):
# def show_image(request, server_id, image_id):
# def show_wordpress(request, server_id, page_id):
# def show_wordpress_image(request, server_id, image_id):
# def add_image(request, server_id, image_id, roi_id):
#
###

from .show_imaging_server import show_imaging_server
from .show_group import show_group
from .show_project import show_project
from .show_dataset import show_dataset
from .show_image import show_image
from .show_wordpress import show_wordpress
from .show_wordpress_image import show_wordpress_image
from .add_image import add_image
