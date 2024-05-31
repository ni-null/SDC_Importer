import os
import pandas as pd


def run_process(files_path, pt=None):
    pt(f"#### 合併符合的CSV檔案 ####\n")
    # 獲取當前工作目錄下的所有檔案列表

    # 檔案所在目錄
    file_list = os.listdir(files_path)

    combined_data = pd.DataFrame()  # 合併後的資料
    all_columns = set()  # 存儲所有檔案的標題行集合
    columns_with_attributes = []  # 属性的列索引和名字
    sum_num = 0  # 加總筆數
    process_file_num = 0

    # 迭代處理每個檔案，同時檢查標題行

    for file_name in file_list:
        if file_name.endswith(".csv") and file_name.startswith(
            "survey_item_list_"
        ):  # 排除 product_update.csv
            file_path = os.path.join(files_path, file_name)

            # 讀取CSV檔案
            process_file_num += 1
            df = pd.read_csv(file_path)

            # 計算資料筆數（排除標題行）
            num_rows = len(df)
            sum_num = sum_num + num_rows

            pt(f"{num_rows:04d}筆 --- {file_name}")

            # 将标题行添加到集合中
            all_columns.add(tuple(df.columns))

            # 查找包含特定属性的列索引和名字

            attribute_keywords = ["屬性", "分類", "標籤"]

            for col_index, col_name in enumerate(df.columns):
                if any(keyword in col_name for keyword in attribute_keywords):
                    if col_index not in columns_with_attributes:
                        columns_with_attributes.append(
                            (col_index, col_name)
                        )  # 记录列索引和名字

            # 替換指定列中的逗號為竖线並刪除空格
            for col_index in [col_index for col_index, _ in columns_with_attributes]:
                if len(df.columns) > col_index:
                    col_name = df.columns[col_index]
                    df[col_name] = df[col_name].apply(
                        lambda x: (
                            x
                            if pd.isna(x)
                            else str(x).replace(",", "|").replace(" ", "")
                        )
                    )

            # 如果是第一個檔案，保留標題行，否則不保留
            if combined_data.empty:
                combined_data = df
            else:
                combined_data = pd.concat([combined_data, df], ignore_index=True)

    #
    if process_file_num == 0:
        delete_file_path = os.path.join(files_path, "product_update.csv")
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)
            pt(f"發現舊『product_update.csv』已刪除")
        raise ValueError("警告:停止運行，沒發現可用檔案")

    # 檢查所有檔案的標題行是否一致
    if len(all_columns) > 1:
        raise ValueError("警告:停止運行，檢測到檔案標題不一致")
    else:
        pt("\n檢查格式 :  所有檔案中的標題行都是一致的")

        # 儲存合併後的結果到一個新的CSV檔案
        product_update_path = os.path.join(files_path, "product_update.csv")
        combined_data.to_csv(product_update_path, index=False, encoding="utf-8-sig")

    pt(f"\n檔案已經合併，共有{sum_num}筆資料\n\n")
