#!/usr/bin/python3
###!
# \file         views_permissions.py
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
# This file contains the new_collection_collection_authorisation view routine
###
from __future__ import unicode_literals

import os
import time
import requests

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
from django.db.models import Q

from decouple import config

from matrices.forms import AuthorisationForm
from matrices.forms import CollectionAuthorisationForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Server
from matrices.models import Command
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential
from matrices.models import Collection
from matrices.models import Authority
from matrices.models import CollectionAuthority
from matrices.models import Authorisation
from matrices.models import CollectionAuthorisation

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines import authorisation_exists_for_bench_and_permitted
from matrices.routines import credential_exists
from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# CREATE A NEW COLLECTION AUTHORISATION FOR A GIVEN COLLECTION
#
@login_required
def new_collection_collection_authorisation(request, collection_id):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:

        next_page = request.POST.get('next', '/')

        form = CollectionAuthorisationForm(request.POST)

        if form.is_valid:

            collection_authorisation = form.save(commit=False)

            collection_authorisation.set_collection_authority(form.cleaned_data['authority'])

            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):

                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))

                if collection_authorisation_old.collection_authority != collection_authorisation.collection_authority:

                    collection_authorisation_old.collection_authority = collection_authorisation.collection_authority

                    collection_authorisation_old.save()

            else:

                collection_authorisation.save()

            return HttpResponseRedirect(next_page)

        else:

            messages.error(request, "Error")

            text_flag = " for Collection: " + format(int(collection_id), '06d')

            data.update({ 'text_flag': text_flag, 'form': form })

    else:

        text_flag = " for Collection: " + format(int(collection_id), '06d')

        form = CollectionAuthorisationForm()

        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))
        form.fields['collection'].initial = collection_id

        form.fields['authority'] = forms.ModelChoiceField(CollectionAuthority.objects.all())

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_collection_authorisation.html', data)
