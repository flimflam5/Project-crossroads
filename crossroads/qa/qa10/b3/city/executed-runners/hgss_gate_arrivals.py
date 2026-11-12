"""Explicit return-only warp anchors; never treat these public floor tiles as doors."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def arrivals():
 result={}
 for r in json.loads((R/'crossroads/hgss/gate-review.json').read_text()):
  for key,n in [('city','EcruteakCity'),('route',r['route'])]:
   for anchor,entry in zip(r.get(key+'_arrival_indices',[]),r[key+'_alias_indices']):result[(n,anchor)]=entry
 return result
def gate_connections():
 return {(a,b) for r in json.loads((R/'crossroads/hgss/gate-review.json').read_text()) for a,b in [('EcruteakCity',r['route']),(r['route'],'EcruteakCity')]}
