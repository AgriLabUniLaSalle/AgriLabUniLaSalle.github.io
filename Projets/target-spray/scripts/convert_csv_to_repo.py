import csv,re,os,shutil,zipfile,unicodedata,html
from pathlib import Path
src=Path('/mnt/data/p(2).csv')
out=Path('/mnt/data/target-spray')
if out.exists(): shutil.rmtree(out)
for d in ['docs','assets/images','assets/models','notebooks','scripts','data']:(out/d).mkdir(parents=True,exist_ok=True)

def slug(s):
 s=s.replace('_','-').replace('/','-')
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
 return re.sub(r'-+','-',re.sub(r'[^a-z0-9-]+','-',s)).strip('-')

def title_from_name(s): return s.replace('_',' ').strip()
with src.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
# map aliases for links
page_map={}
for r in rows:
 n=r['page_wiki']; page_map[n.lower().replace('_',' ')]=slug(n)+'.md'
 page_map[title_from_name(n).lower()]=slug(n)+'.md'
# Prefer plural canonical page
page_map['solutions techniques']='solutions-techniques.md'
page_map['modification pour salon/expo']='modification-pour-salonexpo.md'
page_map['modification pour salon expo']='modification-pour-salonexpo.md'
images=set(); pyblocks=[]; shellblocks=[]

def img_repl(m):
 fn=m.group(1).strip().replace('\\_','_'); images.add(fn)
 return f'![{Path(fn).stem}](../assets/images/{fn})'
def thumb_repl(m):
 fn=m.group(1).strip(); images.add(fn)
 return f'![{Path(fn).stem}](../assets/images/{fn})'
def wikilink(m):
 label=m.group(1).strip().replace('\\','')
 key=label.lower().replace('_',' ')
 target=page_map.get(key,slug(label)+'.md')
 return f'[{label}]({target})'
def convert(text):
 text=text.replace('\r\n','\n').replace('\r','\n')
 # HTML code blocks first
 def code(m):
  lang=(m.group(1) or '').replace('"','').strip() or 'text'
  body=html.unescape(m.group(2)).strip('\n')
  if lang=='python': pyblocks.append(body)
  elif lang in ('bash','shell','sh','text') and ('sudo ' in body or 'systemctl' in body): shellblocks.append(body)
  return f'```{lang}\n{body}\n```'
 text=re.sub(r'<pre>\s*<code[^>]*class=(?:""|\")?([^"> ]*)[^>]*>(.*?)</code>\s*</pre>',code,text,flags=re.S|re.I)
 text=re.sub(r'<pre>(.*?)</pre>',lambda m:'```text\n'+html.unescape(m.group(1)).strip()+'\n```',text,flags=re.S|re.I)
 # Redmine headings
 text=re.sub(r'(?m)^h([1-6])\.\s*',lambda m:'#'*int(m.group(1))+' ',text)
 # thumbnails and images (allow escaped !)
 text=re.sub(r'\{\{thumbnail\(([^,\)]+).*?\)\}\}',thumb_repl,text)
 text=re.sub(r'!\{[^}]*\}([^!\n]+)\\?!',img_repl,text)
 text=re.sub(r'(?<!\w)!([^!\n]+?\.(?:png|jpe?g|gif|webp))\\?!',img_repl,text,flags=re.I)
 # wiki links and remaining HTML anchors
 text=re.sub(r'\\?\[\\?\[([^\]]+?)\\?\]\\?\]',wikilink,text)
 text=re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>',lambda m:f'[{re.sub("<.*?>","",m.group(2)).strip() or m.group(1)}]({m.group(1)})',text,flags=re.S|re.I)
 text=html.unescape(text)
 # Textile bold/italics basic
 text=re.sub(r'(?m)^\+(.+?)\+$',r'**\1**',text)
 # normalize escaped chars from CSV exports
 text=text.replace('\\!','!').replace('\\_','_').replace('\\>','>').replace('\\[','[').replace('\\]',']')
 text=re.sub(r'[ \t]+\n','\n',text)
 text=re.sub(r'\n{3,}','\n\n',text).strip()+'\n'
 return text

pages=[]
for r in rows:
 name=r['page_wiki']; fn=slug(name)+'.md'; body=convert(r['contenu'])
 # avoid duplicate top title if missing title only
 if not body.startswith('# '): body='# '+title_from_name(name)+'\n\n'+body
 # add navigation
 body += '\n---\n\n[← Retour au sommaire](../README.md)\n'
 (out/'docs'/fn).write_text(body,encoding='utf-8')
 pages.append((title_from_name(name),fn))
