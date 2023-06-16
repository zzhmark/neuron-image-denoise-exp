from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import subprocess
import tempfile
import shutil
from v3dpy.loaders import PBD


wkdir = Path(r"D:\rectify")


def raw(name):
    rawdir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st')
    in_file = rawdir / name
    out_file = (wkdir / 'raw_app2' / name).with_suffix('.swc')
    marker = Path(wkdir / 'manual_marker' / (name + '.marker'))
    p = PBD()
    if not marker.exists():
        marker = wkdir / "1024.marker"
        if out_file.exists():
            return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        img = p.load(in_file)
        mi = img.min()
        img = ((img - mi) * (255 / (img.max() - mi))).astype('uint8')
        t1 = Path(tdir) / 'temp.v3dpbd'
        t2 = Path(tdir) / 'temp.swc'
        p.save(t1, img)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1200)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


def my(name):
    in_file = wkdir / 'my_8bit' / name
    out_file = (wkdir / 'my_app2' / name).with_suffix('.swc')
    marker = Path(wkdir / 'manual_marker' / (name + '.marker'))
    if not marker.exists():
        marker = wkdir / "1024.marker"
        if out_file.exists():
            return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {in_file} /o {t} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t, out_file)
        except:
            print(f'{in_file} timeout.')


if __name__ == '__main__':
    files = [i.name for i in (wkdir / 'my_8bit').glob('*.v3dpbd')]
    with Pool(12) as p:
        for res in tqdm(p.imap_unordered(my, files), total=len(files)):
            pass
        # for res in tqdm(p.imap_unordered(raw, files), total=len(files)):
        #     pass