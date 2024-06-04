import requests
import time
import json
import os

 

def trigger_job(cron_trigger_url,cron_trigger_cancel_url,pt):
    max_attempts = 3
    retry_interval = 5  # seconds

    for attempt in range(1, max_attempts + 1):
        try:
            trigger_response = requests.get(cron_trigger_url) 
            
            if trigger_response.json().get("status") == 200 :
                
                pt(f"Trigger ※ 呼叫成功")
                pt(f"Response data : {trigger_response.json().get("message")}\n") 
                return True  
            
            elif "already triggered" in trigger_response.json().get("message", "") :
                
                trigger_cancel_response =  requests.get(cron_trigger_cancel_url)
           
                if "canceled" in trigger_cancel_response.json().get("message", "") :
                    pt(f"Trigger ※ 取消舊有任務")
                    pt(f"Response data : {trigger_cancel_response.json().get("message")}\n") 
                    attempt = 0
                
            else:
                pt(f"Attempt {attempt}: Retry after {
                      retry_interval} seconds")
                time.sleep(retry_interval)
        except requests.exceptions.RequestException as e:
            pt(f"嘗試 {attempt}/3: 請求失敗 - {e} \n")
            time.sleep(retry_interval)

    raise ValueError("警告: 停止運行，Trigger呼叫錯誤")


def processing_job(cron_processing_url,pt):
    max_retries = 5
    retry_count = 0
    pt(f"Processing ※ 執行中") 

    while retry_count < max_retries:
        retry_count += 1

        try:
            
            response = requests.get(cron_processing_url)
            pt(f"Response data : {response.text}") 

        except requests.RequestException as e:
            pt(f"Request error ({retry_count}/{max_retries}):" )
            pt(f"{e}")
            if retry_count < max_retries:
                time.sleep(10)  # 避免由於連接問題造成過度重試
            else:
                ValueError("警告: 停止運行，Processing超過嘗試上限")
                break

            continue

        if "is not triggered. Request skipped." in response.text:
            pt(f"\nProcessing任務完成")
            break


def run_process(param,pt=None, config_data=None):
    pt(f"#### 任務調用 ####\n") 
    trigger_job(f"{config_data['cron_url']}&action=trigger",f"{config_data['cron_url']}&action=cancel",pt)

    processing_job(f"{config_data['cron_url']}&action=processing",pt)
