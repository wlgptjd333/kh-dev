-- 테이블 생성
CREATE TABLE BOARD(
    TITLE       VARCHAR2(100)
    , CONTENT   VARCHAR2(4000)
);

-- 데이터 넣기
INSERT INTO BOARD(TITLE, CONTENT) VALUES('안녕' , '반갑습니다');

-- 데이터 조회
SELECT * FROM BOARD;


-- 데이터 수정
UPDATE BOARD SET TITLE = '안녕하세요'  WHERE TITLE = '안녕';

-- 데이터 삭제
DELETE BOARD WHERE TITlE = '안녕하세요';

-- 테이블 삭제
DROP TABLE BOARD;