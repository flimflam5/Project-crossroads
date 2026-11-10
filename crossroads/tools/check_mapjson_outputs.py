#!/usr/bin/env python3
"""Verify generator timestamp stability without suppressing genuine output changes."""
import json,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as d:
    out=Path(d)/'ids.h';src=Path(d)/'map.json'
    data=json.loads((root/'data/maps/EcruteakCity_DanceTheater/map.json').read_text())
    src.write_text(json.dumps(data))
    cmd=[str(root/'tools/mapjson/mapjson'),'event_constants','emerald',str(src),str(out)]
    subprocess.run(cmd,check=True);first=out.read_bytes();stamp=out.stat().st_mtime_ns
    subprocess.run(cmd,check=True)
    assert out.read_bytes()==first and out.stat().st_mtime_ns==stamp
    data['object_events'][0]['local_id']='LOCALID_TIMESTAMP_REGRESSION'
    src.write_text(json.dumps(data));subprocess.run(cmd,check=True)
    assert out.read_bytes()!=first and b'LOCALID_TIMESTAMP_REGRESSION' in out.read_bytes()
print('Mapjson stable timestamps and genuine content updates: PASS')
