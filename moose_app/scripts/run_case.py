#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import sys,json,hashlib,subprocess,time,os
from decks import make,ROOT
RUNTIME=ROOT/'.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run(name,**kwargs):
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        deck=Path(tmp)/'input.i';config=make(deck,**kwargs);text=deck.read_text()
    return run_input(name,text,config)

def run_input(name,text,config):
    out=RUNTIME/name
    if (out/'provenance.json').exists():
        prior=json.loads((out/'provenance.json').read_text())
        if prior['exit_code']==0 and prior['binary_sha256']==sha(ROOT/'moose_app/anisotropic_biot-opt'):return out
        raise RuntimeError(f'Refusing to overwrite existing evidence {out}')
    out.mkdir(parents=True,exist_ok=True);deck=out/'input.i';deck.write_text(text)
    command=[str(ROOT/'moose_app/anisotropic_biot-opt'),'-i',str(deck),f'Outputs/file_base={out}/solution','--n-threads=1']
    start=time.time()
    with (out/'run.log').open('w') as log:
        proc=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    provenance=dict(case=name,configuration=config,command=command,exit_code=proc.returncode,seconds=time.time()-start,input_sha256=sha(deck),binary_sha256=sha(ROOT/'moose_app/anisotropic_biot-opt'),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'moose_app').glob('**/*')) if p.suffix in ['.C','.h'] and 'build' not in p.parts},outputs={p.name:sha(p) for p in out.glob('*') if p.is_file() and p!=out/'provenance.json'})
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(name,proc.returncode,round(provenance['seconds'],2),flush=True)
    if proc.returncode:raise RuntimeError(f'{name} failed; see {out}/run.log')
    return out
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('--nx',type=int,default=10);ap.add_argument('--ny',type=int,default=2);ap.add_argument('--dt',type=float,default=.001);ap.add_argument('--end',type=float,default=.2);ap.add_argument('--load',type=float,default=1e-4);ap.add_argument('--linear',action='store_true');ap.add_argument('--case',default='mandel');ap.add_argument('--angle',type=float,default=0);a=vars(ap.parse_args());run(**a)
