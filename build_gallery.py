import os
import re
import json

series_meta = [
    ('flower', '🌷小花仙子们会有香香的味道吗🌻', '🌸 小花仙子'),
    ('xmas', '🎄圣诞佳节！', '🎄 圣诞佳节'),
    ('sleep', '帝王睡相', '👑 帝王睡相'),
    ('foryou', '给你的☺️', '🎁 给你的'),
    ('dog', '好可爱的16个小狗呀^ ^', '🐶 可爱小狗'),
    ('hot', '很热！！！！！', '🔥 很热'),
    ('rain', '老天爷你别下了我害怕', '🌧️ 老天爷别下了'),
    ('food', '朋友帮我带了饭回来但我不敢吃', '🍱 朋友带饭不敢吃'),
    ('aunt', '七个老姨算一难', '👵 七个老姨算一难'),
    ('cool', '前途一片阴暗 好凉快', '🕶️ 前途阴暗好凉快'),
    ('sorry', '请原谅(^з^)-☆', '🙏 请原谅'),
    ('cube', '是不是有点太棱角分明了老师', '📐 棱角分明'),
    ('xllp', '是xllp表情包！这下不得不用了！', '🐱 暹罗厘普精选'),
    ('know', '我全都知道了', '👀 我全都知道了'),
    ('who', '这样的表情到底是谁在用啊？', '❓ 谁在用这样的表情'),
    ('summer', '征集高效的解暑招数 被采纳者将被采纳', '🧊 解暑招数'),
]

series_slug_map = {orig: slug for slug, orig, desc in series_meta}

files = [f for f in os.listdir('.') if f.endswith('.jpg')]
pattern = re.compile(r'^(.+)_(\d+)_(.+)\.jpg$')

groups = {}
for f in files:
    m = pattern.match(f)
    if not m:
        continue
    series, idx = m.group(1), int(m.group(2))
    slug = series_slug_map.get(series)
    if slug:
        groups.setdefault(slug, []).append((idx, f, series))

mapping_records = []
gallery_sections = []

for slug, orig_title, display_title in series_meta:
    items = groups.get(slug, [])
    items.sort(key=lambda x: x[0])  # sort by original index
    
    gallery_rows = []
    current_row = []
    
    for i, (orig_idx, old_filename, orig_series) in enumerate(items):
        new_filename = f"{slug}-{i+1:02d}.jpg"
        mapping_records.append({
            'new_name': new_filename,
            'original_name': old_filename,
            'series': orig_series,
            'series_slug': slug,
            'order_index': i + 1,
            'raw_url': f"https://raw.githubusercontent.com/wilderye/avatars/main/{new_filename}",
            'jsdelivr_url': f"https://cdn.jsdelivr.net/gh/wilderye/avatars@main/{new_filename}"
        })
        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)
        
        current_row.append(f'<img src="./{new_filename}" width="140" /><br><code>{new_filename}</code>')
        if len(current_row) == 4:
            gallery_rows.append(' | '.join(current_row))
            current_row = []
            
    if current_row:
        while len(current_row) < 4:
            current_row.append(' ')
        gallery_rows.append(' | '.join(current_row))
        
    table_md = f"### {display_title} (`{slug}`) - {len(items)} 张\n\n"
    table_md += "| 预览 | 预览 | 预览 | 预览 |\n"
    table_md += "| :---: | :---: | :---: | :---: |\n"
    for r in gallery_rows:
        table_md += f"| {r} |\n"
    table_md += "\n"
    gallery_sections.append(table_md)

with open('mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_records, f, ensure_ascii=False, indent=2)

readme_content = """# 🎭 Avatars & Stickers Gallery

个人自用表情包 / 角色头像外链图库（暹罗厘普系列共 100 张）。用于酒馆 (SillyTavern) 角色卡、各种 Bot 匿名头像、论坛及日常聊天。

## 🔗 外链地址格式

替换末尾的 `<文件名>` 为下表对应的图片名即可（如 `dog-01.jpg`）：

* **GitHub Raw (原始直链)**:
  ```text
  https://raw.githubusercontent.com/wilderye/avatars/main/<文件名>
  ```
* **jsDelivr CDN (国内高速免翻墙推荐)**:
  ```text
  https://cdn.jsdelivr.net/gh/wilderye/avatars@main/<文件名>
  ```

---

## 🖼️ 图片画廊

""" + '\n'.join(gallery_sections)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print(f"Successfully processed {len(mapping_records)} files.")
