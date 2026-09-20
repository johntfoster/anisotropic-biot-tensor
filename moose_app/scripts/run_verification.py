#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run independent spatial/time refinement and nonlinear load limits."""
from concurrent.futures import ThreadPoolExecutor
from run_case import run
from analyze_mandel import analyze
jobs=[]
for nx in [10,20,40]:jobs.append((f'linear_space_{nx}',dict(nx=nx,ny=2,dt=.0002,end=.1,linear=True)))
for dt in [.002,.001]:jobs.append((f'linear_time_{dt:g}',dict(nx=40,ny=2,dt=dt,end=.1,linear=True)))
jobs.append(('linear_load_reference',dict(nx=20,ny=2,dt=.001,end=.1,linear=True)))
for load in [.01,.001,.0001]:jobs.append((f'nonlinear_load_{load:g}',dict(nx=20,ny=2,dt=.001,end=.1,load=load)))
def one(job):
    name,kw=job;out=run(name,**kw);return analyze(out)
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(one,jobs):pass
