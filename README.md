### 介紹

一個基於 WP All Import 創作的上傳更新工具 sdc.org.tw

1. 合併 survey_item_list 多個開頭 CSV 檔案 ，轉換欄位格式
2. 上傳合併後的檔案
3. 觸發 API 更新

### 打包

```
git clone  https://github.com/ni-null/SDC_Importer.git
pip install -r requirements.txt

```

建立 config.json 於根目錄

```
{
  "product_update_text": {
    "file_upload_url": "",
    "cron_url": ""
  },

  "product_update_text_with_img": {
    "file_upload_url": "",
    "cron_url": ""
  },

  "product_state": {
    "file_upload_url": "",
    "cron_url": ""
  }
}

```

```
python build.py
```

### 運行

初次運行會自動於同目錄下建立 sdc_data 檔案  
![Snipaste_2024-08-28_12-17-25](https://github.com/user-attachments/assets/a69b3762-2ba7-4510-9f8a-df1a92b2665a)

運行 log 於 app.log  
![Snipaste_2024-08-28_12-17-31](https://github.com/user-attachments/assets/8b873c45-3b86-47df-971c-fe3ddab42728)

### 狀態

需出現 Response data : {"status":200,"message":"Import # complete"} 才表示完整執行成功  
運行中需保持網路通順(多次錯誤會停止)  
![Snipaste_2024-08-28_12-16-01](https://github.com/user-attachments/assets/8cbd7a97-e54b-4675-8cac-852c61af94f6)
