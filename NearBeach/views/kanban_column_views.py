from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.views.tools.internal_functions import *
from django.db.models import Max
from NearBeach.decorators.check_user_permissions import check_user_permissions, check_user_kanban_permissions
from NearBeach.forms import NewColumnForm, DeleteColumnForm
import json, urllib3


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
#@check_user_permissions(min_permission_level=2, object_lookup='kanban_board_id')
def edit_column(request, kanban_column_id, *args, **kwargs):
    """
    """
    # Get form data
    form = NewColumnForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the kanban_column
    kanban_column_update = kanban_column.objects.get(kanban_column_id=kanban_column_id)

    # Update data
    kanban_column_update.kanban_column_name = form.cleaned_data['kanban_column_name']
    kanban_column_update.kanban_column_sort_number = form.cleaned_data['kanban_column_sort_number']

    # Save
    kanban_column_update.save()
    
    # Return data
    return HttpResponse(serializers.serialize('json', [kanban_column_update]), content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
#@check_user_permissions(min_permission_level=4, object_lookup='kanban_board_id')
def delete_column(request, *args, **kwargs):
    """
    """
    # Get the form data
    form = DeleteColumnForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the variables
    kanban_card.objects.filter(
        is_deleted=False,
        kanban_column_id=form.cleaned_data['delete_item_id'],
    ).update(
        kanban_column_id=form.cleaned_data['destination_item_id']
    )

    # Soft delete the old column
    deleted_column = kanban_column.objects.get(
        kanban_column_id=form.cleaned_data['delete_item_id'].kanban_column_id,
    )
    deleted_column.is_deleted=True
    deleted_column.save()

    return HttpResponse("");


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
@check_user_permissions(min_permission_level=3, object_lookup='kanban_board_id')
def new_column(request, kanban_board_id, *args, **kwargs):
    """
    """
    # Get data from form
    form = NewColumnForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create a new column
    kanban_column_submit = kanban_column(
        kanban_column_name=form.cleaned_data['kanban_column_name'],
        kanban_board_id=kanban_board_id,
        kanban_column_sort_number=form.cleaned_data['kanban_column_sort_number'],
        change_user=request.user,
    )
    kanban_column_submit.save()

    # Get the information and return as json results
    kanban_column_results = kanban_column.objects.filter(
        kanban_column_id = kanban_column_submit.kanban_column_id,
    )
     
    return HttpResponse(serializers.serialize('json',[kanban_column_submit]), content_type='application/json')
