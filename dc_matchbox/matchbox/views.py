

from django.http import HttpResponse
from django.template import Context, loader
from django import forms

from queries import search_entities_by_name, search_transactions_by_entity, transaction_result_columns


def transactions_page(request):
    template = loader.get_template('transactions.html')
                                           
    if request.GET['entity_id']:                                       
        results = search_transactions_by_entity(request.GET['entity_id'])
        
        context = Context()
        context['results'] = results
        context['headers'] = transaction_result_columns
        
        return HttpResponse(template.render(context))
    else:
        return HttpResponse("Error: request should include entity_id parameter.")
    
    
    
class EntitiesForm(forms.Form):    
    query = forms.CharField(max_length = 40)
        
def entities_page(request):
    template = loader.get_template('entities.html')
    context = Context()
    context['action'] = 'entities'
    context['search_form'] = EntitiesForm()

    if request.method == 'POST':
        search_form = EntitiesForm(request.POST)
        if search_form.is_valid():
            results = search_entities_by_name(search_form.cleaned_data['query'])
            
            context['search_form'] = search_form
            context['results'] = results
            context['headers'] = ['name', 'count']
            
            return HttpResponse(template.render(context))
        else:
            return HttpResponse("Error: invalid form data")
    else:
        return HttpResponse(template.render(context))
    
