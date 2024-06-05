import os
import pandas as pd


def run_process(base_path, pt=None, uid_product_array=None, state_str=None):

    pt(f"#### 產生 product_state.csv ####\n")

    # 獲取當前工作目錄下的所有檔案列表
    if not uid_product_array:
        raise ValueError("警告:停止運行，無符合的UID格式")
    else:
        product_state_text = ""
        if state_str == "publish":
            pt(f"選擇格式『上架』\n")
            pt(f"{"UID : " + ", ".join(uid_product_array)}\n")
            product_state_text = ""
        elif state_str == "trash":
            pt(f"選擇格式『下架』\n")



    # 創建 DataFrame
    df = pd.DataFrame(uid_product_array, columns=["Meta: uid"])
    df["status"] = state_str 

    # 檢查 files_path 目錄是否存在，不存在則創建
    files_path = os.path.join(base_path, "sdc_data/state")  # 檔案所在目錄
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    # 將 DataFrame 寫入 CSV 檔案
    csv_file_path = os.path.join(files_path, "product_state.csv")
    df.to_csv(csv_file_path, index=False)

    pt(f"CSV 檔案已成功創建\n\n")
