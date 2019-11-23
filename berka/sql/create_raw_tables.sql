create schema if not exists raw;

drop table if exists raw.account;

create table raw.account (
  "account_id" TEXT,
  "district_id" TEXT,
  "frequency" TEXT,
  "date" TEXT
);

comment on table raw.account is 'describe las características estáticas de una cuenta';

drop table if exists raw.client;

create table raw.client (
  "client_id" TEXT,
  "birth_number" TEXT,
  "district_id" TEXT
);

comment on table raw.client is 'describe las características de los clientes';

drop table if exists raw.district;

create table raw.district (
  "A1" TEXT,
  "A2" TEXT,
  "A3" TEXT,
  "A4" TEXT,
  "A5" TEXT,
  "A6" TEXT,
  "A7" TEXT,
  "A8" TEXT,
  "A9" TEXT,
  "A10" TEXT,
  "A11" TEXT,
  "A12" TEXT,
  "A13" TEXT,
  "A14" TEXT,
  "A15" TEXT,
  "A16" TEXT
);

comment on table raw.district is 'describe las características demográficas de un distrito';

drop table if exists raw.order;

create table raw.order (
  "order_id" TEXT,
  "account_id" TEXT,
  "bank_to" TEXT,
  "account_to" TEXT,
  "amount" TEXT,
  "k_symbol" TEXT
);

comment on table raw.order is 'describe una orden de pago';

drop table if exists raw.card;

create table raw.card (
  "card_id" TEXT,
  "disp_id" TEXT,
  "type" TEXT,
  "issued" TEXT
);

comment on table raw.card is 'describe las tarjetas de crédito emitidas para las cuentas';

drop table if exists raw.disp;

create table raw.disp (
  "disp_id" TEXT,
  "client_id" TEXT,
  "account_id" TEXT,
  "type" TEXT
);

comment on table raw.disp is 'describe la relación entre clientes y cuentas';

drop table if exists raw.loan;

create table raw.loan (
  "loan_id" TEXT,
  "account_id" TEXT,
  "date" TEXT,
  "amount" TEXT,
  "duration" TEXT,
  "payments" TEXT,
  "status" TEXT
);

comment on table raw.loan is 'describe préstamos otorgados a cuentas';

drop table if exists raw.trans;

create table raw.trans (
  "trans_id" TEXT,
  "account_id" TEXT,
  "date" TEXT,
  "type" TEXT,
  "operation" TEXT,
  "amount" TEXT,
  "balance" TEXT,
  "k_symbol" TEXT,
  "bank" TEXT,
  "account" TEXT
);

comment on table raw.trans is 'describe transacciones en una cuenta';
