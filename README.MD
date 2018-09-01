# Logs Analysis Project
Generate the text report from PostgreSQL DB with provided data dump 
using SQL Queries and Views (Optional)

## Project tasks
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements / Prerequisites
1. Download / install [Vagrant](https://www.vagrantup.com/)
2. Download / install [Virtual Box](https://www.virtualbox.org/)
3. Clone / fork source from this repository.
4. Unzip **newsdata.zip**
5. Move **newsdata.sql** and **syslog.py** files to **vagrant** directory.

#### Run commands bellow: 
1. ```vagrant up```
2. ```vagrant ssh``` 
3. ```cd /vagrant``` 
4. ```psql -d news -f newsdata.sql``` 
5. ```python3 syslog.py``` 

## Required Views
##### vw_status
````sql
CREATE VIEW vw_status AS
SELECT time ::date, status
FROM log;
````
##### vw_status_fail
````sql
CREATE VIEW vw_status_fail AS
SELECT time, count(*) AS counter
FROM vw_status
WHERE status = '404 NOT FOUND'
GROUP BY time;
````
##### vw_status_all
````sql
CREATE VIEW vw_status_all AS
SELECT time, count(*) AS counter
FROM vw_status
WHERE status = '404 NOT FOUND' OR status = '200 OK'
GROUP BY time;
````
##### vw_percentage_counter
````sql
CREATE VIEW vw_percentage_counter AS
SELECT vw_status_all.time,
       vw_status_fail.counter::double precision/vw_status_all.counter::double precision * 100 AS percentage_fail
FROM vw_status_all, vw_status_fail
WHERE vw_status_all.time = vw_status_fail.time;
````