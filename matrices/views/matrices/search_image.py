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
# This file contains the search_image view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import SearchUrlForm

from matrices.routines import convert_url_omero_to_cpw
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection

HTTP_POST = 'POST'
NO_CREDENTIALS = ''
LIST_IMAGING_HOSTS = "list_imaging_hosts"
VIEW_ACTIVE_COLLECTION = "view_active_collection"
VIEW_ALL_COLLECTIONS = "view_all_collections"
VIEW_COLLECTION = "view_collection"


#
# Search for an Image
#
@login_required
def search_image(request, path_from, identifier):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        form = SearchUrlForm()

        if request.method == HTTP_POST:

            form = SearchUrlForm(request.POST)

            if form.is_valid():

                cd = form.cleaned_data

                url_string = cd.get('url_string')

                url_string_out = convert_url_omero_to_cpw(request, url_string)

                if url_string_out == "":

                    messages.error(request, "URL not found!")
                    form.add_error(None, "URL not found!")

                else:

                    return redirect(url_string_out)

            else:

                messages.error(request, "ERROR: Form is Invalid!")
                form.add_error(None, "ERROR: Form is Invalid!")

        else:

            form = SearchUrlForm()

        return_page = ''

        if path_from == LIST_IMAGING_HOSTS:

            data.update({ 'form': form, 'search_from': "list_imaging_hosts" })

            return_page = 'host/list_imaging_hosts.html'


        if path_from == VIEW_ACTIVE_COLLECTION:

            collection_list = get_active_collection_for_user(request.user)
            collection = collection_list[0]
            collection_image_list = get_images_for_collection(collection)

            data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_active_collection" })

            return_page = 'matrices/view_collection.html'


        if path_from == VIEW_ALL_COLLECTIONS:

            data.update({ 'form': form, 'search_from': "view_all_collections" })

            return_page = 'matrices/view_all_collections.html'


        if path_from == VIEW_COLLECTION:

            collection = get_object_or_404(Collection, pk=identifier)
            collection_image_list = get_images_for_collection(collection)

            data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_collection" })

            return_page = 'matrices/view_collection.html'


        return render(request, return_page, data)
