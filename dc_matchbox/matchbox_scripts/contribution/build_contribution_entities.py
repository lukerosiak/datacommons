
"""
Build the Entity table from the Contribution table. 

Transactions with identical organization_name belong to the same entity.
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from dcdata.contribution.models import sql_names


def get_recipient_type(types):
    if 'C' in types:
        return 'committee'
    return 'politician'

def get_contributor_type(types):
    if 'C' in types:
        return 'committee'    
    return 'individual'
    
    

def run():
    
    log("Building committee entities...")
    populate_entities(sql_names['contribution'],
                      sql_names['contribution_committee_entity'],
                      [sql_names['contribution_committee_name']],
                      sql_names['contribution_committee_ext_id'],
                      'committee')
    
    log("Building organization entities...")
    populate_entities(sql_names['contribution'], 
                      sql_names['contribution_organization_entity'],
                      [sql_names['contribution_organization_name'], sql_names['contribution_contributor_employer']],
                      sql_names['contribution_organization_ext_id'],
                      'organization')   
     
    log("Building parent organization entities...")
    populate_entities(sql_names['contribution'], 
                      sql_names['contribution_parent_organization_entity'],
                      [sql_names['contribution_parent_organization_name']],
                      sql_names['contribution_parent_organization_ext_id'],
                      'organization')
        
    log("Building recipient entities...")
    populate_entities(sql_names['contribution'],
                      sql_names['contribution_recipient_entity'],
                      [sql_names['contribution_recipient_name']],
                      sql_names['contribution_recipient_ext_id'],
                      get_recipient_type,
                      sql_names['contribution_recipient_type'])
    
    # we won't be including contribution entities
#    log("Building contributor entities...")
#    populate_entities(sql_names['contribution'],
#                      sql_names['contribution_contributor_entity'],
#                      sql_names['contribution_contributor_name'],
#                      sql_names['contribution_contributor_urn'],
#                      get_contributor_type,
#                      sql_names['contribution_contributor_type'])
    
    
    
from matchbox_scripts.support.build_entities import populate_entities
from matchbox_scripts.build_matchbox import log

    
if __name__ == '__main__':
    run()
    
    