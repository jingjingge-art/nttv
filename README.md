# IPTV 自动抓取与整理

此仓库包含自动抓取并解析 M3U 播放列表的脚本，定时运行的 GitHub Actions 会每小时更新 streams.json 和 streams.csv 到仓库根目录。

运行说明：

1. 本地运行

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python download_and_parse_m3u.py

2. GitHub Actions

工作流位于 .github/workflows/sync.yml，已配置为每小时运行一次并在有变更时提交到 main（使用 GITHUB_TOKEN）。

注意：请在仓库设置中确保 Actions 有 "Read and write repository contents" 权限，否则 workflow 无法 push 提交。
