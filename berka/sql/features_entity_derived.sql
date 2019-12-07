create schema if not exists features;

drop table if exists features.entity_derived;

create table if not exists features.entity_derived as (
select * from
(
  select
    as_of_date,
    client
    from
        labels.loan_granted_3m
) as aod
             left join lateral ( -- for loop
               select
                 extract(year from age(as_of_date, bod)) as age
                 , extract(month from age(as_of_date, since)) as antiquity
                 from semantic.entities
                where aod.client = client
             ) as t2
                 on true
);
