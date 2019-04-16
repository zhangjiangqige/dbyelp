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