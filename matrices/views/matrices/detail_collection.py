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
# This file contains the detail_collection view routine
#
###
from __future__ import unicode_literals

import os
import time
import requests
import re

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string

from decouple import config

from matrices.forms import MatrixForm
from matrices.forms import NewMatrixForm
from matrices.forms import CellForm
from matrices.forms import HeaderForm
from matrices.forms import CommentForm
from matrices.forms import CollectionForm
from matrices.forms import SearchUrlForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Collection

from matrices.routines import AESCipher
from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_image_in_cells
from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import exists_collections_for_image
from matrices.routines import get_active_collection_for_user
from matrices.routines import set_first_active_collection_for_user
from matrices.routines import set_inactive_collection_for_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import get_benches_for_last_used_collection
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_blog_link_post_url
from matrices.routines import get_active_collection_images_for_user
from matrices.routines import get_collections_for_image
from matrices.routines import convert_url_omero_to_cpw

WORDPRESS_SUCCESS = 'Success!'

HTTP_POST = 'POST'

NO_CREDENTIALS = ''

#
# VIEW AN IMAGE COLLECTION DETAILS
#
@login_required
def detail_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        data.update({ 'collection_id': collection_id, 'collection': collection })

        return render(request, 'matrices/detail_collection.html', data)
