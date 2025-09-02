# glenatom/plotting.py 

import matplotlib.pyplot as plt
import os


def fiddich(what='line'):
    """
    지정된 이름의 Matplotlib 스타일을 적용합니다.

    스타일 파일은 패키지 내부의 'styles' 디렉토리에 위치해야 합니다.
    .mplstyle 확장자는 자동으로 추가됩니다.

    Args:
        what (str): 적용할 스타일의 이름 (e.g., 'line', 'bar').
    """
    style_dir = os.path.join(os.path.dirname(__file__), 'styles')
    style_file = os.path.join(style_dir, f"{what}.mplstyle")

    if os.path.exists(style_file):
        plt.style.use(style_file)
        #print(f"✅ GlenAtom style '{what}' applied successfully.")
    else:
        print(f"❌ Warning: GlenAtom style '{what}' not found.")


def get_available_styles():
    """
    'styles' 디렉토리에서 사용 가능한 모든 스타일 시트 목록을 반환합니다.
    """
    try:
        style_dir = os.path.join(os.path.dirname(__file__), 'styles')
        
        # styles 폴더 안의 파일 목록을 읽어와서
        # .mplstyle로 끝나는 파일만 골라냅니다.
        # 'line.mplstyle' -> 'line' 으로 확장자를 제거합니다.
        available_styles = [
            f.replace('.mplstyle', '') 
            for f in os.listdir(style_dir) 
            if f.endswith('.mplstyle')
        ]
        return available_styles
    except FileNotFoundError:
        # styles 폴더가 없는 예외 상황 처리
        return []