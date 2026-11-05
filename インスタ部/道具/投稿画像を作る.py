"""使い方: python3 投稿画像を作る.py 原本.png 出力.png 上五 中七 下五
背景 #F1F1EF、右上に縦書きの句、左下に絵、右下に「ダル竜」の 2160×2700px の画像を作る。"""
import sys,pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
art,out,*lines=sys.argv[1:]
root=pathlib.Path(__file__).resolve().parents[1]
font=root/'素材/フォント/Yomogi-Regular.ttf'
o=Image.open(art).convert('RGBA');x0,y0,x1,y1=o.getchannel('A').getbbox()
s=min(0.316,936/(x1-x0))
l=64-x0*s;t=1238-y1*s;w=o.width*s
txt=''.join(f'<div class=l style="margin-top:{i}em">{v}</div>' for i,v in enumerate(lines))
html=f'''<!doctype html><html lang=ja><meta charset=utf-8><style>@font-face{{font-family:A;src:url(file://{font})}}*{{margin:0}}html,body{{width:1080px;height:1350px;background:#F1F1EF;overflow:hidden;position:relative;color:#454545;font-family:A}}
.h{{z-index:2;position:absolute;top:88px;right:96px;display:flex;flex-direction:row-reverse;gap:40px;font-size:60px;line-height:1}}.l{{writing-mode:vertical-rl;letter-spacing:.1em}}
img{{position:absolute;left:{l}px;top:{t}px;width:{w}px;height:{w}px}}.c{{position:absolute;right:72px;bottom:52px;font-size:28px;letter-spacing:.1em}}</style>
<div class=h>{txt}</div><img src="file://{pathlib.Path(art).resolve()}"><div class=c>ダル竜</div></html>'''
t_=pathlib.Path(out).with_suffix('.html');t_.write_text(html,encoding='utf8')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
    pg.goto(f'file://{t_.resolve()}');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(400);pg.screenshot(path=out);b.close()
t_.unlink()
