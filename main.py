import asyncio
import os
import random
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile; rv:109.0) Gecko/118.0 Firefox/118.0"
}

async def simulate_watch(session, video_url):
    print(f"[INFO] Visiting: {video_url}")
    try:
        async with session.get(video_url, headers=HEADERS, timeout=15) as resp:
            if resp.status == 200:
                watch_time = random.randint(10, 30)
                print(f"[INFO] Simulating watch for {watch_time} seconds...")
                await asyncio.sleep(watch_time)
            else:
                print(f"[WARN] Failed to fetch video ({resp.status})")
    except Exception as e:
        print(f"[ERROR] {e}")

async def main():
    # Load video URLs from file
    if not os.path.exists("videos.txt"):
        print("[ERROR] videos.txt not found! Please create it with one YouTube URL per line.")
        return

    with open("videos.txt") as f:
        video_urls = [line.strip() for line in f if line.strip()]

    if not video_urls:
        print("[ERROR] videos.txt is empty!")
        return

    proxy = os.getenv("PROXY")
    connector = ProxyConnector.from_url(proxy) if proxy else None

    async with ClientSession(connector=connector) as session:
        print(f"[INFO] Loaded {len(video_urls)} video(s) from videos.txt")
        for video in video_urls:
            await simulate_watch(session, video)

        print("[INFO] All videos processed.")

if __name__ == "__main__":
    asyncio.run(main())
