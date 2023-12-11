-----------------------------------------------------------------------------------------------------------------------------------------
----- The 3 statics I have captured are the win rate, the amount of games played by each person and each persons highest win streak -----
-----------------------------------------------------------------------------------------------------------------------------------------
/*

create database BlackJackDB;

grant all on BlackJackDB.* to 'dan'@'localhost' identified by 'password'

exit



mysql -u dan -p BlackJackDB
password


create table games (
    gamertag varchar(32) not null,
    outcome varchar(4) not null,
    attempts varchar(8) not null,
    wins varchar(4) not null
);


create table players (
    realname varchar(32) not null,
    gamertag varchar(32) not null,
    email varchar(64) not null
);


insert into players (realname, gamertag, email) values ("Josh", "JDawg", "c00270917@setu.ie");
insert into players (realname, gamertag, email) values ("Shane", "idk", "c00270031@setu.ie");
insert into players (realname, gamertag, email) values ("Alwyn", "alwyn", "c00271145@setu.ie");
insert into players (realname, gamertag, email) values ("Darragh", "FrogGranna", "c00271651@setu.ie");
insert into players (realname, gamertag, email) values ("Pavol", "PDawg", "c00272003@setu.ie");
insert into players (realname, gamertag, email) values ("Daniel", "frodo", "c00272187@setu.ie");
insert into players (realname, gamertag, email) values ("Richie", "The Legend 27", "c00272345@setu.ie");
insert into players (realname, gamertag, email) values ("Conor", "xxx_CDawg_xxx", "c00272506@setu.ie");
insert into players (realname, gamertag, email) values ("Jack", "Xx_TTV_MadJack69_xX", "c00273123@setu.ie");
insert into players (realname, gamertag, email) values ("Ruslan", "Ruark", "c00273521@setu.ie");
insert into players (realname, gamertag, email) values ("Killian", "kio", "c00275417@setu.ie");
insert into players (realname, gamertag, email) values ("Adrian", "Mia", "c0027xxxxx@setu.ie");

*/