#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from concurrent.futures import ThreadPoolExecutor
from run_case import run
jobs=[]
for angle in [0,30,45,90]:jobs.append((f'anisotropic_{angle}',dict(case='anisotropic',angle=angle,nx=16,ny=4,dt=.001,end=.1,load=.7)))
jobs.append(('isotropic',dict(case='isotropic',nx=16,ny=4,dt=.001,end=.1,load=.7)))
for angle in [0,30]:jobs.append((f'partial_{angle}',dict(case='partial',angle=angle,nx=12,ny=12,dt=.001,end=.1,load=.7)))
for n,dt,label in [(8,.002,'coarse'),(24,.0005,'fine')]:jobs.append((f'anisotropic_30_{label}',dict(case='anisotropic',angle=30,nx=n,ny=max(2,n//4),dt=dt,end=.1,load=.7)))
for n,dt,label in [(8,.002,'coarse'),(16,.0005,'fine')]:jobs.append((f'partial_30_{label}',dict(case='partial',angle=30,nx=n,ny=n,dt=dt,end=.1,load=.7)))
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        for out in pool.map(lambda job:run(job[0],**job[1]),jobs):print(out,flush=True)
