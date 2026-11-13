#!/usr/bin/env python3
"""scientists-side/*.md を index.html に埋め込む（file:// で開いたときの初期値）。

使い方:  python3 scientists-side/tools/embed.py
.md を書き換えたら実行してください。GitHub Pages やローカルサーバーで開くときは .md を直接読むので、なくても動きます。
"""
import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
files = ['scenario.md', 'map.md', 'characters.md', 'items.md', 'enemies.md']
blocks = []
for f in files:
    text = (root / f).read_text(encoding='utf-8').replace('</script', '<\\/script')
    blocks.append(f'<script type="text/markdown" data-file="{f}">\n{text}</script>')
html_path = root / 'index.html'
html = html_path.read_text(encoding='utf-8')
new = re.sub(r'<!--EMBED-START-->.*?<!--EMBED-END-->',
             lambda _: '<!--EMBED-START-->\n' + '\n'.join(blocks) + '\n<!--EMBED-END-->',
             html, flags=re.S)
html_path.write_text(new, encoding='utf-8')
print('embedded', len(files), 'files')
