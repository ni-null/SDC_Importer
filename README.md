### 流程

1. 合併survey_item_list開頭CSV檔案
2. 上傳合併後的檔案
3. 觸發API


### 打包

```
git clone  https://github.com/ni-null/SDC_Importer.git 
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

### 運行
初次運行會自動於同目錄下建立sdc_data檔案  
![Snipaste_2024-08-28_12-17-25](https://github.com/user-attachments/assets/a69b3762-2ba7-4510-9f8a-df1a92b2665a)


運行log於app.log  
![Snipaste_2024-08-28_12-17-31](https://github.com/user-attachments/assets/8b873c45-3b86-47df-971c-fe3ddab42728)



### 狀態
需出現 Response data : {"status":200,"message":"Import # complete"} 才表示完整執行成功  
![Snipaste_2024-08-28_12-16-01](https://github.com/user-attachments/assets/8cbd7a97-e54b-4675-8cac-852c61af94f6)
