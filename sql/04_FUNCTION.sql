--함수 (FUNCTION)

/*
    <함수>
        칼럼값을 읽어서 계산 결과를 반환한다.
          - 단일행 함수 : N개의 값을 읽어서 N개의 결과를 리턴한다. (매 행 함수 실행 -> 결과 반환)
          - 그룹 함수   : N개의 값을 읽어서 1개의 결과를 리턴한다. (하나의 그룹별로 함수 실행 -> 결과 반환)
        SELECT 절에 단일행 함수와 그룹 함수를 함께 사용하지 못한다. (결과 행의 개수가 다르기 때문에)
        함수를 기술할 수 있는 위치는 SELECT, WHERE, ORDER BY, GROUP BY, HAVING 절에 기술할 수 있다.
*/

--------------------- 단일행 함수 ---------------------

/*
    <문자 관련 함수>
    1) LENGTH / LENGTHB
      - LENGTH(칼럼|'문자값') : 글자 수 반환
      - LENGTHB(칼럼|'문자값') : 글자의 바이트 수 반환
        한글 한 글자 -> 3BYTE
        영문자, 숫자, 특수문자 한 글자 -> 1BYTE
        
    * DUAL 테이블
      - SYS 사용자가 소유하는 테이블
      - SYS 사용자가 소유하지만 모든 사용자가 접근이 가능하다.
      - 한 행, 한 칼럼을 가지고 있는 더미(DUMMY) 테이블이다.
      - 사용자가 함수(계산)를 사용할 때 임시로 사용하는 테이블이다.
*/

SELECT LENGTH(EMP_NAME)
FROM EMPLOYEE
;

/*
    2) INSTR
        - INSTR(칼럼|'문자값', '문자'[, POSITION[, OCCURRENCE]])
        - 지정한 위치부터 지정된 숫자 번째로 나타나는 문자의 시작 위치를 반환한다.
*/

SELECT  INSTR('AABAACAABBAA', 'B', -1, 3)
FROM DUAL
;

SELECT 
    EMAIL
    , INSTR(EMAIL, '@')
FROM EMPLOYEE
;

/* 
    3) LPAD / RPAD
        - LPAD/RPAD(칼럼|'문자값', 길이(바이트)[, '덧붙이려고 하는 문자'])
        - 제시된 칼럼|'문자값'에 임의의 문자를 왼쪽 또는 오른쪽에 덧붙여 최종 N 길이 만큼의 문자열을 반환한다.
        - 문자에 대해 통일감 있게 표시하고자 할 때 사용한다.
*/

SELECT RPAD(EMAIL, 20, '#')
FROM EMPLOYEE
;

/*
    4) LTRIM / RTRIM
        - LTRIM/RTRIM(칼럼|'문자값'[, '제거하고자 하는 문자'])
        - 문자열의 왼쪽 혹은 오른쪽에서 제거하고자 하는 문자들을 찾아서 제거한 결과를 반환한다.
        - 제거하고자 하는 문자값을 생략 시 기본값으로 공백을 제거한다.
*/

SELECT LTRIM('        A   BC           ')
FROM DUAL
;

/*
    5) TRIM
        - TRIM([[LEADING|TRAILING|BOTH] '제거하고자 하는 문자값' FROM] 칼럼|'문자값')
        - 문자값 앞/뒤/양쪽에 있는 지정한 문자를 제거한 나머지를 반환한다. 
        - 제거하고자 하는 문자값을 생략 시 기본적으로 양쪽에 있는 공백을 제거한다. 
*/

SELECT TRIM('        A   BC           ')
FROM DUAL
;

/*
    6) SUBSTR
        - SUBSTR(칼럼|'문자값', POSITION[, LENGTH])
        - 문자데이터에서 지정한 위치부터 지정한 개수만큼의 문자열을 추출해서 반환한다.
*/

SELECT SUBSTR('HELLO WORLD', -3, 6)
FROM DUAL
;

SELECT
    EMP_NAME
    , EMP_NO
    , SUBSTR(EMP_NO, 8,1) 성별
FROM EMPLOYEE
WHERE SUBSTR(EMP_NO, 8,1) = 1
;

/*
    7) LOWER / UPPER / INITCAP
        - LOWER/UPPER/INITCAP(컬럼|'문자값')
          LOWER : 모두 소문자로 변경한다.
          UPPER : 모두 대문자로 변경한다.
          INITCAP : 단어 앞 글자마다 대문자로 변경한다.
*/

/*
    8) CONCAT
        - CONCAT(칼럼|'문자값', 칼럼|'문자값')
        - 문자데이터 두 개를 전달받아서 하나로 합친 후 결과를 반환한다.
*/

SELECT 'AAA' || 'BBB'
FROM DUAL
;

SELECT CONCAT('AAA', 'BBB')
FROM DUAL
;

/*
    9) REPLACE
      - REPLACE(칼럼|'문자값', 변경하려고 하는 문자, 변경하고자 하는 문자)
      - 칼럼 또는 문자값에서 "변경하려고 하는 문자"를 "변경하고자 하는 문자"로 변경해서 반환한다.
*/
