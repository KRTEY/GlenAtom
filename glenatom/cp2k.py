# Add these to the top of your glenatom.py file if they aren't there already
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import subprocess
import numpy as np

# Your other functions (like fiddich) can remain here...

def read_box(directory_path):
    """
    디렉터리 내 out.log 파일에서 Cell lengths 데이터를 효율적으로 파싱합니다.
    (순수 파이썬을 사용하여 subprocess 오버헤드를 제거한 버전)

    Args:
        directory_path (str): 분석할 out.log 파일이 있는 디렉터리 경로.

    Returns:
        numpy.ndarray: a, b, c cell 길이를 담은 2D NumPy 배열.
                       데이터가 없으면 비어있는 배열을 반환합니다.
    """
    log_file_path = os.path.join(directory_path, 'out.log')

    if not os.path.exists(log_file_path):
        print(f"Error: 파일을 찾을 수 없습니다 -> {log_file_path}")
        return np.array([])

    # 추출한 데이터를 임시로 저장할 리스트
    extracted_data = []
    
    try:
        # 파일을 열고, 한 줄씩 메모리에 올리며 처리 (대용량 파일에 효율적)
        with open(log_file_path, 'r') as f:
            for line in f:
                # 원하는 문자열이 포함된 줄만 처리
                if 'Cell lengths [ang' in line:
                    try:
                        parts = line.split()
                        # 5, 6, 7번째 열(인덱스 4, 5, 6)을 float으로 변환해 추가
                        row = [float(parts[4]), float(parts[5]), float(parts[6])]
                        extracted_data.append(row)
                    except (IndexError, ValueError):
                        # 줄은 찾았지만 형식이 안 맞는 경우(숫자가 없거나 부족)는 건너뜀
                        continue
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
        return np.array([])
    
    # 마지막에 리스트를 NumPy 배열로 한 번에 변환
    return np.array(extracted_data)


def read_ener(directory_path):
    """
    Scans a directory for .ener files, combines them, and returns a DataFrame.

    This function searches for all files ending with '.ener', reads them, 
    concatenates them into a single pandas DataFrame, and sorts the result by time.

    Args:
        directory_path (str): The full path to the directory containing the .ener files.

    Returns:
        pandas.DataFrame: A single DataFrame containing all the combined and sorted data.
                          Returns None if no files are found or if data cannot be read.
    """
    #print(f"Searching for .ener files in: {directory_path}")
    
    search_pattern = os.path.join(directory_path, '*.ener')
    ener_files = glob.glob(search_pattern)

    if not ener_files:
        print(f"No '.ener' files found in '{directory_path}'.")
        return None

    #print(f"Found {len(ener_files)} files. Processing...")

    column_names = [
        'Step', 'Time[fs]', 'Kin.[a.u.]', 'Temp[K]', 'Pot.[a.u.]',
        'Cons Qty[a.u.]', 'UsedTime[s]'
    ]

    df_list = []
    for file in ener_files:
        try:
            df = pd.read_csv(
                file,
                delim_whitespace=True,
                header=None,
                names=column_names,
                dtype=float,
                comment='#'
            )
            df_list.append(df)
        except Exception as e:
            print(f"Warning: Could not process file {file}. Error: {e}")

    if not df_list:
        print("All files failed to process. No data to return.")
        return None

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df = combined_df.sort_values(by='Time[fs]')
    
    #print("Data successfully loaded and combined.")
    return combined_df

def plot_box_test(data_df):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(np.arange(data_df.shape[0])*0.5, data_df[:,0], color='black')
    ax.set_xlabel('Time [fs]', fontsize=10)
    ax.set_ylabel('BOX length [$\AA$]', fontsize=10)
    plt.grid()


def plot_ener_test(data_df):
    """
    Generates plots for key AIMD metrics from a DataFrame.

    Args:
        data_df (pandas.DataFrame): A DataFrame containing the AIMD simulation data.
                                   It must include 'Time[fs]', 'Temp[K]', 'Kin.[a.u.]',
                                   'Pot.[a.u.]', and 'UsedTime[s]' columns.
    """
    # First, check if the input is a valid DataFrame
    if data_df is None or data_df.empty:
        print("Input is not a valid DataFrame. Nothing to plot.")
        return

    #print("Generating plots...")

    # Define the plots to create
    plots_to_generate = [
        {'y_col': 'Temp[K]', 'y_label': 'Temperature [K]'},
        {'y_col': 'Kin.[a.u.]', 'y_label': 'KE [a.u.]'},
        {'y_col': 'Pot.[a.u.]', 'y_label': 'PE [a.u.]'},
        {'y_col': 'UsedTime[s]', 'y_label': 'UsedTime [s]'}
    ]

    # Check if required columns exist before trying to plot
    required_cols = ['Time[fs]'] + [p['y_col'] for p in plots_to_generate]
    if not all(col in data_df.columns for col in required_cols):
        print(f"Error: DataFrame is missing one or more required columns: {required_cols}")
        return

    # Loop and create each plot
    for plot_info in plots_to_generate:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(data_df['Time[fs]'], data_df[plot_info['y_col']], color='black')
        ax.set_xlabel('Time [fs]', fontsize=10)
        ax.set_ylabel(plot_info['y_label'], fontsize=10)
        ax.grid(True)