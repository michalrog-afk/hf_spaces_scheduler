import os
import requests
from datetime import datetime
from pathlib import Path
from huggingface_hub import (
    HfApi,
    hf_hub_download,
    login
)
import tempfile
import shutil


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


def download_and_backup_webui():
    print("开始从 Hugging Face 下载文件...")
    token = os.environ['HF_TOKEN']
    user = os.environ['HF_USER']
    space = os.environ['HF_SPACE']
    repo_id = f"{user}/{space}"
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # 在临时目录中创建data文件夹
            temp_data_dir = Path(temp_dir) / "data"
            temp_data_dir.mkdir(parents=True, exist_ok=True)
            
            # 从HF space下载webui.db到临时目录
            local_path = hf_hub_download(
                repo_id=repo_id,
                filename="data/webui.db",
                repo_type="space",
                token=token,
                local_dir=temp_dir  # 指定下载到临时目录
            )
            
            # 执行WebDAV备份
            webdav_username = os.environ.get('WEBDAV_USERNAME')
            webdav_password = os.environ.get('WEBDAV_PASSWORD')
            webdav_url = os.environ.get('WEBDAV_URL')
            
            # 生成带时间戳的文件名
            filename = f"webui_{datetime.now().strftime('%m_%d_%H%M')}.db"
            auth = (webdav_username, webdav_password)
            
            # 上传备份文件
            with open(local_path, 'rb') as f:
                response = requests.put(
                    f"{webdav_url}/{filename}",
                    data=f,
                    auth=auth
                )
                response.raise_for_status()
            print(f"WebDAV 备份成功: {filename}")

            # 更新主文件
            with open(local_path, 'rb') as f:
                response = requests.put(
                    f"{webdav_url}/webui.db",
                    data=f,
                    auth=auth
                )
                response.raise_for_status()
            print("WebDAV 更新主文件成功")
            return True
            
        except Exception as e:
            print(f"操作失败: {e}")
            return False
        # 临时目录会在with块结束后自动删除


if __name__ == "__main__":
    # 先从HF下载
    if download_and_backup_webui():
        restart_space()
    else:
        print("备份失败，取消重启操作")
        exit(1)
