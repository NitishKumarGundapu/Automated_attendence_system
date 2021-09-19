create database project;

use project;

create table student(
    sname varchar(20),    
    sid varchar(10),
    spwd varchar(10),
    sattend varchar(5),
    periods varchar(5),
    percen varchar(5)
);

insert into student values('nitish_kumar','18519','18519','20','24','41');

insert into student values('saketh_reddy','18509','18509','10','20','50');

insert into student values('varun_sai','18532','18532','10','20','50');

insert into student values('nishant_racherla','18535','18535','10','20','50');

insert into student values('anunai','18531','18531','10','20','50');

insert into student values('jaideep','18513','18513','10','20','50');

insert into student values('pranav','18534','18534','10','20','50');

select * from student;

create table admin(
    aid VARCHAR(10),
    apwd VARCHAR(10)
);

insert into admin values('ts104','ts104');

insert into admin values('ts101','ts101');

insert into admin values('ts102','ts102');

insert into admin values('ts103','ts103');

select * from admin;
