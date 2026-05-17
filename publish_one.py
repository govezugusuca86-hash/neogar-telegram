#!/usr/bin/env python3
"""Публикует один пост из очереди в Telegram-канал."""

import json, os, sys, requests, io
from pathlib import Path

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

POSTS_FILE = Path(__file__).parent / "posts" / "posts.json"
PROGRESS_FILE = Path(__file__).parent / "posts" / "progress.json"
PHOTOS_DIR = Path(__file__).parent / "photos"


def load_progress():
    try:
        return json.loads(PROGRESS_FILE.read_text())
    except:
        return {"done": []}


def save_progress(prog):
    PROGRESS_FILE.write_text(json.dumps(prog, indent=2))


def tg(method, **kwargs):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
        **kwargs,
        timeout=30,
    )
    d = r.json()
    if not d.get("ok"):
        print(f"TG error: {d.get('description', '?')}")
    return d


def publish(post):
    text = post["text"]
    photo_name = post.get("photo")
    photo_path = PHOTOS_DIR / photo_name if photo_name else None

    if photo_path and photo_path.exists():
        ext = photo_path.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        with open(photo_path, "rb") as f:
            return tg(
                "sendPhoto",
                data={
                    "chat_id": CHANNEL_ID,
                    "caption": text[:1024],
                    "parse_mode": "HTML",
                },
                files={"photo": (photo_name, f, mime)},
            ).get("ok", False)

    return tg(
        "sendMessage",
        json={
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
    ).get("ok", False)


def main():
    posts = json.loads(POSTS_FILE.read_text())
    posts.sort(key=lambda x: x["order"])

    progress = load_progress()
    done = set(progress["done"])
    remaining = [p for p in posts if p["id"] not in done]

    if not remaining:
        print("Все посты опубликованы.")
        return

    post = remaining[0]
    tag = "foto" if post.get("photo") else "text"
    print(f"[{post['order']}/{len(posts)}] {tag} | {post['text'][:60]}...")

    ok = publish(post)
    if ok:
        print("OK")
        progress["done"].append(post["id"])
        save_progress(progress)
    else:
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
