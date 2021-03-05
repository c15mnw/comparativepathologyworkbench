from __future__ import unicode_literals

from django import forms

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from sortable_listview import SortableListView


from matrices.models import MatrixSummary
from matrices.forms import MatrixSummarySearchForm

from matrices.routines import get_header_data
from matrices.routines import bench_list_by_user_and_direction


class MatrixListView(LoginRequiredMixin, SortableListView):

    query_title = forms.CharField(max_length=25)
    query_description = forms.CharField(max_length=25)
    query_created_after = forms.DateTimeField()
    query_created_before = forms.DateTimeField()
    query_modified_after = forms.DateTimeField()
    query_modified_before = forms.DateTimeField()
    query_owner = forms.CharField(max_length=10)
    query_authority = forms.CharField(max_length=12)

    allowed_sort_fields = {'matrix_id': {'default_direction': '', 'verbose_name': 'Bench Id'},
                           'matrix_title': {'default_direction': '', 'verbose_name': 'Title'},
                           'matrix_created': {'default_direction': '', 'verbose_name': 'Created On'},
                           'matrix_modified': {'default_direction': '', 'verbose_name': 'Updated On'},
                           'matrix_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'matrix_authorisation_authority': {'default_direction': '', 'verbose_name': 'Authority'}
                           }


    default_sort_field = 'matrix_id'

    paginate_by = 10

    template_name = 'host/list_benches.html'

    model = MatrixSummary

    context_object_name = 'matrix_summary_list'


    def get_queryset(self):

        sort_parameter = ''

        if self.request.GET.get('sort', None) == None:

            sort_parameter = 'matrix_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        self.query_title = self.request.GET.get('title', '')
        self.query_description = self.request.GET.get('description', '')
        self.query_owner = self.request.GET.get('owner', '')
        self.query_authority = self.request.GET.get('authority', '')
        self.query_created_before = self.request.GET.get('created_before', '')
        self.query_created_after = self.request.GET.get('created_after', '')
        self.query_modified_before = self.request.GET.get('modified_before', '')
        self.query_modified_after = self.request.GET.get('modified_after', '')

        return bench_list_by_user_and_direction(self.request.user, sort_parameter, self.query_title, self.query_description, self.query_owner, self.query_authority, self.query_created_after, self.query_created_before, self.query_modified_after, self.query_modified_before)


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        data_dict = {'title': self.query_title, 'description': self.query_description, 'created_before': self.query_created_before, 'created_after': self.query_created_after, 'modified_before': self.query_modified_before, 'modified_after': self.query_modified_after, 'owner': self.query_owner, 'authority': self.query_authority }

        form = MatrixSummarySearchForm(data_dict)

        data.update({ 'form': form,  })

        context.update(data)

        return context
