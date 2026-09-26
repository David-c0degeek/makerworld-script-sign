"""Verify a script sign STL and convert it to a basic, portable 3MF.

The generated 3MF contains geometry only; choose your printer and slicing
settings when opening it in Bambu Studio.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import trimesh


def export_3mf(mesh, destination):
    vertex_xml = '\n'.join('<vertex x="{:.6f}" y="{:.6f}" z="{:.6f}"/>'.format(*p) for p in mesh.vertices)
    triangle_xml = '\n'.join('<triangle v1="{}" v2="{}" v3="{}"/>'.format(*t) for t in mesh.faces)
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<resources><object id="1" type="model"><mesh><vertices>'
        + vertex_xml + '</vertices><triangles>' + triangle_xml +
        '</triangles></mesh></object></resources>'
        '<build><item objectid="1"/></build></model>'
    )
    content_types = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="r0" Target="/3D/3dmodel.model" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        '</Relationships>')
    with ZipFile(destination, 'w', ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', model)
    with ZipFile(destination) as z:
        assert z.testzip() is None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stl', type=Path)
    parser.add_argument('output_3mf', type=Path)
    args = parser.parse_args()
    mesh = trimesh.load_mesh(args.stl, process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError('STL must contain one mesh')
    parts = mesh.split(only_watertight=False)
    size = mesh.extents
    print('Components:', len(parts))
    print('Watertight:', mesh.is_watertight)
    print('Extents (mm):', [round(float(x),2) for x in size])
    if len(parts) != 1 or not mesh.is_watertight:
        raise SystemExit('Model is not one watertight printable piece; do not publish.')
    if max(size[:2]) > 180:
        raise SystemExit('Model exceeds the Bambu Lab A1 Mini bed.')
    export_3mf(mesh, args.output_3mf)
    loaded = trimesh.load(args.output_3mf, force='mesh')
    print('3MF round-trip:', len(loaded.faces), 'faces; watertight:', loaded.is_watertight)
    if len(loaded.split()) != 1 or not loaded.is_watertight:
        raise SystemExit('Generated 3MF failed validation.')


if __name__ == '__main__':
    main()
