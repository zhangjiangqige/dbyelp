create table tip (
    business_id char(32) not null,
    compliment_count int default 0,
    date datetime not null,
    user_id char(32) not null
);