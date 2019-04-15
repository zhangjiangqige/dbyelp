create table user (
    average_stars float default 0,
    cool int default 0,
    elite VARCHAR(1024) default null,
    fans int default 0,
    review_count int default 0,
    useful int default 0,
    user_id char(32) not null,
    yelping_since datetime
);

create table business (
    business_id char(32) not null,
    categories VARCHAR(1024) default null,
#     hours__Friday_o time default null,
#     hours__Friday_c time default null,
#     hours__Monday_o time default null,
#     hours__Monday_c time default null,
#     hours__Saturday_o time default null,
#     hours__Saturday_c time default null,
#     hours__Sunday_o time default null,
#     hours__Sunday_c time default null,
#     hours__Thursday_o time default null,
#     hours__Thursday_c time default null,
#     hours__Tuesday_o time default null,
#     hours__Tuesday_c time default null,
#     hours__Wednesday_o time default null,
#     hours__Wednesday_c time default null,
    is_open int default 0,
    review_count int default 0,
    stars float default 0
);

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

create table tip (
    business_id char(32) not null,
    compliment_count int default 0,
    date datetime not null,
    user_id char(32) not null
);
