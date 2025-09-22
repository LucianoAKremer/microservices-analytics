-- Tabla de usuarios
drop table if exists users cascade;
create table users (
    id serial primary key,
    username varchar(50) unique not null,
    password_hash varchar(255) not null
);

-- Tabla de categorías
drop table if exists categories cascade;
create table categories (
    id serial primary key,
    name varchar(100) not null
);

-- Tabla de gastos
drop table if exists expenses cascade;
create table expenses (
    id serial primary key,
    amount numeric(12,2) not null,
    description varchar(255),
    date date not null,
    category_id integer references categories(id),
    user_id integer references users(id)
);

insert into categories (name) values ('General'), ('Alimentación'), ('Transporte'), ('Entretenimiento');

