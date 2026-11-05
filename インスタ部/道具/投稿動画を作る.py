"""使い方: python3 投稿動画を作る.py 投稿画像.png 出力.mp4
投稿画像を 1080×1920px の中央に置き、ダル竜の音声15秒を付けたリール動画を作る。ffmpeg が必要。"""
import sys,pathlib,subprocess
img,out=sys.argv[1:3]
root=pathlib.Path(__file__).resolve().parents[1]
wav=root/'素材/音声/dalui_kyoryu_575.wav'
subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',img,'-i',str(wav),'-t','15','-r','30','-vf','scale=1080:1350:flags=lanczos,pad=1080:1920:0:285:color=0xF1F1EF','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',out],check=True)
