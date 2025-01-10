import cloudinary
import cloudinary.uploader as uploader
from fastapi import UploadFile

from src.config import Config

cloudinary.config(
    cloud_name=Config.CLOUD_NAME,
    api_key=Config.CLOUDNARY_API_KEY,
    api_secret=Config.CLOUDNARY_API_SECRET,
    secure=True,
)


async def uploadUserProfile(image: UploadFile) -> str:
    try:
        result = uploader.upload(
            image.file,
            folder="users_profiles/",
        )
        return result["secure_url"]
    except:
        return "https://cdn-icons-png.flaticon.com/512/9187/9187604.png"
