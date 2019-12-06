\echo 'Berka(helpers)'
\echo 'Programación para Ciencia de Datos'
\echo 'Adolfo De Unánue <unanue@itam.mx>'
\set VERBOSITY terse
\set ON_ERROR_STOP true

do language plpgsql $$ declare
    exc_message text;
    exc_context text;
    exc_detail text;
begin
  raise notice 'adding extensions';
  raise notice 'creating functions';

exception when others then
    get stacked diagnostics exc_message = message_text;
    get stacked diagnostics exc_context = pg_exception_context;
    get stacked diagnostics exc_detail = pg_exception_detail;
    raise exception E'\n------\n%\n%\n------\n\nCONTEXT:\n%\n', exc_message, exc_detail, exc_context;
end $$;


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
