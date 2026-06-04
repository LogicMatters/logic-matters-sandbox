#!/usr/bin/env python3
"""Pre-render script: generates _recent_posts.md with the 3 most recent blog post links."""
import os
import re
from datetime import datetime

blog_dir = "blog"
posts = []

for fname in os.listdir(blog_dir):
    if not fname.endswith(".qmd") or fname == "index.qmd":
        continue

    with open(os.path.join(blog_dir, fname), encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        continue

    end = content.find("\n---", 3)
    if end < 0:
        continue

    yaml_text = content[3:end]

    title_m = re.search(r'^title:\s*"([^"]+)"', yaml_text, re.MULTILINE)
    if not title_m:
        title_m = re.search(r"^title:\s*'([^']+)'", yaml_text, re.MULTILINE)
    if not title_m:
        title_m = re.search(r"^title:\s*(.+)", yaml_text, re.MULTILINE)

    date_m = re.search(r'^date:\s*"?(\d{4}-\d{2}-\d{2})"?', yaml_text, re.MULTILINE)

    if title_m and date_m:
        posts.append({
            "title": title_m.group(1).strip().strip("'\""),
            "date": date_m.group(1),
            "slug": fname[:-4],
        })

posts.sort(key=lambda p: p["date"], reverse=True)

parts = []
for post in posts[:3][::-1]:
    dt = datetime.strptime(post["date"], "%Y-%m-%d")
    date_fmt = dt.strftime("%-d %B %Y")
    parts.append(f"[{post['title']}](blog/{post['slug']}.qmd) ({date_fmt})")

new_content = "Recent posts: " + ", ".join(parts) + "\n"
try:
    with open("_recent_posts.md", "r", encoding="utf-8") as f:
        old_content = f.read()
except FileNotFoundError:
    old_content = ""

if new_content != old_content:
    with open("_recent_posts.md", "w", encoding="utf-8") as f:
        f.write(new_content)

render_time = datetime.now().strftime("%B %-d @ %H.%M")
with open("_render_time.md", "w", encoding="utf-8") as f:
    f.write(f"*Site updated: {render_time}*\n")
