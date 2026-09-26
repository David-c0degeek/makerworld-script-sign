"""Add short, measured low-profile bridges between nearby mesh components.

This never connects components more than max_gap apart: long connectors are
an artistic decision and should be edited in MakerWorld, not guessed.
"""
import argparse
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import cKDTree


def closest_xy(a, b):
    aa = a.vertices[:, :2]
    bb = b.vertices[:, :2]
    distances, indexes = cKDTree(aa).query(bb, workers=-1)
    idx = int(np.argmin(distances))
    return float(distances[idx]), aa[int(indexes[idx])].tolist(), bb[idx].tolist()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_stl', type=Path)
    p.add_argument('output_scad', type=Path)
    p.add_argument('--max-gap', type=float, default=1.5)
    p.add_argument('--bridge-diameter', type=float, default=2.2)
    p.add_argument('--bridge-height', type=float, default=3.0)
    args = p.parse_args()

    mesh = trimesh.load_mesh(args.input_stl, process=True)
    if not isinstance(mesh, trimesh.Trimesh) or not mesh.is_watertight:
        raise SystemExit('Input is not a watertight mesh.')
    parts = sorted(mesh.split(only_watertight=False), key=lambda m: m.volume, reverse=True)
    print('Unrepaired mesh components:', len(parts), flush=True)
    linked = {0}
    bridges = []
    while len(linked) < len(parts):
        choices = [(*closest_xy(parts[i],parts[j]),i,j) for i in linked
                   for j in range(len(parts)) if j not in linked]
        dist, a, b, i, j = min(choices, key=lambda x: x[0])
        if dist > args.max_gap:
            raise SystemExit(f'Refusing visible {dist:.2f}mm connector; manual adjustment needed.')
        print(f'Bridge component {i} to {j}: gap {dist:.3f} mm, {a} -> {b}',flush=True)
        bridges.append((a,b))
        linked.add(j)

    source = args.input_stl.resolve().as_posix()
    lines = ['$fn = 36;', 'union() {', f'  import("{source}", convexity=5);']
    if bridges:
        lines.append(f'  linear_extrude(height={args.bridge_height}) union() {{')
        for a,b in bridges:
            lines += ['    hull() {',
                f'      translate([{a[0]:.6f},{a[1]:.6f}]) circle(d={args.bridge_diameter});',
                f'      translate([{b[0]:.6f},{b[1]:.6f}]) circle(d={args.bridge_diameter});',
                '    }']
        lines += ['  }']
    lines += ['}', '']
    args.output_scad.write_text('\n'.join(lines), encoding='utf-8')


if __name__=='__main__':
    main()
