drop schema if exists cohorts;
create schema if not exists cohorts;

drop table if exists cohorts.new_clients;
create table if not exists cohorts.new_clients as (
with as_of_dates as (
  select
    generate_series(min(date), max(date), '6 month') as as_of_date
    from
        semantic.events
),

  new_clients as (
    select
      client,
      gender,
      bod,
      district,
      since,
      aod.as_of_date::date,
      daterange(
        (aod.as_of_date - interval '1 year')::date,
        aod.as_of_date::date)
        @> since as "new?"
      from  (
        select
          as_of_date
          from
              as_of_dates
      ) as aod
              left join lateral (
                select *, age(since, as_of_date)
                  from semantic.entities
              ) as t2 on true
  )

select
  -- as_of_date, count(*)
  *
  from
      new_clients
 where "new?" is true
 -- group by 1
)
