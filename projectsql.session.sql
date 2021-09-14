create table student(
    sid VARCHAR(20),
    sname VARCHAR(20),
    spwd VARCHAR(20),
    sattend VARCHAR(20),
    periods VARCHAR(20),
    percen VARCHAR(20)
);

select * from student;

delete from student where sid = "18521";

insert into student values('saketh_reddy','18509','18509','10','20','50');

insert into student values('nitish_kumar','18519','18519','20','24','41');

insert into student values('varun_sai','18532','18532','10','10','50');

insert into student values('nishant_racherla','18535','18535','12','24','50');

create table admin(
    aid VARCHAR(10),
    apwd VARCHAR(10)
);

select * from admin;

insert into admin values('ts101','ts101');

insert into admin values('ts102','ts102');

insert into admin values('ts103','ts103');

insert into admin values('ts104','ts104');

