from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Q 


"""
    Get All Benches for All Users except for a particular User
"""
def bench_list_not_by_user(a_user):

    Matrix = apps.get_model('matrices', 'Matrix')

    queryset = Matrix.objects.filter(~Q(owner=a_user)).order_by('id')
    
    matrices = list()
    
    for matrix in queryset:
    
        out_matrix = ({
            'matrix_id': matrix.id, 
            'matrix_title': matrix.title, 
            'matrix_description': matrix.description, 
            'matrix_blogpost': matrix.blogpost, 
            'matrix_created': matrix.created, 
            'matrix_modified': matrix.modified, 
            'matrix_height': matrix.height, 
            'matrix_width': matrix.width, 
            'matrix_owner': matrix.owner.username,
            'authorisation_id': "0", 
            'authorisation_authority': "ADMIN",
            'authorisation_permitted': matrix.owner.username
        })

        matrices.append(out_matrix)
    
    return matrices

