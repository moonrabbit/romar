# Rows Marshaller
Row의 나열 형태로 되어있는 데이터를 템플릿에 맞게 구조화 해주는 라이브러리입니다.
 
# Data Type
 * str : 문자열
 * list<{type}> : 리스트. type에는 지원하는 다른 타입들을 넣을 수 있음.
 * num : 숫자
 * bool : 참/거짓

# Options
 romar는 dict 형태로 option을 받습니다.

## option list
 * list_separators : 한 컬럼에서 리스트를 표현하는 경우 각 아이템을 구분하기 위한 구분자를
 넣을 수 있는 부분.
    * ex) ',|' => ,과 |를 구분자로 사용
 * ignore_empty_item : list나 dict에서 비어있는 아이템을 무시할 것인지 결정하는 옵션
 * filter : 무시할 row를 위한 filter. dict로 표현됨.
    * ex) inclusion:bool 컬럼이 참인 경우에만 포함됨.

        {
            '${inclusion:bool}': True
        }

