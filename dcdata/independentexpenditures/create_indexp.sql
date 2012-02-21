
drop table if exists fec_indexp_import;
create table fec_indexp_import (
    candidate_id varchar(9),
    candidate_name varchar(90),
    spender_id varchar(9),
    spender_name varchar(90),
    election_type varchar(5),
    candidate_state varchar(2),
    candidate_district varchar(2),
    candidate_office varchar(9),
    candidate_party varchar(32),
    amount varchar(15),
    date date,
    aggregate_amount varchar(15),
    support_oppose varchar(9),
    purpose varchar(100),
    payee varchar(90),
    filing_number varchar(6),
    amendment varchar(2),
    transaction_id varchar(32),
    image_number varchar(11),
    received_date date
);


-- manual fixes...not sure how to best package these if there are more in the future
update fec_indexp_import
set candidate_id = 'P60003654'
where
    candidate_id = 'P80003353'
    and spender_id = 'C00507525'
    and support_oppose = 'Support';


update fec_indexp_import
set candidate_id = manual_fixes.id
from (values
    ('barack obama, ', 'P80003338'),
    ('barak obama, ', 'P80003338'), 
    ('bonamici, suzanne', 'H2OR01133'),
    ('boucher, rick', 'H2VA09010'),
    ('canseco, francisco raul quico', 'H4TX28046'),
    ('cornilles, robert', 'H0OR01095'),
    ('corwin, jane', 'H2NY00044'),
    ('davis, jack', 'H4NY26045'),
    ('gingrich, newt', 'P60003654'),
    ('hahn, janice', 'H8CA36097'),
    ('hatch, orrin', 'S6UT00063'),
    ('hochul, kathleen', 'H2NY00036'),
    ('hochul, kathy', 'H2NY00036'),
    ('huntsman, jon', 'P20003067'),
    ('marshall, kate', 'H2NV02247'),
    ('newt, gingrich', 'P60003654'),
    ('obama, barack', 'P80003338'),
    ('paul, ron', 'P80000748'),
    ('perry, rick', 'P20003281'),
    ('rahall, nick', 'H6WV04057'),
    ('romne, mitt', 'P80003353'),
    ('romney, mitt', 'P80003353'),
    ('ron, p', 'P80000748'),
    ('ron, paul', 'P80000748'),
    ('santorum, richard', 'P20002721'),
    ('santorum, rick', 'P20002721'),
    ('thompson, tommy', 'S2WI00235'),
    ('turner, bob', 'H0NY09072')
) manual_fixes (name, id)
where
    lower(candidate_name) = manual_fixes.name
    and length(candidate_id) < 9;
    
    
-- just here to trigger errors if something is wrong with the data
alter table fec_indexp_import add constraint fec_indexp_import_transactions unique (spender_id, filing_number, transaction_id);
alter table fec_indexp_import add constraint fec_indexp_import_ids check (length(candidate_id) = 9);
-- is there some way to add a constraint that for each lower(candidate_name) there should be only a single candidate_id?


drop table fec_indexp_amendments;
create table fec_indexp_amendments as
with filings as (
    select distinct spender_id, filing_number, case when amendment = 'N' then 0 else substring(amendment from 2 for 1)::integer end as amendment_number
    from fec_indexp_import)
select a.spender_id, a.filing_number as original_filing, a.amendment_number, b.filing_number as amendment_filing, b.amendment_number as amendment_number2
from filings a
inner join filings b using (spender_id)
where
    a.amendment_number < b.amendment_number
    and exists (
        select *
        from fec_indexp_import x
        inner join fec_indexp_import y using (spender_id, transaction_id)
        where
            x.filing_number = a.filing_number
            and y.filing_number = b.filing_number);


drop table if exists fec_indexp;
create table fec_indexp as
select candidate_id, candidate_name, spender_id, spender_name, election_type, candidate_state,
    case when candidate_office = 'House' then candidate_district else '' end as candidate_district,
    candidate_office, candidate_party, 
    regexp_replace(amount, ',|\$', '', 'g')::numeric as amount,
    regexp_replace(aggregate_amount, ',|\$', '', 'g')::numeric as aggregate_amount,
    support_oppose, purpose, payee, filing_number, amendment, transaction_id, image_number, received_date
from fec_indexp_import i
where
    not exists (select * from fec_indexp_amendments a where i.spender_id = a.spender_id and i.filing_number = a.original_filing);

