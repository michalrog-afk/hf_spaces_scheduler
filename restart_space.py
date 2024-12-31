import os
import requests
from datetime import datetime
from pathlib import Path
from huggingface_hub import HfApi

def restart_space():
    token = os.environ['HF_TOKEN'] # Please navigate to Settings > Secrets and variables > Actions and define "HF_TOKEN".
    user = os.environ['HF_USER']
    space = os.environ['HF_SPACE']
    repo_id = f"{user}/{space}" #  Please replace this value with the name of your own Hugging Face Space.

    try:
        HfApi().restart_space(repo_id=repo_id, token=token)
        print(f"Successfully restarted Space: {repo_id}")
    except Exception as e:
        print(f"Failed to restart Space {repo_id}: {e}")

def backup_space():
    # 环境变量配置
    webdav_username = os.environ.get('WEBDAV_USERNAME')
    webdav_password = os.environ.get('WEBDAV_PASSWORD')
    webdav_url = os.environ.get('WEBDAV_URL')
    
    print("开始执行备份...")
    db_path = Path("./data/webui.db")
    
    if db_path.exists():
        # 生成带时间戳的文件名
        filename = f"webui_{datetime.now().strftime('%m_%d_%H%M')}.db"
        auth = (webdav_username, webdav_password)
        
        try:
            # 上传备份文件
            with open(db_path, 'rb') as f:
                response = requests.put(
                    f"{webdav_url}/{filename}",
                    data=f,
                    auth=auth
                )
                response.raise_for_status()
            print(f"WebDAV 备份成功: {filename}")

            # 更新主文件
            with open(db_path, 'rb') as f:
                response = requests.put(
                    f"{webdav_url}/webui.db",
                    data=f,
                    auth=auth
                )
                response.raise_for_status()
            print("WebDAV 更新主文件成功")
            return True

        except requests.exceptions.RequestException as e:
            print(f"WebDAV 上传失败: {e}")
            return False
    else:
        print("未找到 webui.db 文件")
        return False


if __name__ == "__main__":
    backup_space()
    restart_space()
