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
    # 重启hf
    # try:
    #     HfApi().restart_space(repo_id=repo_id, token=token)
    #     print(f"Successfully restarted Space: {repo_id}")
    # except Exception as e:
    #     print(f"Failed to restart Space {repo_id}: {e}")
    
    #重构hf
    try:
        HfApi().restart_space(repo_id=repo_id, token=token, factory_reboot=True)
        print(f"Successfully rebuild Space: {repo_id}")
    except Exception as e:
        print(f"Failed to rebuild Space {repo_id}: {e}")

if __name__ == "__main__":
   
    restart_space()
