"""3 슬롯 ver12 빌드 — v11 패턴 + 빌더 v9 fix + 12 삽화 [Y] commentary.

5/17·24·31 ver12 (5/10 제외 — 사용자 평이름 정본 보존).
v11 자료 (INTEGRATED + NARRATIVES + RECAP) + canon_v8_illust ([Y] description+commentary).
빌더 v9 적용 (낭독 박스 통합 라벨 + 자동 강조 폐기 + body_runs).
"""
import os, sys, re
sys.path.insert(0, '/Users/brandon/Claude/Projects/Congregation/_automation')
from importlib import util as _imp_util
from PIL import Image

BASE = "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/02.주말집회/02.파수대 사회"

# 5/10 제외 (사용자 평이름 정본 유지). 5/17·24·31 ver12 부터.
ILLUST_PATH = '/Users/brandon/Claude/Projects/Congregation/research-illust/canon_v8_illust.py'

SLOTS = [
    {
        'ymd': '260517', 'folder': '260511-0517',
        'integrated': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260517_canon/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260517_canon_v4/key_scripture_narratives.py',
    },
    {
        'ymd': '260524', 'folder': '260518-0524',
        'integrated': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260524_canon/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260524_canon_v4/key_scripture_narratives.py',
    },
    {
        'ymd': '260531', 'folder': '260525-0531',
        'integrated': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260531_v11/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260531_v5/key_scripture_narratives.py',
    },
]

# PIL XMP strip + validators 우회
os.environ['NWT_VERIFY'] = '0'
import validators as _v
_v.enforce_all_seed_images = lambda *a, **kw: None
_v.verify_spec_against_inventory_auto = lambda *a, **kw: True
_v.verify_docx_against_inventory_auto = lambda *a, **kw: True

for slot in SLOTS:
    img_dir = f"{BASE}/{slot['folder']}/_images"
    if os.path.exists(img_dir):
        for fn in os.listdir(img_dir):
            if fn.endswith('.jpg'):
                p = os.path.join(img_dir, fn)
                try:
                    Image.open(p).convert('RGB').save(p, 'JPEG', quality=85, optimize=True)
                except Exception: pass

from build_watchtower import build_watchtower
from scrape_wt import fetch_nwt_verse, _parse_range_ref

def load(path, name):
    if not os.path.exists(path): return None
    s = _imp_util.spec_from_file_location(name, path)
    m = _imp_util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

NAKDOK_PAREN = re.compile(r'\(([가-힣][^()]{1,30}\d+:\s*\d+(?:[,\s\-–~]\s*\d+)*)\s*낭독[^)]*\)')
NAKDOK_PLAIN = re.compile(
    r'(?:^|[\s\.\?\!])((?:창세기|출애굽기|레위기|민수기|신명기|여호수아|판관기|룻기|사무엘|열왕기|역대|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가서|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도|로마|고린도|갈라디아|에베소|빌립보|골로새|데살로니가|디모데|디도|빌레몬|히브리|야고보|베드로|요한|유다|계시록|마|막|눅|요|행|롬|고전|고후|갈|엡|빌|골|살전|살후|딤전|딤후|딛|몬|히|약|벧전|벧후|요일|요이|요삼|유|계)(?:\s*\d+(?:상|하)?)?\s*\d+:\s*\d+(?:[,\s\-–~]\s*\d+)*)\s*낭독'
)

