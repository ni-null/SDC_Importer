import requests
import time
import json
import os

 

def trigger_job(cron_trigger_url,cron_trigger_cancel_url,pt):
    max_attempts = 3
    retry_interval = 5  # seconds

    for attempt in range(1, max_attempts + 1):
        try:
            trigger_response = requests.get(cron_trigger_url, timeout=10) 
            
            if trigger_response.json().get("status") == 200 :
                
                pt(f"Trigger ※ 呼叫成功")
                pt(f"Response data : {trigger_response.text}\n") 
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
                
        except (requests.ConnectionError, requests.Timeout) as e:
            pt(f"嘗試 {attempt}/3: 網路異常 - {e}")
            
        except requests.exceptions.RequestException as e:
            pt(f"嘗試 {attempt}/3: 請求失敗 - {e} \n")
            time.sleep(retry_interval)

    raise ValueError("警告: 停止運行，Trigger呼叫錯誤")


def processing_job(cron_processing_url,pt):
    max_retries = 3
    retry_count = 0
    pt(f"Processing ※ 執行中") 

    while retry_count < max_retries:

        try:
            response = requests.get(cron_processing_url, timeout=180)
            pt(f"Response data : {response.text}") 
            responseData = response.json()
            # 響應成功，重設 retry_count
            retry_count = 0
            if responseData.get('status')==403:  
                pt(f"\nProcessing任務完成")
                break
            
        except requests.Timeout:
            retry_count += 1  # 發生超時錯誤後增加重試次數
            pt(f"Timeout error ({retry_count}/{max_retries}): 請求超時，等待{timeout}秒")
            if retry_count < max_retries:
                time.sleep(10)  # 避免由於連接問題造成過度重試
            else:
                pt("警告: 停止運行，Processing超過錯誤上限")
                break
            
        except requests.RequestException as e:
            retry_count += 1
            pt(f"Request error ({retry_count}/{max_retries}):" )
            pt(f"{e}")
            if retry_count < max_retries:
                time.sleep(10)  # 避免由於連接問題造成過度重試
            else:
                ValueError("警告: 停止運行，Processing超過錯誤上限")
                break

            continue


def run_process(param,pt=None, config_data=None):
    pt(f"#### 任務調用 ####\n") 
    trigger_job(f"{config_data['cron_url']}&action=trigger",f"{config_data['cron_url']}&action=cancel",pt)

    processing_job(f"{config_data['cron_url']}&action=processing",pt)
