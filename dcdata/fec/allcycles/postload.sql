

create view fec_candidates_allcycles_import as
    select 2012 as cycle, * from fec_candidates_12
union all
    select 2010, * from fec_candidates_10
union all
    select 2008, * from fec_candidates_08
union all
    select 2006, * from fec_candidates_06
union all
    select 2004, * from fec_candidates_04
union all
    select 2002, * from fec_candidates_02
union all
    select 2000, * from fec_candidates_00;

drop table if exists fec_candidates_allcycles;
create table fec_candidates_allcycles as
select *,
    case
        when substring(candidate_id for 1) = 'P' then 'P'
        when substring(candidate_id for 1) = 'S' then 'S' || '-' || substring(candidate_id from 3 for 2)
        when substring(candidate_id for 1) = 'H' then 'H' || '-' || substring(candidate_id from 3 for 2) || '-' || current_district
    end as race
from fec_candidates_allcycles_import;

create index fec_candidates_allcycles_candidate_id on fec_candidates_allcycles (candidate_id);


create view fec_committees_allcycles as
    select 2012 as cycle, * from fec_committees_12
union all
    select 2010, * from fec_committees_10
union all
    select 2008, * from fec_committees_08
union all
    select 2006, * from fec_committees_06
union all
    select 2004, * from fec_committees_04
union all
    select 2002, * from fec_committees_02
union all
    select 2000, * from fec_committees_00;


create view fec_indiv_allcycles_import as
    select 2012 as cycle, * from fec_indiv_12
union all
    select 2010, * from fec_indiv_10
union all
    select 2008, * from fec_indiv_08
union all
    select 2006, * from fec_indiv_06
union all
    select 2004, * from fec_indiv_04
union all
    select 2002, * from fec_indiv_02
union all
    select 2000, * from fec_indiv_00;

drop table if exists fec_indiv_allcycles;
create table fec_indiv_allcycles as
    select
        cycle,
        filer_id,
        amendment,
        report_type,
        election_type,
        microfilm_location,
        lower(transaction_type) as transaction_type,
        entity_type,
        contributor_name,
        city,
        state,
        zipcode,
        employer,
        occupation,
        (substring(date for 4 from 5) || substring(date for 2) || substring(date for 2 from 3))::date as date,
        case when transaction_type = '22Y' then -abs(amount) else amount end as amount,
        other_id,
        transaction_id,
        file_num,
        memo_code,
        memo_text,
        fec_record
from fec_indiv_allcycles_import;
create index fec_indiv_allcycles_filer_id on fec_indiv_allcycles (filer_id);


create view fec_pac2cand_allcycles_import as
    select 2012 as cycle, * from fec_pac2cand_12
union all
    select 2010, * from fec_pac2cand_10
union all
    select 2008, * from fec_pac2cand_08
union all
    select 2006, * from fec_pac2cand_06
union all
    select 2004, * from fec_pac2cand_04
union all
    select 2002, * from fec_pac2cand_02
union all
    select 2000, * from fec_pac2cand_00;

drop table if exists fec_pac2cand_allcycles;
create table fec_pac2cand_allcycles as
    select
        cycle,
        filer_id,
        amendment,
        report_type,
        election_type,
        microfilm_location,
        lower(transaction_type) as transaction_type,
        entity_type,
        contributor_name,
        city,
        state,
        zipcode,
        employer,
        occupation,
        (substring(date for 4 from 5) || substring(date for 2) || substring(date for 2 from 3))::date as date,
        case when transaction_type = '22Y' then -abs(amount) else amount end as amount,
        other_id,
        candidate_id,
        transaction_id,
        file_num,
        memo_code,
        memo_text,
        fec_record
from fec_pac2cand_allcycles_import;

create index fec_pac2cand_allcycles_filer_id on fec_pac2cand_allcycles (filer_id);
create index fec_pac2cand_allcycles_other_id on fec_pac2cand_allcycles (other_id);
create index fec_pac2cand_allcycles_candidate_id on fec_pac2cand_allcycles (candidate_id);
    