# README derived from Wiki plus index
wiki=next((r for r in rows if r['page_wiki']=='Wiki'),None)
intro=convert(wiki['contenu']) if wiki else '# Target Spray\n'
intro=re.sub(r'\]\(([^)]+\.md)\)',r'](docs/\1)',intro)
index='\n## Documentation complète\n\n'+''.join(f'- [{t}](docs/{f})\n' for t,f in pages if f!='wiki.md')
readme=intro+index+'''\n## Structure du dépôt\n\n```text\ntarget-spray/\n├── README.md\n├── docs/\n├── assets/\n│   ├── images/\n│   └── models/\n├── notebooks/\n├── scripts/\n└── data/\n```\n\n## Ressources non incluses\n\nLes images, le modèle `.pt` et le notebook référencés par le wiki ne se trouvaient pas dans le CSV. Les dossiers prévus sont présents et la liste des fichiers attendus se trouve dans `assets/images/README.md`.\n\n## Licence\n\nAucune licence de réutilisation n'était indiquée dans les données sources. Voir `LICENSE`.\n'''
(out/'README.md').write_text(readme,encoding='utf-8')
# extracted python blocks
for i,b in enumerate(pyblocks,1): (out/'scripts'/f'yolov8_laser_{i}.py').write_text(b+'\n',encoding='utf-8')
(out/'scripts'/'README.md').write_text('# Scripts\n\nScripts Python extraits de la page « Code python et logiciel ». Vérifiez les chemins, broches GPIO et dépendances avant exécution sur le Raspberry Pi.\n',encoding='utf-8')
(out/'assets/images'/'README.md').write_text('# Images attendues\n\nExportez les pièces jointes Redmine dans ce dossier en conservant leurs noms :\n\n'+''.join(f'- `{x}`\n' for x in sorted(images,key=str.lower)),encoding='utf-8')
(out/'assets/models'/'README.md').write_text('# Modèles IA\n\nPlacez ici les modèles YOLO (`.pt`, `.hef`). Ces fichiers binaires ne sont pas présents dans le CSV.\n',encoding='utf-8')
(out/'notebooks'/'README.md').write_text('# Notebooks\n\nPlacez ici le notebook Google Colab d’entraînement YOLO référencé dans la documentation.\n',encoding='utf-8')
shutil.copy2(src,out/'data'/'wiki-export.csv')
(out/'.gitignore').write_text('''__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n.DS_Store\nThumbs.db\nruns/\n*.hef\n*.pt\n!assets/models/README.md\n''',encoding='utf-8')
(out/'requirements.txt').write_text('ultralytics\nopencv-python\nnumpy\ngpiozero\nmatplotlib\npicamera2; platform_machine == "aarch64"\n',encoding='utf-8')
(out/'CONTRIBUTING.md').write_text('# Contribution\n\n1. Créez une branche dédiée.\n2. Modifiez la documentation ou les scripts.\n3. Vérifiez les liens et les chemins d’images.\n4. Ouvrez une pull request avec une description claire.\n',encoding='utf-8')
(out/'LICENSE').write_text('''Copyright (c) 2026 AgriLab / contributeurs du projet Target Spray\n\nAucune licence de réutilisation n’a été fournie dans l’export source.\nTous droits réservés jusqu’à ce que les titulaires des droits choisissent une licence explicite.\nCe fichier doit être remplacé par la licence validée par les responsables du projet avant publication publique.\n''',encoding='utf-8')
# conversion utility
shutil.copy2('/tmp/build_repo.py',out/'scripts'/'convert_csv_to_repo.py')
# manifest check
missing=[]
for p in out.rglob('*.md'):
 txt=p.read_text(encoding='utf-8')
 for target in re.findall(r'\]\(([^)#]+)',txt):
  if target.startswith(('http:','https:','mailto:')): continue
  q=(p.parent/target).resolve()
  if not q.exists() and 'assets/images/' not in target: missing.append((str(p.relative_to(out)),target))
manifest=f'pages={len(rows)}\nmarkdown_files={len(list(out.rglob("*.md")))}\npython_blocks={len(pyblocks)}\nreferenced_images={len(images)}\nmissing_internal_links={len(missing)}\n'
(out/'MANIFEST.txt').write_text(manifest,encoding='utf-8')
zip_path=Path('/mnt/data/target-spray-github.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in out.rglob('*'):
  if p.is_file(): z.write(p,Path(out.name)/p.relative_to(out))
print(manifest)
print('zip',zip_path,zip_path.stat().st_size)
print('images',len(images))
print('missing',missing[:10])
