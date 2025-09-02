import os
import pandas as pd
import matplotlib.pyplot as plt

def get_headers_from_line(file_path, line_number, exclude_words=None):
    """
    지정된 파일의 특정 줄에서 헤더 목록을 추출합니다.
    '#'는 default로 제거되며, 필요에 따라 추가 단어를 제외할 수 있습니다.
    :param file_path: (str) 파일 경로
    :param line_number: (int) 헤더가 위치한 줄 번호 (1부터 시작)
    :param exclude_words: (list, optional) 헤더에서 제외할 단어 목록. 기본값은 None.
    :return: (list) 추출 및 필터링된 헤더 목록
    """
    if exclude_words is None:
        exclude_words = []
    
    # 제외할 단어들을 소문자로 변환하여 비교 시 대소문자 구분 없도록 함
    exclude_words_lower = [word.lower() for word in exclude_words]

    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            if i == line_number:
                # 라인 정리: 앞뒤 공백 제거 및 주석 기호('#') 제거
                header_line = line.strip().lstrip('#').strip()
                
                # 공백 기준으로 단어 분리 후, 제외할 단어 필터링
                all_fields = header_line.split()
                column_names = [
                    field for field in all_fields 
                    if field.lower() not in exclude_words_lower
                ]
                return column_names
                
    raise ValueError(f"Error: Line {line_number} not found in file {file_path}.")

def read_file(file_path, header_line, no_header_words=None):
    ## 추가해야 할 것 skip_lines 및 comment로 시작하는 줄 다 생략하는 코드 추가
    """
    파일의 특정 줄을 헤더로 사용하여 데이터를 읽어 Pandas DataFrame으로 반환합니다.

    :param file_path: (str) 파일 경로
    :param header_line: (int) 헤더가 위치한 줄 번호
    :param no_header_words: (list, optional) 헤더 라인에서 제외할 단어 목록 (예: ['FIELDS', 'time'])
    :return: (pd.DataFrame) 데이터가 담긴 Pandas DataFrame
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: file not found in '{file_path}'")

    # 헬퍼 함수를 사용하여 헤더 추출
    column_names = get_headers_from_line(file_path, header_line, no_header_words)
    
    if not column_names:
        raise ValueError(f"Could not find any headers on line {header_line} in {file_path}")

    print(f"✅ Reading file with headers: {column_names}")
    
    # Pandas를 사용하여 데이터 로드
    df = pd.read_csv(
        file_path,
        comment='#',          # '#'로 시작하는 모든 줄을 주석으로 처리하여 건너뜀
        sep=r'\s+',           # 정규 표현식을 사용하여 모든 종류의 공백 처리
        header=None,          # 파일 자체의 헤더를 사용하지 않음
        names=column_names,   # 위에서 추출한 헤더를 컬럼명으로 지정
        engine='python'       # sep가 정규표현식일 때 권장
    )
    
    return df