import os, mimetypes, aiofiles
from tenacity import retry, wait_exponential, stop_after_attempt

def iter_media_files(directory: str) -> list[str]:
    if not directory or not os.path.isdir(directory):
        return []
    files = []
    for root, _, names in os.walk(directory):
        for n in sorted(names):
            p = os.path.join(root, n)
            mt, _ = mimetypes.guess_type(p)
            if mt in {"image/jpeg","image/png","image/webp","video/mp4","image/gif"}:
                files.append(p)
    return files

@retry(wait=wait_exponential(min=1, max=30), stop=stop_after_attempt(5))
async def send_media(bot, chat_id: int, path_or_url: str, caption: str | None = None):
    mt, _ = mimetypes.guess_type(path_or_url)
    mt = mt or ""
    if path_or_url.startswith("http"):
        if "video" in mt or path_or_url.endswith((".mp4",".mov",".m4v",".gifv")):
            await bot.send_video(chat_id=chat_id, video=path_or_url, caption=caption)
        else:
            await bot.send_photo(chat_id=chat_id, photo=path_or_url, caption=caption)
    else:
        if "video" in mt or path_or_url.endswith((".mp4",".mov",".m4v",".gifv")):
            async with aiofiles.open(path_or_url, "rb") as f:
                await bot.send_video(chat_id=chat_id, video=await f.read(), caption=caption)
        else:
            async with aiofiles.open(path_or_url, "rb") as f:
                await bot.send_photo(chat_id=chat_id, photo=await f.read(), caption=caption)
