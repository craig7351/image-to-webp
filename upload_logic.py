import requests
import os
import base64
import json
import time

def upload_to_imgbb(image_path, api_key):
    url = "https://api.imgbb.com/1/upload"
    try:
        with open(image_path, "rb") as file:
            payload = {
                "key": api_key,
                "image": base64.b64encode(file.read()),
            }
            response = requests.post(url, data=payload)
            response_json = response.json()
            if response.status_code == 200 and response_json['success']:
                return response_json['data']['url']
            else:
                return None
    except Exception:
        return None

def batch_upload(folder_path, api_key, log_callback=print):
    if not os.path.isdir(folder_path):
        log_callback(f"錯誤: 找不到目錄 {folder_path}")
        return None

    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]
    
    if len(files) > 20:
        log_callback(f"錯誤: 檔案數量 ({len(files)}) 超過上限 20 張！")
        # Raising error here might stop thread if not caught properly in main, 
        # but let's stick to logic to abort.
        raise ValueError(f"Too many files: {len(files)}")

    log_callback(f"找到 {len(files)} 個檔案，準備上傳至 ImgBB...")
    
    results = []
    for idx, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        log_callback(f"[{idx+1}/{len(files)}] 正在上傳 {filename}...")
        
        url = upload_to_imgbb(file_path, api_key)
        if url:
            results.append({"filename": filename, "url": url})
            log_callback(f"  -> 成功: {url}")
        else:
            log_callback(f"  -> 失敗: {filename}")
        
        time.sleep(0.5)
        
    # 產生 output.json
    output_json_path = os.path.join(os.path.dirname(folder_path), "output.json")
    # If folder_path is root like "C:\", dirname might be same or empty, handle carefully.
    # Actually putting output.json alongside the folder usually means parent dir of the target folder.
    # Or maybe inside? The original code put it in dirname(folder_path).
    # Let's check original: os.path.join(os.path.dirname(folder_path), "output.json")
    # If I select "C:\images", results go to "C:\". 
    # If I select "C:\images\out", results go to "C:\images\". 
    # That seems fine.
    
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        log_callback(f"\n上傳完成！紀錄已儲存至: {output_json_path}")
    except Exception as e:
        log_callback(f"\n上傳完成，但無法寫入 JSON: {e}")

    return results
