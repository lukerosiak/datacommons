from dcapi.common.handlers import FilterHandler
from dcapi.common.schema import InclusionField, FulltextField, ComparisonField
from dcapi.schema import Schema
from dcdata.contracts.models import Contract

CONTRACTS_SCHEMA = Schema(
    InclusionField('agency_id', 'agencyid'),
    InclusionField('contracting_agency_id', 'contractingofficeagencyid'),
    InclusionField('fiscal_year'),
    InclusionField('place_distrct', 'congressionaldistrict'),
    InclusionField('place_state', 'statecode'),
    InclusionField('requesting_agency_id', 'fundingrequestingagencyid'),
    InclusionField('vendor_state', 'state'),
    InclusionField('vendor_zipcode', 'zipcode'),
    InclusionField('vendor_district', 'vendor_cd'),
    InclusionField('vendor_duns', 'dunsnumber'),
    InclusionField('vendor_parent_duns', 'eeparentduns'),

    FulltextField('agency_name'),
    FulltextField('contracting_agency_name'),
    FulltextField('requesting_agency_name'),
    FulltextField('vendor_name', ['vendorname']),
    FulltextField('vendor_city', ['city']),

    ComparisonField('obligated_amount', 'obligatedamount', cast=int),
    ComparisonField('current_amount', 'baseandexercisedoptionsvalue', cast=int),
    ComparisonField('maximum_amount', 'baseandalloptionsvalue', cast=int)
)


def filter_contracts(request):
    return CONTRACTS_SCHEMA.build_filter(Contract.objects, request).order_by()


class ContractsFilterHandler(FilterHandler):
    model = Contract
    ordering = ['-fiscal_year','-baseandexercisedoptionsvalue']
    filename = 'contracts'
        
    def queryset(self, params):
        return filter_contracts(self._unquote(params))
    
