drop table if exists CurrentTime;
create table CurrentTime (
	cur_time datetime primary key
);
insert into CurrentTime values (' 2001-12-20 00:00:01');
select cur_time from CurrentTime;
