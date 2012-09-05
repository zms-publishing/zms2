# http://gadfly.sourceforge.net/gadfly.html
create table cds (cd_id integer, cd_title varchar, cd_cover varchar, cd_category integer);
insert into cds(cd_id, cd_title, cd_cover, cd_category) values (4711, 'Pink Floyd: The dark side of the moon', '', 1);
insert into cds(cd_id, cd_title, cd_cover, cd_category) values (4712, 'Rolling Stones: A Bigger Bang', '', 2);
create table cdtracks (cd_id integer, track_id integer, track_title varchar, track_duration varchar, track_info varchar, sort_id integer);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4711, 1, 'Speak to Me', '1:30', 'Nick Mason', 10);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4711, 2, 'Breathe', '2:43', 'David Gilmour, Roger Waters, Richard Wright', 20);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4711, 3, 'On the Run', '3:30', 'Gilmour, Waters', 30);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4711, 4, 'Time', '6:53', 'Gilmour, Waters, Wright, Mason', 40);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4712, 5, 'Rough Justice', '3:13', '', 10);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4712, 6, 'Let Me Down Slow', '4:15', '', 20);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4712, 7, 'It Wont Take Long', '3:54', '', 30);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4712, 8, 'Rain Fall Down', '4:54', '', 40);
insert into cdtracks (cd_id, track_id, track_title, track_duration, track_info, sort_id) values ( 4712, 9, 'Streets of Love', '5:10', '', 50);
create table cdreviews (cd_id integer, review_id integer, review_author varchar, review_timestamp varchar, review_title varchar, review_content varchar);
insert into cdreviews (cd_id, review_id, review_author, review_timestamp, review_title, review_content) values ( 4711, 1, 'F. Lieberman', '2005-01-01.12.00.00', 'Excellent!', 'Excellent sound, the best Pink Floyd record ever!');
create table cdcategories (category_id integer, category_name varchar);
insert into cdcategories (category_id, category_name) values ( 1, 'Klassik');
insert into cdcategories (category_id, category_name) values ( 2, 'Rock');
create table cdcompanies (company_id varchar, company_name varchar);
insert into cdcompanies (company_id, company_name) values ( 'BMG', 'Bertelsmann Music Group');
insert into cdcompanies (company_id, company_name) values ( 'SOE', 'Sony Entertainment');
insert into cdcompanies (company_id, company_name) values ( 'ARI', 'Ariola');
create table cdhascategory (cd_id integer, category_id integer);