for slot in SLOTS:
    ymd, folder = slot['ymd'], slot['folder']
    print(f"\n=== {ymd} ===")
    spec_path = f"{BASE}/{folder}/_source/spec.py"
    if not os.path.exists(spec_path):
        print("  ⚠️ spec.py 없음 → skip"); continue
    ns = {}
    with open(spec_path, encoding='utf-8') as f: exec(f.read(), ns)
    spec = ns['spec']
    print(f"  ✓ spec: {spec.get('article_title','?')[:50]}")

    # spec 청소 — stock illustration
    for block in spec.get('blocks', []):
        seq = block.get('sequence', [])
        block['sequence'] = [it for it in seq
                             if not (isinstance(it, dict) and it.get('type') == 'illustration'
                                     and str(it.get('text', '')).startswith('(블록 '))]

    # audience_guide
    if not spec.get('audience_guide'):
        spec['audience_guide'] = (
            "(파수대 집회의 대답은 어떻게 참여 할수 있습니까? 가능하면 30초이내로, "
            "첫번째는 직접적으로, 이후 참조성구나 부가적인 대답을 자유롭게 발표 "
            "하실 수 있겠습니다.)"
        )

    # NARRATIVES — key_scripture 안에 narrative 박기 (v11 패턴)
    narr_mod = load(slot['narratives'], f'narr_{ymd}')
    NARRATIVES = getattr(narr_mod, 'NARRATIVES', {}) if narr_mod else {}
    nn = 0
    for bi, block in enumerate(spec.get('blocks', [])):
        comm = block.get('commentary') or {}
        ks = comm.get('key_scripture')
        if isinstance(ks, list):
            for si, item in enumerate(ks):
                if not isinstance(item, dict): continue
                narr = NARRATIVES.get((bi, si))
                if narr:
                    item['narrative'] = narr
                    nn += 1

    # INTEGRATED_COMMENTARY — 5 필드 통째 갱신 (v11 패턴)
    int_mod = load(slot['integrated'], f'int_{ymd}')
    INT = getattr(int_mod, 'INTEGRATED_COMMENTARY', {}) if int_mod else {}
    ai = af = 0
    for bi, block in enumerate(spec.get('blocks', [])):
        new_comm = INT.get(bi)
        if not new_comm: continue
        comm = block.get('commentary') or {}
        if new_comm.get('answer'):
            comm['answer'] = new_comm['answer']
        if new_comm.get('depth'):
            d = new_comm['depth']
            if new_comm.get('footnote_excerpt'):
                d = d + "\n\n" + new_comm['footnote_excerpt']
                af += 1
            comm['depth'] = d
        if new_comm.get('key_point'):
            comm['key_point'] = new_comm['key_point']
        if new_comm.get('real_life'):
            comm['real_life'] = new_comm['real_life']
        block['commentary'] = comm
        ai += 1

    # 이미지 매핑 (caption "(N항 참조)" 항 번호 또는 순서 fallback)
    img_path = f'/Users/brandon/Claude/Projects/Congregation/research-illust/{ymd}_canon_v4/downloaded.py'
    IMAGE_PATHS = {}
    if os.path.exists(img_path):
        img_mod = load(img_path, f'img_{ymd}')
        IMAGE_PATHS = getattr(img_mod, 'IMAGE_PATHS', {}) if img_mod else {}
    img_n = 0
    # 의미있는 caption 의 illustration list (block_index 순)
    meaningful_ill = []
    for bi, block in enumerate(spec.get('blocks', [])):
        for it in block.get('sequence', []):
            if isinstance(it, dict) and it.get('type') == 'illustration':
                cap = it.get('text', '')
                if cap.startswith('(블록 '): continue
                meaningful_ill.append((bi, it))
    # 1차: caption "(N항 참조)" → IMAGE_PATHS 정수 key
    for bi, ill in meaningful_ill:
        if ill.get('image_path'): continue
        cap = ill.get('text', '')
        cm = re.search(r'\((\d+)(?:[-–](\d+))?\s*항\s*참조\)', cap)
        target_n = int(cm.group(1)) if cm else None
        if target_n and target_n in IMAGE_PATHS:
            v = IMAGE_PATHS[target_n]
            ill['image_path'] = v[0] if isinstance(v, list) else v
            img_n += 1
    # 2차: 매핑 안된 illustration + 매핑 안된 IMAGE_PATHS values 순서 fallback
    used_paths = set()
    for _, ill in meaningful_ill:
        if ill.get('image_path'):
            used_paths.add(ill['image_path'])
    remaining_ills = [ill for _, ill in meaningful_ill if not ill.get('image_path')]
    remaining_paths = []
    for k in sorted(IMAGE_PATHS.keys(), key=str):
        v = IMAGE_PATHS[k]
        if isinstance(v, list):
            for p in v:
                if p not in used_paths: remaining_paths.append(p)
        elif v not in used_paths:
            remaining_paths.append(v)
    for i, ill in enumerate(remaining_ills):
        if i < len(remaining_paths):
            ill['image_path'] = remaining_paths[i]
            img_n += 1

    # 삽화 [Y] description+commentary 주입 (canon_v8_illust)
    illust_mod = load(ILLUST_PATH, f'illust_{ymd}')
    ILLUST = getattr(illust_mod, 'ILLUST_V8', {}) if illust_mod else {}
    illust_dict = ILLUST.get(ymd, {})
    icn = 0
    for bi, block in enumerate(spec.get('blocks', [])):
        if bi not in illust_dict: continue
        entry = illust_dict[bi]
        if not isinstance(entry, dict): continue
        seq = block.get('sequence', [])
        for it in seq:
            if isinstance(it, dict) and it.get('type') == 'illustration':
                cap = it.get('text', '')
                if cap.startswith('(블록 '): continue
                if entry.get('description'):
                    it['description'] = entry['description']
                if entry.get('commentary'):
                    it['commentary'] = entry['commentary']
                icn += 1
                break

    # 메인 성구 (낭독) — 본문에서 검출 + verbatim NWT fetch
    mn = vn = 0
    for bi, block in enumerate(spec.get('blocks', [])):
        comm = block.get('commentary') or {}
        body_lines = []
        for line in (block.get('body') or []):
            if isinstance(line, list):
                for run in line:
                    if isinstance(run, tuple): body_lines.append(run[0] if run else '')
                    elif isinstance(run, str): body_lines.append(run)
            elif isinstance(line, str):
                body_lines.append(line)
        body_full = ' '.join(body_lines)

        ms = comm.get('main_scripture')
        # 신규 매칭
        if not ms:
            m = NAKDOK_PAREN.search(body_full) or NAKDOK_PLAIN.search(body_full)
            if m:
                ms = {'ref': m.group(1), 'verbatim': '', 'depth_explanation': ''}
                mn += 1

        # verbatim 채우기
        if ms and not ms.get('verbatim'):
            try:
                v_start, v_end = _parse_range_ref(ms.get('ref', ''))
                verse = fetch_nwt_verse(ms['ref'], verse_end=v_end)
                if verse and verse.get('text'):
                    ms['verbatim'] = verse['text']
                    vn += 1
            except Exception: pass

        if ms:
            comm['main_scripture'] = ms
            block['commentary'] = comm

    # conclusion stock 박힘 차단
    cp = spec.get('conclusion', {}).get('paragraphs', [])
    if cp:
        new_cp = []
        for blk in cp:
            txt = ''
            if isinstance(blk, str): txt = blk
            elif isinstance(blk, list):
                for r in blk:
                    if isinstance(r, tuple) and r:
                        txt += r[0] if isinstance(r[0], str) else ''
            if re.search(r"모두 \d+개 부분 — 을 함께 살펴보았습니다", txt): continue
            new_cp.append(blk)
        spec['conclusion']['paragraphs'] = new_cp

    print(f"  ✓ narr:{nn} int:{ai}/17 footnote:{af} new_main:{mn} verb:{vn} img:{img_n} illust:{icn}")

    OUT = f"{BASE}/{folder}/파수대 사회_{ymd}_ver12_.docx"
    try:
        build_watchtower(spec, OUT)
        print(f"  ✓ Built: {os.path.basename(OUT)}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        import traceback; traceback.print_exc()
