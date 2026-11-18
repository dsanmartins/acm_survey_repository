#!/usr/bin/env python3
"""Run unchanged approved standalone generators in a temporary local copy."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--conceptual-only',action='store_true');a=p.parse_args()
    cache=ROOT/'.cache';cache.mkdir(exist_ok=True)
    dest=ROOT/'results/generated_figures';dest.mkdir(parents=True,exist_ok=True)
    sources=['current_conceptual_maps.py']+([] if a.conceptual_only else ['assurance_reporting_schema.py'])
    records=[]
    with tempfile.TemporaryDirectory(dir=cache) as tmp:
        work=Path(tmp);(work/'figure_sources').mkdir();(work/'figures').mkdir()
        for source in sources:
            src=ROOT/'figure_sources'/source;target=work/'figure_sources'/source;shutil.copy2(src,target)
            subprocess.run([sys.executable,'-B',str(target)],check=True,cwd=work,env=dict(os.environ,MPLCONFIGDIR=str(work/'mpl'),PYTHONDONTWRITEBYTECODE='1'))
            records.append(dict(generator='figure_sources/'+source,sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
        files={}
        for f in sorted((work/'figures').iterdir()):
            shutil.copy2(f,dest/f.name);files[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
        (dest/'generation_provenance.json').write_text(json.dumps(dict(generators=records,outputs=files,scientific_data_changed=False,scope='Figures 3 and 6 are conceptual syntheses; Figure 5 describes a source-reported procedure, not a new experimental outcome.'),indent=2)+'\n')
    print('PASS: approved standalone sources regenerated in results/generated_figures; packaged reference figures were not overwritten.')
if __name__=='__main__':main()
