#!/usr/bin/env python3
"""Provide missing LuaLaTeX font support in ignored local runtime storage.

The normal dependency is a complete TeX Live LuaLaTeX installation. This
Ubuntu/Debian fallback downloads and unpacks texlive-luatex without changing
system packages. The repository latexmk configuration discovers the result.
"""
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'.agent-runtime/latex-packages'
LOCAL=CACHE/'extracted/usr/share/texlive/texmf-dist'


def main():
    if (LOCAL/'tex/luatex/luaotfload/luaotfload-main.lua').is_file():
        print('Local LuaLaTeX support is available.');return
    if shutil.which('kpsewhich') and subprocess.run(['kpsewhich','luaotfload-main.lua'],stdout=subprocess.DEVNULL).returncode==0:
        print('System LuaLaTeX support is available.');return
    if not all(shutil.which(x) for x in ('apt-get','dpkg-deb')):
        raise SystemExit('Install the LuaLaTeX component of TeX Live with your platform package manager.')
    CACHE.mkdir(parents=True,exist_ok=True)
    subprocess.run(['apt-get','download','texlive-luatex'],cwd=CACHE,check=True)
    packages=sorted(CACHE.glob('texlive-luatex_*.deb'),key=lambda p:p.stat().st_mtime)
    if not packages:raise SystemExit('No downloaded texlive-luatex package found.')
    subprocess.run(['dpkg-deb','-x',str(packages[-1]),str(CACHE/'extracted')],check=True)
    if not (LOCAL/'tex/luatex/luaotfload/luaotfload-main.lua').is_file():
        raise SystemExit('The package does not contain the expected LuaLaTeX support.')
    print('Local LuaLaTeX support unpacked; run the normal latexmk command.')

if __name__=='__main__':main()
