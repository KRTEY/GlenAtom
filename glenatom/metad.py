# glenatom/metad.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def read_hills_file(directory_path):
    """
    디렉토리 경로를 받아 'HILLS' 파일을 찾아 Pandas DataFrame으로 반환합니다.

    :param directory_path: 'HILLS' 파일이 있는 디렉토리 경로
    :return: HILLS 데이터가 담긴 Pandas DataFrame
    """
    hills_path = os.path.join(directory_path, 'HILLS')

    if not os.path.exists(hills_path):
        raise FileNotFoundError(f"Error: 'HILLS' file not found in '{directory_path}'")

    # 파일 내에서 첫 번째 주석 라인을 찾아 헤더를 추출하는 내부 함수
    def get_headers(filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip().startswith('#'):
                    # '#!' 또는 '#'를 제거하고 양쪽 공백을 정리
                    header_line = line.strip().lstrip('#!').strip()
                    # 첫 필드('time' 등)를 제외하고 실제 CV 필드만 반환하는 경우가 많으므로,
                    # Plumed 헤더 형식에 맞춰 필드 개수를 확인해야 함.
                    if 'FIELDS' in header_line:  # 여기서는 'FIELDS' 단어를 기준으로 분리하고 그 이후의 필드를 사용.
                        return header_line.split('FIELDS')[1].strip().split()
        return None

    column_names = get_headers(hills_path)
    if not column_names:
        raise ValueError(f"Could not find a header line starting with '# FIELDS' in {hills_path}")

    print(f"✅ Reading HILLS file with headers: {column_names}")
    
    # Pandas를 사용하여 데이터 로드
    hills_df = pd.read_csv(
        hills_path,
        comment='#',
        sep=r'\s+',  # 정규 표현식을 사용하여 모든 종류의 공백 처리
        header=None,
        names=column_names,
        engine='python' # sep가 정규표현식일 때 권장
    )
    
    return hills_df


def plot_test(hills_df, y_col, x_col='time', timestep=0.001, ax=None, downsample=10,color='black', **kwargs):
    """
    HILLS DataFrame에서 특정 열의 수렴을 시각화합니다.

    :param hills_df: read_hills_file로 읽은 DataFrame
    :param y_col: Y축에 그릴 데이터의 열(column) 이름 (e.g., 'height')
    :param x_col: X축에 사용할 데이터의 열 이름 (기본값: 'time')
    :param timestep: 시간 단위 변환을 위한 계수 (기본값: 0.001 -> ps 단위)
    :param ax: 그래프를 그릴 Matplotlib axes 객체 (없으면 새로 생성)
    :param downsample: 데이터 양이 많을 경우 N개 중 1개만 샘플링하여 그림 (기본값: 10)
    :return: Matplotlib figure와 axes 객체
    """
    if y_col not in hills_df.columns:
        raise ValueError(f"Column '{y_col}' not found in the DataFrame. Available columns: {hills_df.columns.tolist()}")
    if x_col not in hills_df.columns:
        raise ValueError(f"Column '{x_col}' not found in the DataFrame. Available columns: {hills_df.columns.tolist()}")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    # 데이터 준비
    y_data = hills_df[y_col]
    x_data = hills_df[x_col] * timestep  # 시간 단위 변환

    # 데이터 플로팅 (스타일링 요소는 제거하여 fiddich를 따르도록 함)
    ax.scatter(x_data[::downsample], y_data[::downsample], color=color, **kwargs)
    
    return fig, ax