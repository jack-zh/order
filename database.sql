/* CREATE DATABASE qcloud; */
create database qcloud default charset utf8 collate utf8_unicode_ci;
USE qcloud;
  
CREATE TABLE user (
    username varchar(20) NOT NULL,
    passwd varchar(20) NOT NULL,
    email varchar(20),
    authorization int default 0,
    phonenumber varchar(20),
    PRIMARY KEY (username)
);

CREATE TABLE area (
    areanum int NOT NULL default 1,
    areaname varchar(20) NOT NULL,
    PRIMARY KEY (areanum)
);

CREATE TABLE userarea (
    username varchar(20) NOT NULL,
    areanum int NOT NULL,
    foreign key(username) references user(username),
    foreign key(areanum) references area(areanum),
    PRIMARY KEY (username,areanum)
);

CREATE TABLE pas (
    areanum int NOT NULL default 1,
    gno varchar(15) NOT NULL,
    name varchar(40) NOT NULL,
    descs varchar(40),
    enable int NOT NULL default 1,
    status int NOT NULL default 2,
    stc datetime NOT NULL,
    foreign key(areanum) references area(areanum),
    PRIMARY KEY (gno)
);

CREATE TABLE history (  
    id int auto_increment primary key not null,
    gno varchar(15) NOT NULL,
    status int NOT NULL default 2,
    foreign key(gno) references pas(gno),
    stc datetime NOT NULL
);

INSERT INTO user (username,passwd,authorization) VALUES ('admin','admin',1)