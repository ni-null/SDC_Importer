import os
import pandas as pd


def run_process(base_path, pt=None, uid_product_array=None):
    pt(f"#### run_process ####\n")
    # 獲取當前工作目錄下的所有檔案列表

    files_path = os.path.join(base_path, "sdc/state")  # 檔案所在目錄

    print(base_path)

    # 創建 DataFrame
    df = pd.DataFrame(uid_product_array, columns=["Match"])

    # 檢查 files_path 目錄是否存在，不存在則創建
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    # 將 DataFrame 寫入 CSV 檔案
    csv_file_path = os.path.join(files_path, "matches.csv")
    df.to_csv(csv_file_path, index=False)

    pt(f"CSV 檔案已成功創建，位置: {csv_file_path}")
