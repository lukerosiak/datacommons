from django.db.models.query_utils import Q
from dcdata.utils.sql import parse_date
from dcdata.utils.strings.transformers import build_remove_substrings
from dcdata.lobbying.models import Lobbying
from dcapi.schema import Operator, Schema, InclusionField, OperatorField

LESS_THAN_OP = '<'
GREATER_THAN_OP = '>'
BETWEEN_OP = '><'

TRANSACTION_ID_FIELD = 'transaction_id'
TRANSACTION_TYPE_FIELD = 'transaction_type'

CLIENT_FT_FIELD = 'client_ft'
CLIENT_PARENT_FT_FIELD = 'client_parent_ft'
LOBBYIST_FT_FIELD = 'lobbyist_ft'
REGISTRANT_FT_FIELD = 'registrant_ft'

AMOUNT_FIELD = 'amount'
FILING_TYPE_FIELD = 'filing_type'
YEAR_FIELD = 'year'

# utility generators

def _ft_generator(query, column, *searches):
    return query.extra(where=[_ft_clause(column)], params=[_ft_terms(*searches)])

_strip_postgres_ft_operators = build_remove_substrings("&|!():*")

def _ft_terms(*searches):
    cleaned_searches = map(_strip_postgres_ft_operators, searches)
    return ' | '.join("(%s)" % ' & '.join(search.split()) for search in cleaned_searches)

def _ft_clause(column):
    return """to_tsvector('datacommons', %s) @@ to_tsquery('datacommons', %%s)""" % column

#
# generators

def _transaction_id_in_generator(query, *transaction_ids):
    return query.filter(transaction_id__in=transaction_ids)

def _transaction_type_in_generator(query, *transaction_types):
    return query.filter(transaction_type__in=transaction_types)

def _year_in_generator(query, *years):
    return query.filter(year__in=years)

def _filing_type_in_generator(query, *filing_types):
    return query.filter(filing_type__in=filing_types)

# amount generators
def _amount_less_than_generator(query, amount):
    return query.filter(amount__lte=int(amount))
    
def _amount_greater_than_generator(query, amount):
    return query.filter(amount__gte=int(amount))
    
def _amount_between_generator(query, lower, upper):
    return query.filter(amount__range=(int(lower), int(upper)))

# full text generators
def _client_ft_generator(query, *searches):
    return _ft_generator(query, 'client_name', *searches)

def _client_parent_ft_generator(query, *searches):
    return _ft_generator(query, 'client_parent_name', *searches)

def _lobbyist_ft_generator(query, *searches):
    return _ft_generator(query, 'lobbyist_name', *searches)

def _registrant_ft_generator(query, *searches):
    return _ft_generator(query, 'registrant_name', *searches)

    
LOBBYING_SCHEMA = Schema(
    InclusionField(TRANSACTION_ID_FIELD, _transaction_id_in_generator),
    InclusionField(TRANSACTION_TYPE_FIELD, _transaction_type_in_generator),
    InclusionField(FILING_TYPE_FIELD, _filing_type_in_generator),
    InclusionField(YEAR_FIELD, _year_in_generator),
    # full text fields
    InclusionField(CLIENT_FT_FIELD, _client_ft_generator),
    InclusionField(CLIENT_PARENT_FT_FIELD, _client_parent_ft_generator),
    InclusionField(LOBBYIST_FT_FIELD, _lobbyist_ft_generator),
    InclusionField(REGISTRANT_FT_FIELD, _registrant_ft_generator),
    # operator fields
    OperatorField(AMOUNT_FIELD,
        Operator(LESS_THAN_OP, _amount_less_than_generator),
        Operator(GREATER_THAN_OP, _amount_greater_than_generator),
        Operator(BETWEEN_OP, _amount_between_generator)))

def filter_lobbying(request):
    q = LOBBYING_SCHEMA.build_filter(Lobbying.objects, request).order_by()
    if 'lobbyist_ft' in request:
        q = q.filter(lobbyists__lobbyist_name__isnull=False)
    return q.select_related()