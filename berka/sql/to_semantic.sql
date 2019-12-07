\echo 'Berka(semantic)'
\echo 'Programación para Ciencia de Datos'
\echo 'Adolfo De Unánue <unanue@itam.mx>'
\set VERBOSITY terse
\set ON_ERROR_STOP true

do language plpgsql $$ declare
    exc_message text;
    exc_context text;
    exc_detail text;
begin

  do $semantic$ begin

  set search_path = semantic, public;

  raise notice 'populating entities';
  drop table if exists entities;
  
  create table if not exists entities as (
    select
      client,
      gender,
      bod,
      clients.district,
      first_value(date)
        over (partition by client, account order by date asc) as since
      from
          cleaned.clients
          left join cleaned.dispositions using(client)
          left join cleaned.accounts using(account)
  );
  
  create index semantic_entities_client_ix on semantic.entities(client);
  create index semantic_entities_since_ix on semantic.entities(since);
  create index semantic_entities_bod_ix on semantic.entities(bod);

  raise notice 'defining event types';
  drop type if exists event_type cascade;
              create type event_type as enum (
                'open account',  'loan granted', 'card issued',
                'loan payment', 'old-age pension',
                'insurance payment', 'interest credited',
                'payment for statement', 'household', 'credit in cash',
                'collection from another bank', 'credit card withdrawal',
                'remittance to another bank', 'withdrawal in cash');
  
  raise notice 'defining events schema';
  drop table if exists events;
  create table if not exists events (
    event serial,
    client integer,
    account integer,
    type event_type,
    date date,
    attributes jsonb
  );
  
  raise notice 'populating events';
  insert into events (client, account, type, date)
              (
                select
                  client,
                  account,
                  'open account'::event_type,
                  date
                  from cleaned.accounts
                         inner join cleaned.dispositions using(account)
              )
              union
              (
                select
                  client,
                  account,
                  'loan granted'::event_type,
                  date
                  from cleaned.loans
                         inner join cleaned.dispositions using(account)
              )
              union
              (
                select
                  client,
                  account,
                  'card issued'::event_type,
                  issued as date
                  from  cleaned.credit_cards
                          inner join cleaned.dispositions using(disposition)
              )
              union
              (
                select
                  client,
                  account,
                  coalesce(k_symbol, mode)::event_type,
                  date
                 from cleaned.transactions
                        inner join cleaned.dispositions using(account)
              )
              ;
  
  create index semantic_events_event_ix on semantic.events(event);
  create index semantic_events_client_ix on semantic.events(client);
  create index semantic_events_client_account_ix on semantic.events(client, account);
  create index semantic_events_date_ix on semantic.events(date);
  create index semantic_events_type_ix on semantic.events(type);
  create index semantic_events_type_loan_granted_ix on semantic.events(type) where type = 'loan granted';

  end $semantic$;

  set search_path = semantic, public;
exception when others then
    get stacked diagnostics exc_message = message_text;
    get stacked diagnostics exc_context = pg_exception_context;
    get stacked diagnostics exc_detail = pg_exception_detail;
    raise exception E'\n------\n%\n%\n------\n\nCONTEXT:\n%\n', exc_message, exc_detail, exc_context;
end $$;
