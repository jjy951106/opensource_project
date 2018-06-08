schema name = nodejsconnect
table name = project

CREATE TABLE project (
	id	INT NOT NULL primary Key,
    sName VARCHAR(20),
    hit INT
);

router 폴더의 main.js에서 connection을 자기 데이터베이스에 맞게 수정해주고 사용.
