create schema if not exists raw;

drop table if exists raw.accounts;

create table accounts (
  "account_id" TEXT,
  "district_id" TEXT,
  "frequency" TEXT,
  "date" TEXT
);

drop table if exists raw.clients;

create table clients (
  "client_id" TEXT,
  "birth_number" TEXT,
  "district_id" TEXT
);

drop table if exists raw.districts;

create table districts(
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

drop table if exists raw.orders;

create table orders (
  "order_id" TEXT,
  "account_id" TEXT,
  "bank_to" TEXT,
  "account_to" TEXT,
  "amount" TEXT,
  "k_symbol" TEXT
);

drop table if exists raw.cards;

create table cards (
  "card_id" TEXT,
  "disp_id" TEXT,
  "type" TEXT,
  "issued" TEXT
);

drop table if exists raw.dispositions;

create table dispositions (
  "disp_id" TEXT,
  "client_id" TEXT,
  "account_id" TEXT,
  "type" TEXT
);

drop table if exists raw.loans;

create table loans (
  "loan_id" TEXT,
  "account_id" TEXT,
  "date" TEXT,
  "amount" TEXT,
  "duration" TEXT,
  "payments" TEXT,
  "status" TEXT
);

drop table if exists raw.transactions;

create table transactions (
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
