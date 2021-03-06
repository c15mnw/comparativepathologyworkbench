#!/usr/bin/python3
###!
# \file         views_matrices.py
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
# This file contains the view_cell_blog view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import CommentForm

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import get_header_data
from matrices.routines import get_primary_wordpress_server

HTTP_POST = 'POST'
NO_CREDENTIALS = ''
WORDPRESS_SUCCESS = 'Success!'

#
# VIEW THE CELL BLOG ENTRY
#
@login_required
def view_cell_blog(request, matrix_id, cell_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        cell = get_object_or_404(Cell, pk=cell_id)

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        blogpost = serverWordpress.get_wordpress_post(cell.blogpost)

        if blogpost['status'] != WORDPRESS_SUCCESS:

            messages.error(request, "WordPress Error - Contact System Administrator")

        comment_list = list()

        comment_list = serverWordpress.get_wordpress_post_comments(cell.blogpost)

        for comment in comment_list:

            if comment['status'] != WORDPRESS_SUCCESS:

                messages.error(request, "WordPress Error - Contact System Administrator")

        if request.method == HTTP_POST:

            form = CommentForm(request.POST)

            if form.is_valid():

                cd = form.cleaned_data

                comment = cd.get('comment')

                if comment != '':

                    returned_comment = serverWordpress.post_wordpress_comment(request.user.username, cell.blogpost, comment)

                    if returned_comment['status'] != WORDPRESS_SUCCESS:

                        messages.error(request, "WordPress Error - Contact System Administrator")

                return HttpResponseRedirect(reverse('view_cell_blog', args=(matrix_id, cell_id)))

            else:

                messages.error(request, "Error")

        else:

            form = CommentForm()

        data.update({ 'form': form, 'matrix_id': matrix_id, 'cell': cell, 'matrix': matrix, 'blogpost': blogpost, 'comment_list': comment_list })

        return render(request, 'matrices/detail_cell_blog.html', data)
