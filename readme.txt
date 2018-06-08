schema name = nodejsconnect
table name = project
table name = photopath

CREATE TABLE project (
	id	INT NOT NULL primary Key,
    sName VARCHAR(20),
    hit INT
);

CREATE TABLE photopath (
	id	INT NOT NULL primary Key,
    path VARCHAR(40)
);

router 폴더의 main.js에서 connection을 자기 데이터베이스에 맞게 수정해주고 사용.

실행은 server.js

업로드중간에 나가버리면 photopath 테이블이랑 project 테이블이 꼬일 가능성이 있음. 주의할 것.