"""使い方: python3 tools/render.py 素材.png 出力.png 上五 中七 下五"""
import sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
art, out, *lines = sys.argv[1:]
art = pathlib.Path(art).resolve(); font = pathlib.Path(__file__).with_name('Yomogi-Regular.ttf')
im = Image.open(art); w, h = int(im.width*1.25), int(im.height*1.25)
txt = ''.join(f'<div class=l style="margin-top:{i}em">{l}</div>' for i, l in enumerate(lines))
html = f'''<!doctype html><html lang=ja><meta charset=utf-8><style>@font-face{{font-family:A;src:url(file://{font})}}*{{margin:0}}html,body{{width:1080px;height:1350px;background:#F1F1EF;overflow:hidden;position:relative;color:#454545;font-family:A}}
.h{{z-index:2;position:absolute;top:88px;right:96px;display:flex;flex-direction:row-reverse;gap:40px;font-size:60px;line-height:1}}.l{{writing-mode:vertical-rl;letter-spacing:.1em}}
img{{position:absolute;left:72px;bottom:112px;width:{w}px;height:{h}px}}.c{{position:absolute;right:72px;bottom:52px;font-size:28px;letter-spacing:.1em}}</style>
<div class=h>{txt}</div><img src="file://{art}"><div class=c>ダル竜</div></html>'''
t = pathlib.Path(out).with_suffix('.html'); t.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350}, device_scale_factor=1)
    pg.goto(f'file://{t.resolve()}'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.screenshot(path=out); b.close()
t.unlink()
