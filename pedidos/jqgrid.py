import operator
from django.db import models
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.db.models.query import ValuesQuerySet
from django.utils.encoding import smart_str
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404

def serialize(items, fields):
    json = []
    for item in items:
        i = {}
        for field in fields:
            if '__' in field:
                fk_name, field_name = field.split('__', 1)
                i[field] = item.__getattribute__(fk_name).__getattribute__(field_name)
            else:
                i[field] = item.__getattribute__(field)
        json.append(i)
    return json

def json_encode(data):
    encoder = DjangoJSONEncoder()
    return encoder.encode(data)

def get_items(request, items):
    items = filter_items(request, items)
    items = sort_items(request, items)
    paginator, page, items = paginate_items(request, items)
    return (paginator, page, items)

def get_filters(request):
    _search = request.GET.get('_search')
    filters = None

    if _search == 'true':
        _filters = request.GET.get('filters')
        try:
            filters = _filters and json.loads(_filters)
        except ValueError:
            return None

        if filters is None:
            field = request.GET.get('searchField')
            op = request.GET.get('searchOper')
            data = request.GET.get('searchString')

            if all([field, op, data]):
                filters = {
                    'groupOp': 'AND',
                    'rules': [{'op': op, 'field': field, 'data': data}]
                }
    return filters

def filter_items(request, items):
    filter_map = {
        'ne': ('%(field)s__exact', True),
        'bn': ('%(field)s__startswith', True),
        'en': ('%(field)s__endswith', True),
        'nc': ('%(field)s__contains', True),
        'ni': ('%(field)s__in', True),
        'in': ('%(field)s__in', False),
        'eq': ('%(field)s__exact', False),
        'bw': ('%(field)s__startswith', False),
        'gt': ('%(field)s__gt', False),
        'ge': ('%(field)s__gte', False),
        'lt': ('%(field)s__lt', False),
        'le': ('%(field)s__lte', False),
        'ew': ('%(field)s__endswith', False),
        'cn': ('%(field)s__contains', False)
    }
    _filters = get_filters(request)
    if _filters is None:
        return items

    q_filters = []
    for rule in _filters['rules']:
        op, field, data = rule['op'], rule['field'], rule['data']
        filter_fmt, exclude = filter_map[op]
        filter_str = smart_str(filter_fmt % {'field': field})
        if filter_fmt.endswith('__in'):
            d_split = data.split(',')
            filter_kwargs = {filter_str: data.split(',')}
        else:
            filter_kwargs = {filter_str: smart_str(data)}

        if exclude:
            q_filters.append(~models.Q(**filter_kwargs))
        else:
            q_filters.append(models.Q(**filter_kwargs))

    if _filters['groupOp'].upper() == 'OR':
        filters = reduce(operator.ior, q_filters)
    else:
        filters = reduce(operator.iand, q_filters)
    return items.filter(filters)

def get_sort_key(i, sidx):
    if '__' in sidx:
        fk_name, field_name = sidx.split('__', 1)
        return i.__getattribute__(fk_name).__getattribute__(field_name)
    else:
        return i.__getattribute__(sidx)

def sort_items(request, items):
    sidx = request.GET.get('sidx')
    if sidx is not None:
        sord = request.GET.get('sord')
        if sord == 'desc':
            items = sorted(items, key=lambda i: get_sort_key(i, sidx), reverse=True)
        else:
            items = sorted(items, key=lambda i: get_sort_key(i, sidx), reverse=False)
    return items

def get_paginate_by(request):
    rows = request.GET.get('rows', 10)
    try:
        paginate_by = int(rows)
    except ValueError:
        paginate_by = 10
    return paginate_by

def paginate_items(request, items):
    paginate_by = get_paginate_by(request)
    if not paginate_by:
        return (None, None, items)

    paginator = Paginator(items, paginate_by,
        allow_empty_first_page=False)
    page = request.GET.get('page', 1)

    try:
        page_number = int(page)
        page = paginator.page(page_number)
    except (ValueError, InvalidPage):
        page = paginator.page(1)
    return (paginator, page, page.object_list)

def get_json(request, items, fields):
    paginator, page, items = get_items(request, items)
    data = {
        'page': int(page.number),
        'total': int(paginator.num_pages),
        'rows': serialize(items, fields),
        'records': int(paginator.count),
        }
    return json_encode(data)

def get_default_config():
    config = {
        'datatype': 'json',
        'autowidth': True,
        'forcefit': True,
        'shrinkToFit': True,
        'jsonReader': {'repeatitems': False},
        'rowNum': 10,
        'rowList': [10, 25, 50, 100],
        'sortname': 'id',
        'viewrecords': True,
        'sortorder': "asc",
        'pager': '#pager',
        'altRows': True,
        'gridview': True,
        'height': 'auto',
    }
    return config

def get_config(items, url, fields=None, as_json=True):
    config = get_default_config()
    config.update({
        'url': reverse(url),
        'colModel': get_colmodels(fields, items.model),
        })
    if as_json:
        config = json_encode(config)
    return config

def lookup_foreign_key_field(options, field_name):
    if '__' in field_name:
        fk_name, field_name = field_name.split('__', 1)
        fields = [f for f in options.fields if f.name == fk_name]
        if len(fields) > 0:
            field_class = fields[0]
        else:
            raise FieldError('No field %s in %s' % (fk_name, options))
        foreign_model_options = field_class.rel.to._meta
        return lookup_foreign_key_field(foreign_model_options, field_name)
    else:
        try:
            return options.get_field_by_name(field_name)
        except:
            return (field_name.replace('_', ' '), None, None, None)

def get_colmodels(fields, model):
    colmodels = []
    opts = model._meta
    for field_name in get_field_names(model, fields):
        (field, model, direct, m2m) = lookup_foreign_key_field(opts, field_name)
        colmodel = field_to_colmodel(field, field_name)
        colmodels.append(colmodel)
    return colmodels

def get_field_names(model, fields):
    if not fields:
        fields = [f.name for f in model._meta.local_fields]
    return fields

def field_to_colmodel(field, field_name):
    try:
        colmodel = {
            'name': field_name,
            'index': field_name,
            'label': field.name,
            'editable': True if field_name == 'quantidade' else False,
        }
        if 'Decimal' in str(field.__class__) or field_name == 'valor_total':
            colmodel['formatter'] = 'currency'
            colmodel['formatoptions'] =  {'prefix':'R$ ', 'thousandsSeparator':'.', 'decimalSeparator':','}
    except:
        colmodel = {
            'name': field_name,
            'index': field_name,
            'label': field,
            'editable': True if field_name == 'quantidade' else False,
            'formatter': 'currency' if 'Decimal' in str(field.__class__) else 'default'
        }
        if 'Decimal' in str(field.__class__) or field_name == 'valor_total':
            colmodel['formatter'] = 'currency'
            colmodel['formatoptions'] =  {'prefix':'R$', 'thousandsSeparator':'.', 'decimalSeparator':','}
    return colmodel