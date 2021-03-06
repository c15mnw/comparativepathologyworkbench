#!/usr/bin/python3
###!
# \file         views_gallery.py
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
# This file contains the add_image_to_collection routine
#
###
from __future__ import unicode_literals

import os
import time

from django.shortcuts import get_object_or_404
from django.apps import apps

from decouple import config

from matrices.routines import get_active_collection_for_user
from matrices.routines import get_image_count_for_image
from matrices.routines import exists_image_for_id_server_owner_roi
from matrices.routines import get_images_for_id_server_owner_roi

#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
def add_image_to_collection(user, server, image_id, roi_id):

    Image = apps.get_model('matrices', 'Image')
    Collection = apps.get_model('matrices', 'Collection')

    image_out = None

    json_image = ''
    image_name = ''
    image_viewer_url = ''
    image_birdseye_url = ''

    if server.is_omero547() or server.is_omero56():

        wp_data = server.get_imaging_server_image_json(image_id)

        group = wp_data['group']
        group_name = group['name']

        projects = wp_data['projects']
        project = projects[0]
        project_name = project['name']

        datasets = wp_data['datasets']
        dataset = datasets[0]
        dataset_name = dataset['name']

        json_image = wp_data['image']
        image_name = json_image['name']

        full_image_name = group_name + "/" + project_name + "/" + dataset_name + "/" + image_name

        image_viewer_url = json_image['viewer_url']
        image_birdseye_url = json_image['birdseye_url']

    if server.is_wordpress():

        wp_data = server.get_wordpress_image_json(user, image_id)

        json_image = wp_data['image']
        full_image_name = json_image['name']
        image_viewer_url = json_image['viewer_url']
        image_birdseye_url = json_image['thumbnail_url']

    if roi_id == 0:

        if exists_image_for_id_server_owner_roi(image_id, server, user, 0):

            existing_image_list = get_images_for_id_server_owner_roi(image_id, server, user, 0)

            image_out = existing_image_list[0]

        else:

            image_out = Image.create(image_id, full_image_name, server, image_viewer_url, image_birdseye_url, roi_id, user)

            image_out.save()

        queryset = get_active_collection_for_user(user)

        for collection in queryset:

            Collection.assign_image(image_out, collection)

    else:

        json_rois = wp_data['rois']

        for rois in json_rois:

            for shape in rois['shapes']:

                if shape['id'] == int(roi_id):

                    image_viewer_url = shape['viewer_url']
                    image_birdseye_url = shape['shape_url']

                    if exists_image_for_id_server_owner_roi(image_id, server, user, roi_id):

                        existing_image_list = get_images_for_id_server_owner_roi(image_id, server, user, roi_id)

                        image_out = existing_image_list[0]

                    else:

                        image_out = Image.create(image_id, full_image_name, server, image_viewer_url, image_birdseye_url, roi_id, user)

                        image_out.save()

                    queryset = get_active_collection_for_user(user)

                    for collection in queryset:

                        Collection.assign_image(image_out, collection)

    return image_out
