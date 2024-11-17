import base64
import httpx
from config import SECRET_GITHUB, REPO_GITHUB, BRANCH_GITHUB, DIRECTORY_GITHUB, API_URL_GITHUB
from utils.uuid_utils import get_uuid

async def upload_image(image_bytes: bytes, extension: str) -> str:
    try:        
        encoded_img = base64.b64encode(image_bytes).decode('utf-8')
        image_name = f"{get_uuid()}{extension}"
        repo_path = f"{DIRECTORY_GITHUB}{image_name}"
        url = f"{API_URL_GITHUB}/{REPO_GITHUB}/contents/{repo_path}"
        
        data = {
            "message": f"Upload image {image_name}",
            "content": encoded_img,
            "branch": BRANCH_GITHUB
        }

        headers = {
            "Authorization": f"token {SECRET_GITHUB}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=headers)
        
        if response.status_code == 201:
            try:
                data = response.json()
                download_url = data["content"]["download_url"]
                return download_url
            except Exception as e:
                print(f"Error response: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None