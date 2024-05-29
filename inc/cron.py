import requests
import time
import json
import os

 

def trigger_job(cron_trigger_url,pt):
    max_attempts = 3
    retry_interval = 5  # seconds

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(cron_trigger_url)
            if response.status_code == 200 or "already triggered. Request skipped" in response.json().get("message", ""):

                pt(f"Trigger呼叫成功，Processing執行中")
                return True  # Trigger successful, exit function
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

    while retry_count < max_retries:
        retry_count += 1

        try:
            response = requests.get(cron_processing_url)
            pt(f"Response data:{response.text}") 

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


def run_process(param,pt=None):
    pt(f"#### 任務調用 ####\n")
    
    config_path = os.path.join(param, "config.json")
    
    with open(config_path, "r") as f:
        config_data = json.load(f)
        
         
    trigger_job(config_data["update"]["trigger_url"],pt)

    processing_job(config_data["update"]["processing_url"],pt)
