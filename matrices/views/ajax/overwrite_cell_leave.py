#!/usr/bin/python3
###!
# \file         views_ajax.py
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
# This file contains the overwrite_cell_leave view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Cell
from matrices.models import Image

from matrices.routines import credential_exists
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_authority_for_bench_and_user_and_requester

WORDPRESS_SUCCESS = 'Success!'

#
# OVERWRITE A TARGET CELL AND LEAVE SOURCE IN PLACE - COPY
#
#  Overwrites Target Cell with Source Cell, Source Cell is left in place
#
@login_required()
def overwrite_cell_leave(request):
    """
    AJAX - Overwrite Cell
    """

    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']

    source_cell = get_object_or_404(Cell, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)

    matrix = source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    serverWordpress = get_primary_wordpress_server()

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            data = { 'failure': True, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)

        else:

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:

                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()

                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            if target_cell.has_blogpost():

                credential = get_credential_for_user(request.user)

                if credential.has_apppwd():

                    response = serverWordpress.delete_wordpress_post(request.user.username, target_cell.blogpost)

                    if response != WORDPRESS_SUCCESS:

                        messages.error(request, "WordPress Error - Contact System Administrator")

            if target_cell.has_image():

                if not exists_collections_for_image(target_cell.image):

                    cell_list = get_cells_for_image(target_cell.image)

                    delete_flag = True

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix_id:

                            delete_flag = False

                    if delete_flag == True:

                        image = target_cell.image

                        target_cell.image = None

                        target_cell.save()

                        image.delete()

            target_cell.title = source_cell.title
            target_cell.description = source_cell.description

            if source_cell.has_image():

                imageOld = Image.objects.get(pk=source_cell.image.id)

                imageNew = Image.create(imageOld.identifier, imageOld.name, imageOld.server, imageOld.viewer_url, imageOld.birdseye_url, imageOld.roi, imageOld.owner)

                imageNew.save()

                target_cell.image = imageNew


            target_cell.blogpost = source_cell.blogpost

            if source_cell.has_blogpost():

                credential = get_credential_for_user(request.user)

                post_id = ''

                if credential.has_apppwd():

                    returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, source_cell.title, source_cell.description)

                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                    else:

                        messages.error(request, "WordPress Error - Contact System Administrator")

                source_cell.set_blogpost(post_id)


            source_cell.save()
            target_cell.save()

            data = { 'failure': False, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)

    else:

            data = { 'failure': True, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)
