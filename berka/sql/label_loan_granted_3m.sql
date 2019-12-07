create schema if not exists labels;

drop table if exists labels.loan_granted_3m;
create table if not exists labels.loan_granted_3m as (

with outcomes as (
  select
    as_of_date,
    client,
    date as event_date,
    type = 'loan granted' as outcome
    from
        cohorts.new_clients
        left join semantic.events using(client)
)

select
  as_of_date
  , client
-- , array_agg(event_date::date order by event_date asc) as event_dates
-- , array_agg(outcome order by event_date asc) as outcomes
  , bool_or(outcome)::integer as label
  from outcomes
 where
daterange(as_of_date::date,(as_of_date + interval '3 months')::date) @>  event_date
--and as_of_date = '1994-01-01'
 group by as_of_date, client
);

create index  labels_loan_granted_3m_client_ix on labels.loan_granted_3m(client);
create index  labels_loan_granted_3m_as_of_date_ix on labels.loan_granted_3m(as_of_date);
create index  labels_loan_granted_3m_client_as_of_date_ix on labels.loan_granted_3m(client, as_of_date);