create view fec_pac2pac_allcycles_import as
    select 2012 as cycle, * from fec_pac2pac_12
union all
    select 2010, * from fec_pac2pac_10
union all
    select 2008, * from fec_pac2pac_08
union all
    select 2006, * from fec_pac2pac_06
union all
    select 2004, * from fec_pac2pac_04
union all
    select 2002, * from fec_pac2pac_02
union all
    select 2000, * from fec_pac2pac_00;

drop table if exists fec_pac2pac_allcycles;
create table fec_pac2pac_allcycles as
select
    cycle,
    filer_id,
    amendment,
    report_type,
    election_type,
    microfilm_location,
    lower(transaction_type) as transaction_type,
    entity_type,
    contributor_name,
    city,
    state,
    zipcode,
    employer,
    occupation,
    (substring(date for 4 from 5) || substring(date for 2) || substring(date for 2 from 3))::date as date,
    case when transaction_type = '22Y' then -abs(amount) else amount end as amount,
    other_id,
    transaction_id,
    file_num,
    memo_code,
    memo_text,
    fec_record
from fec_pac2pac_allcycles_import;

create index fec_pac2pac_allcycles_filer_id on fec_pac2pac_allcycles (filer_id);
create index fec_pac2pac_allcycles_other_id on fec_pac2pac_allcycles (other_id);


create view fec_committee_summaries_allcycles_import as
    select 2012 as cycle, * from fec_committee_summaries_12
    union all
    select 2010, * from fec_committee_summaries_10
    union all 
    select 2008, * from fec_committee_summaries_08
    union all 
    select 2006, * from fec_committee_summaries_06
    union all 
    select 2004, * from fec_committee_summaries_04
    union all 
    select 2002, * from fec_committee_summaries_02
    union all 
    select 2000, * from fec_committee_summaries_00;
    
drop table if exists fec_committee_summaries_allcycles;
create table fec_committee_summaries_allcycles as
    select cycle, committee_id, committee_name, committee_type, committee_designation, filing_frequency,
        (through_year || through_month || through_day)::date as through_date,
        total_receipts, transfers_from_affiliates, individual_contributions,
        contributions_from_other_committees,
        total_loans_received, total_disbursements, transfers_to_affiliates,
        refunds_to_individuals, refunds_to_committees,
        loan_repayments, cash_beginning_of_year, cash_close_of_period,
        debts_owed, nonfederal_transfers_received, contributions_to_committees,
        independent_expenditures_made, party_coordinated_expenditures_made, nonfederal_expenditure_share
    from fec_committee_summaries_allcycles_import
    where
        -- there are a number of data-less rows. Discard them by looking for valid date.
        through_year != 0;
create index fec_committee_summaries_allcycles_committee_id on fec_committee_summaries_allcycles (committee_id);


create view fec_candidate_summaries_allcycles_import as
    select 2012 as cycle, * from fec_candidate_summaries_12
    union all
    select 2010, * from fec_candidate_summaries_10
    union all 
    select 2008, * from fec_candidate_summaries_08
    union all 
    select 2006, * from fec_candidate_summaries_06
    union all 
    select 2004, * from fec_candidate_summaries_04
    union all 
    select 2002, * from fec_candidate_summaries_02
    union all 
    select 2000, * from fec_candidate_summaries_00;

drop table if exists fec_candidate_summaries_allcycles;
create table fec_candidate_summaries_allcycles as
select cycle, candidate_id, total_receipts, ending_cash, total_disbursements,
    candidate_loan_repayments, other_loan_repayments, refunds_to_individuals, refunds_to_committees,
    contributions_from_other_committees, contributions_from_party_committees,
    contributions_from_candidate, loans_from_candidate,
    authorized_transfers_from, total_individual_contributions,
    (substring(ending_date for 4 from 5) || substring(ending_date for 2 from 1) || substring(ending_date for 2 from 3))::date as ending_date
from fec_candidate_summaries_allcycles_import;

