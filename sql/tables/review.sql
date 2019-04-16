create table review (
    business_id char(32) not null,
    cool int default 0,
    date datetime not null,
    funny int default 0,
    review_id char(32) not null,
    stars int default 0,
#     text text default null,
    useful int default 0,
    user_id char(32) not null
);