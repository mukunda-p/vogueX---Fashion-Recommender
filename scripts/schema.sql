drop database fashion;
create database fashion;
use fashion;

drop table user;
drop table user_details;
drop table preference;
drop table recommendation;

create table user(
    userid varchar(255) not null primary key,
    password varchar(255) not null
);

create table user_details (
    userid varchar(255) not null primary key,
    firstname varchar(255) not null,
    lastname varchar(255) not null,
    age int,
    city varchar(255) not null,

    foreign key (userid) references user(userid)
);

create table preference ( 
    userid varchar(255)  not null, 
    preferences json not null, 
    primary key (userid), 
    foreign key (userid) references user(userid));

create table recommendation (
    userid varchar(255) not null, 
    links json not null, 
    primary key (userid),
    foreign key (userid) references user(userid));