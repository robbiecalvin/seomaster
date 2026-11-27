import argparse,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def install(destination):
    source=ROOT/'skills'; target=Path(destination).expanduser(); dirs=sorted(p for p in source.iterdir() if (p/'SKILL.md').is_file())
    conflicts=[p.name for p in dirs if (target/p.name).exists()]
    if conflicts:raise FileExistsError('Existing skills; no overwrite: '+', '.join(conflicts))
    target.mkdir(parents=True,exist_ok=True)
    for p in dirs:shutil.copytree(p,target/p.name)
    return len(dirs)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('destination',help='Explicit Codex skills directory');a=p.parse_args();print('Installed',install(a.destination),'skill folders. Retain the source repository for scripts and registry.')
