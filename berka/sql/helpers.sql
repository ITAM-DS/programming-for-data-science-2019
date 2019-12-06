create or replace function fix_date
  (
    bad_date text
  )
returns date
language sql
as $$
select to_date(format('19%s', bad_date), 'YYYYMMDD') as date_fixed;
$$;

create or replace function fix_int
  (
    bad_number text
  )
returns integer
language sql
as $$
select case when btrim(bad_number) = '?' then NULL::integer
else bad_number::integer end as int_fixed;
$$;

create or replace function fix_numeric
  (
    bad_number text
  )
returns numeric(10,2)
language sql
as $$
select case when btrim(bad_number) = '?' then NULL::numeric(10,2)
else bad_number::numeric(10,2) end as numeric_fixed;
$$;
