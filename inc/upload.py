from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import requests
import os
import time
import json


def format_file_size(total_size):
    if total_size >= 1024 * 1024:
        size_mb = total_size / (1024 * 1024)
        return f"{size_mb:.2f} MB"
    else:
        size_kb = total_size / 1024
        return f"{size_kb:.2f} KB"


def upload_from_file(src, dst, pt=None, progress_callback=None):
    total_size = os.path.getsize(src)
    uploaded = 0

    pt(f"檔案大小 : {str(format_file_size(total_size))}")

    def callback(monitor):
        nonlocal uploaded
        uploaded = monitor.bytes_read
        progress = uploaded / total_size * 100
        # pt(f"Upload progress: {progress:.2f}%")
        if progress < 100 and progress_callback:
            progress_callback(progress)

    with open(src, "rb") as file:
        encoder = MultipartEncoder({"file": (os.path.basename(src), file)})
        monitor = MultipartEncoderMonitor(encoder, callback)

        headers = {"Content-Type": monitor.content_type}
        response = requests.post(dst, data=monitor, headers=headers)


def run_process(local_file_path, pt=None, config_data=None, progress_callback=None):
    pt(f"#### 檔案上傳中 ####\n")
    retries = 0
    max_retries = 3
    success = False

    while retries < max_retries and not success:
        SRC = local_file_path
        DST = config_data["file_upload_url"]

        try:
            upload_from_file(SRC, DST, pt, progress_callback)
            success = True
            pt(f"\n檔案上傳成功\n\n ")
            if progress_callback:
                progress_callback(100)

        except Exception as e:
            pt(f"第 {retries+1}/3 次嘗試失敗")
            pt(f"上傳失敗，錯誤訊息: \n{str(e)}\n")
            retries += 1

            if retries < max_retries:
                time.sleep(5)

    if not success:
        if progress_callback:
            progress_callback(0)
        raise ValueError("警告: 停止運行，上傳錯誤")
