from pathlib import Path
import runpy,time
p=Path('/tmp/qa10-ecruteak-court-impl.py')
while not p.exists():time.sleep(0.2)
runpy.run_path(str(p),run_name='__main__')
