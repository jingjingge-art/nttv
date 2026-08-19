#!/usr/bin/env python3
"""
每次运行下载并解析 M3U 播放列表，输出到仓库根目录：
  - streams.json
  - streams.csv

目标 URL: https://iptv.1989.click/playlist.m3u
"""
import re
import csv
import json
import sys
from typing import List, Dict
import requests

M3U_URL = "https://iptv.1989.click/playlist.m3u"
JSON_PATH = "streams.json"
CSV_PATH = "streams.csv"
TIMEOUT = 30

ATTR_RE = re.compile(r'(\w+)="([^\"]*)"')
EXTINF_RE = re.compile(r'^#EXTINF:[^\n]*,(.*)$')

def fetch_m3u(url: str) -> str:
    resp = requests.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.text

def parse_m3u(text: str) -> List[Dict]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() != ""]
    items: List[Dict] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            m_name = EXTINF_RE.match(line)
            display_name = m_name.group(1).strip() if m_name else ""
            attrs = dict(ATTR_RE.findall(line))
            url = ""
            j = i + 1
            while j < len(lines):
                if not lines[j].startswith("#"):
                    url = lines[j]
                    break
                j += 1
            item = {
                "name": display_name,
                "url": url,
                "tvg-id": attrs.get("tvg-id") or attrs.get("tvgname") or "",
                "tvg-name": attrs.get("tvg-name") or "",
                "tvg-logo": attrs.get("tvg-logo") or attrs.get("logo") or "",
                "group-title": attrs.get("group-title") or "",
                "extinf": line,
            }
            items.append(item)
            i = j + 1
            continue
        i += 1
    return items

def save_json(items: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def save_csv(items: List[Dict], path: str):
    if not items:
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        return
    fieldnames = ["name", "url", "tvg-id", "tvg-name", "tvg-logo", "group-title"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            row = {k: it.get(k, "") for k in fieldnames}
            writer.writerow(row)

def main():
    try:
        text = fetch_m3u(M3U_URL)
    except Exception as e:
        print(f"下载 M3U 失败: {e}", file=sys.stderr)
        sys.exit(2)
    items = parse_m3u(text)
    save_json(items, JSON_PATH)
    save_csv(items, CSV_PATH)
    print(f"解析完成，写入: {JSON_PATH} ({len(items)} 条), {CSV_PATH}")

if __name__ == "__main__":
    main()
