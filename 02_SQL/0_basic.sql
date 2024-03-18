-- 주석 
/*
block 주석 - 여러줄 짜리 주석.

SQL문을 실행: control + enter
*/
-- 사용자 계정 생성. 
-- 로컬 접속 사용자 계정
create user 'playdata'@'localhost' identified by '1111';
-- 원격 접속 사용자 계정
create user 'playdata'@'%' identified by '1111';
-- 등록된 사용자 계정 조회.
select user, host from mysql.user;
-- 생성한 계정에 권한 부여 (모든 권한 ==> 관리자 계정.)
grant all privileges on *.* to 'playdata'@'localhost';
grant all privileges on *.* to 'playdata'@'%';
-- grant 부여할 권한 on Database.테이블  to 계정

-- database 생성 
create database testdb;
-- database들 조회
show databases;
-- 특정 데이터베이스를 사용
use testdb;  -- database이름.테이블이름 => use 를 하면 database이름 을 생략가능.
/*
create table 이름(
	컬럼이름1 데이터타입 제약조건,
    컬럼이름2 데이터타입 제약조건,
    컬럼이름3 데이터타입 제약조건,
    컬럼이름4 데이터타입 제약조건
)
*/

use testdb;
-- 테이블: member, 
-- 속성: id, password, name, point, email, gender, age, join_date


create table member (
	id varchar(10) primary key,
    password varchar(10) not null,
    name varchar(50) not null,
    point int default 1000, -- 값을 넣지 않으면 1000을 기본값으로 넣는다. not null (x) -> null을 허용하는 컬럼.(nullable)
    email varchar(100) unique, 
    gender char(1) check(gender in ('M', 'F')),
    age    int check(age > 0),
    join_date timestamp not null default current_timestamp -- 값을 넣는 sql이 실행되는 시점의 일시를 넣는다.
);

-- 테이블 조회
show tables;
-- 테이블의 컬럼들 조회
desc member;

-- 테이블 삭제
drop table if exists member;

-- 데이터를 추가 (insert문 - 행추가)
-- 전체 컬럼에 다 값을 넣을 경우 컬럼명은 생략 가능.
-- 문자열: ' ' 감싼다.
-- 일시: ' ' 감싼다. '년-월-일 시:분:초'
insert into member values ('id-1', 'abc111', '이순신',
						    2000, 'a@a.com', 'M', 20, '2000-10-02 10:10:20');

insert into member (id, password, name, join_date)
values ('id-2', '11111', '유관순', '2001-01-02 15:22:33');

select * from member;

insert into member (id, password, name, gender)
values ('id-3', '11111aa', '유관순', 'F' );


