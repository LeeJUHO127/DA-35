-- Edit > Preferences.. > 왼쪽: SQL Editor > 최하단 - Safe update .... 체크해제
-- Edit > Preferences > 왼쪽: SQL Editor - SQL Execution > New Connection autocommit ... 체크해제
use hr_join;
-- mysql (서버)의 autocommit 여부 설정을 확인
select @autocommit;
-- autocommit 설정을 변경.  1: auto commit, 0: manual commit
set @autocommit = 0;

-- commit: 데이터를 수정(추가, 삭제, 수정)한 것을 영구적으로 적용.
-- rollback: 변경을 시작한 상태로 되돌린다. (지금까지 변경한 것을 무효화)

use hr_join;
select * from emp;

delete from emp;
commit;
rollback;


/* *********************************************************************
INSERT 문 - 행 추가
구문
 - 한 행추가 :
   - INSERT INTO 테이블명 (컬럼 [, 컬럼]) VALUES (값 [, 값[])
   - 모든 컬럼에 값을 넣을 경우 컬럼 지정구문은 생략 할 수 있다.
************************************************************************ */
insert into emp values (500, '이순신', 'IT_PROG', 120, 
					   '2020-10-20', 50000.99, null, 30);
commit;
select * from emp order by emp_id desc;
rollback;

insert into emp values (501, '이순신', 'IT_PROG', 120, 
					   '2020-10-20', 50000.99, null, 270);

desc emp;

/* *********************************************************************
UPDATE : 테이블의 컬럼의 값을 수정
UPDATE 테이블명
SET    변경할 컬럼 = 변경할 값  [, 변경할 컬럼 = 변경할 값]
[WHERE 제약조건]

 - UPDATE: 변경할 테이블 지정
 - SET: 변경할 컬럼과 값을 지정
 - WHERE: 변경할 행을 선택. 
************************************************************************ */
-- update emp
-- set    salary = 0;
-- select * from emp;
-- rollback;
-- 직원 ID가 200인 직원의 급여를 5000으로 변경
select * from emp where emp_id = 200;
update emp
set    salary = 5000
where  emp_id = 200;

-- 직원 ID가 200인 직원의 급여를 10% 인상한 값으로 변경.
select * from emp where emp_id = 200;
update emp
set    salary = salary * 1.1
where  emp_id = 200;

-- 부서 ID가 80인 직원의 커미션 비율을 null 로 변경.
select * from emp where dept_id = 80;
update emp
set    comm_pct = null
where  dept_id = 80;

--  부서 ID가 100인 직원들의 급여를 100% 인상
select * from emp where dept_id = 100;
update emp
set    salary = salary * 2
where dept_id = 100;

-- 부서 ID가 100인 직원의 커미션 비율을 0.2로 salary는 3000을 더한 값으로, 
--  상사_id는 100 변경.
select * from emp where dept_id = 100;
update emp
set    comm_pct = 0.2,
	   salary = salary + 3000,
	   mgr_id = 100
where  dept_id = 100;

--  IT 부서의 직원들의 급여를 3배 인상
select * from emp where dept_id = 60;
update emp
set    salary = salary * 3
where  dept_id = (select dept_id from dept where dept_name='IT');
-- select dept_id from dept where dept_name='IT';
commit;

-- EMP 테이블의 모든 데이터를 MGR_ID는 NULL로 HIRE_DATE 는 
--     현재일시로 COMM_PCT는 0.5로 수정.
update emp
set    mgr_id = null,
       hire_date = curdate(),
       comm_pct = 0.5;
select * from emp;       


/* *********************************************************************
DELETE : 테이블의 행을 삭제
구문 
 - DELETE FROM 테이블명 [WHERE 제약조건]
   - WHERE: 삭제할 행을 선택
************************************************************************ */

-- 전체 행 삭제
delete from emp;
select * from emp;
rollback;
-- 부서테이블에서 부서_ID가 200인 부서 삭제
select * from emp where dept_id = 200;
delete from emp where dept_id = 200;

select * from dept where dept_id = 200;
delete from dept where dept_id = 200;

-- 부서테이블에서 부서_ID가 10인 부서 삭제
select * from emp where emp_id = 200;
select * from emp where dept_id = 10; -- on delete cascade => 10번 부서를 삭제하면 10번 부서 소속 직원 데이터도 같이 삭제
select * from dept where dept_id = 10;

delete from dept where dept_id = 10;  

rollback;

-- JOB 테이블에서 job_id가 SA_MAN인 행을 삭제
select * from emp where job_id = 'SA_MAN';

delete from job where job_id = 'SA_MAN';
SELECT *  from job where job_id = 'SA_MAN';

-- on delete set null => 부모테이블에서 참조하고있는 행이 삭제 되면 FK 컬럼 값을 null 변경.
select * from emp where emp_id in (145,146,147,148,149);

-- 부서 ID가 없는 직원들을 삭제
select * from emp where dept_id is null;
delete from emp where dept_id is null;

-- 담당 업무(emp.job_id)가 'SA_MAN'이고 급여(emp.salary) 가 12000 미만인 직원들을 삭제.
rollback;
select * from emp where job_id = 'SA_MAN' and salary < 12000;
delete from emp  where job_id = 'SA_MAN' and salary < 12000;

-- comm_pct 가 null이고 job_id 가 IT_PROG인 직원들을 삭제
select * from emp where comm_pct is null and job_id = 'IT_PROG';
delete from emp  where comm_pct is null and job_id = 'IT_PROG';

