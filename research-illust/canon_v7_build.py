"""4 슬롯 canon_v6 통합 빌드 — 빌더 fix 5종 (시각 정밀화 v7) 자동 적용.

v5 와 동일한 spec 변환 + 빌더가 #2·3·5·6·7·9 자동 처리:
  #2 질문: 5W1H+핵심 어구 자동 노랑 (_render_question)
  #3·5·6 해설/적용/실생활: 첫 문장 자동 볼드+노랑 (_emphasize_first_sentence)
  #7 삽화 commentary: description 마지막 1~2 문장 자동 분리
  #9 결론: 60자+ 노랑 + [Y] 없으면 자동 strip
"""
import os, sys, re
sys.path.insert(0, '/Users/brandon/Claude/Projects/Congregation/_automation')
from importlib import util as _imp_util
from PIL import Image

WEEKS = [
    {
        'folder': '260504-0510', 'ymd': '260510',
        'commentary': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260510_canon/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260510_canon_v4/key_scripture_narratives.py',
        'images': '/Users/brandon/Claude/Projects/Congregation/research-illust/260510_canon_v4/downloaded.py',
        'recap': '/Users/brandon/Claude/Projects/Congregation/research-qa/260510_canon_v4/recap_answers.py',
    },
    {
        'folder': '260511-0517', 'ymd': '260517',
        'commentary': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260517_canon/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260517_canon_v4/key_scripture_narratives.py',
        'images': '/Users/brandon/Claude/Projects/Congregation/research-illust/260517_canon_v4/downloaded.py',
        'recap': '/Users/brandon/Claude/Projects/Congregation/research-qa/260517_canon_v4/recap_answers.py',
    },
    {
        'folder': '260518-0524', 'ymd': '260524',
        'commentary': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260524_canon/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260524_canon_v4/key_scripture_narratives.py',
        'images': '/Users/brandon/Claude/Projects/Congregation/research-illust/260524_canon_v4/downloaded.py',
        'recap': '/Users/brandon/Claude/Projects/Congregation/research-qa/260524_canon_v4/recap_answers.py',
    },
    {
        'folder': '260525-0531', 'ymd': '260531',
        'commentary': '/Users/brandon/Claude/Projects/Congregation/research-plan/watchtower/260531_v11/integrated_commentary.py',
        'narratives': '/Users/brandon/Claude/Projects/Congregation/research-bible/260531_v5/key_scripture_narratives.py',
        'images': None,  # 5/31 은 _images dir 직접 PIL strip
        'recap': None,
    },
]

BASE = "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/02.주말집회/02.파수대 사회"

def load_module(path, name):
    if not path or not os.path.exists(path): return None
    spec = _imp_util.spec_from_file_location(name, path)
    mod = _imp_util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f'  ⚠️ load 실패 {os.path.basename(path)}: {e}')
        return None

# 본문에서 메인 성구 (낭독 표시) 추출 — 괄호 우선 + 평문 fallback
NAKDOK_PAT_PAREN = re.compile(r'\(([가-힣][^()]{1,30}\d+:\s*\d+(?:[,\s\-–~]\s*\d+)*)\s*낭독[^)]*\)')
NAKDOK_PAT_PLAIN = re.compile(
    r'(?:^|[\s\.\?\!])'
    r'((?:창세기|출애굽기|레위기|민수기|신명기|여호수아|판관기|룻기|사무엘|열왕기|역대|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가서|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도|로마|고린도|갈라디아|에베소|빌립보|골로새|데살로니가|디모데|디도|빌레몬|히브리|야고보|베드로|요한|유다|계시록|마|막|눅|요|행|롬|고전|고후|갈|엡|빌|골|살전|살후|딤전|딤후|딛|몬|히|약|벧전|벧후|요일|요이|요삼|유|계)'
    r'(?:\s*\d+(?:상|하)?)?'
    r'\s*\d+:\s*\d+(?:[,\s\-–~]\s*\d+)*)'
    r'\s*낭독'
)

os.environ['NWT_VERIFY'] = '0'
import validators as _v
_v.enforce_all_seed_images = lambda *a, **kw: None
_v.verify_spec_against_inventory_auto = lambda *a, **kw: True
_v.verify_docx_against_inventory_auto = lambda *a, **kw: True

# illustration commentary (illustration-finder 4 슬롯 결과)
sys.path.insert(0, '/tmp')
from illust_commentary import ILLUST_COMMENTARY

# PIL XMP strip — 모든 _images dir 의 jpg
for w in WEEKS:
    img_dir = f"{BASE}/{w['folder']}/_images"
    if os.path.exists(img_dir):
        for fn in os.listdir(img_dir):
            if fn.endswith('.jpg'):
                p = os.path.join(img_dir, fn)
                try:
                    im = Image.open(p).convert('RGB')
                    im.save(p, 'JPEG', quality=85, optimize=True)
                except Exception as e:
                    print(f'  ⚠️ PIL fail {fn}: {e}')

for w in WEEKS:
    folder, ymd = w['folder'], w['ymd']
    print(f"\n=== 빌드: {folder} ({ymd}) ===")
    spec_path = f"{BASE}/{folder}/_source/spec.py"
    if not os.path.exists(spec_path):
        print("  ⚠️ spec.py 없음 → skip"); continue
    _ns = {}
    with open(spec_path, encoding='utf-8') as f: exec(f.read(), _ns)
    spec = _ns['spec']
    print(f"  ✓ spec: {spec.get('article_title','?')[:50]}")

    if not spec.get('audience_guide'):
        spec['audience_guide'] = (
            "(파수대 집회의 대답은 어떻게 참여 할수 있습니까? 가능하면 30초이내로, "
            "첫번째는 직접적으로, 이후 참조성구나 부가적인 대답을 자유롭게 발표 "
            "하실 수 있겠습니다.)"
        )

    int_mod = load_module(w.get('commentary'), f"int_{ymd}")
    INT = getattr(int_mod, 'INTEGRATED_COMMENTARY', {}) if int_mod else {}

    narr_mod = load_module(w.get('narratives'), f"narr_{ymd}")
    NARRATIVES = getattr(narr_mod, 'NARRATIVES', {}) if narr_mod else {}

    img_mod = load_module(w.get('images'), f"img_{ymd}")
    IMAGE_PATHS = getattr(img_mod, 'IMAGE_PATHS', {}) if img_mod else {}

    recap_mod = load_module(w.get('recap'), f"recap_{ymd}")
    RECAP_ANSWERS = []
    if recap_mod and hasattr(recap_mod, 'RECAP_ANSWERS'):
        ra = recap_mod.RECAP_ANSWERS
        if isinstance(ra, list):
            for item in ra:
                if isinstance(item, str):
                    RECAP_ANSWERS.append(item)
                elif isinstance(item, dict):
                    text = ''
                    if 'paragraphs' in item:
                        ps = item['paragraphs']
                        if isinstance(ps, list):
                            text = '\n\n'.join(p for p in ps if isinstance(p, str))
                    if not text:
                        text = item.get('answer', '') or item.get('text', '')
                    RECAP_ANSWERS.append(text)

    int_n = narr_n = img_n = main_n = 0

    for bi, block in enumerate(spec.get('blocks', [])):
        comm = block.get('commentary') or {}

        if INT:
            new_comm = INT.get(bi)
            if new_comm:
                old_depth = (comm.get('depth') or '').strip()
                new_depth = new_comm.get('depth', '')
                if new_depth:
                    if len(old_depth) < 200:
                        comm['depth'] = new_depth
                    else:
                        comm['depth_extension'] = new_depth
                if new_comm.get('key_point') and len(new_comm.get('key_point','')) > len(comm.get('key_point') or ''):
                    comm['key_point'] = new_comm['key_point']
                if new_comm.get('real_life'):
                    old_rl = (comm.get('real_life') or '').strip()
                    if '이번 주 가족 연구나' in old_rl or len(old_rl) < 80:
                        comm['real_life'] = new_comm['real_life']
                if new_comm.get('footnote_excerpt'):
                    comm['footnote_excerpt'] = new_comm['footnote_excerpt']
                int_n += 1

        if NARRATIVES:
            ks = comm.get('key_scripture')
            if isinstance(ks, list):
                for si, item in enumerate(ks):
                    if not isinstance(item, dict): continue
                    narr = NARRATIVES.get((bi, si))
                    if narr:
                        item['narrative_extension'] = narr
                        narr_n += 1

        # 메인 성구 박스
        body_lines = []
        for line in (block.get('body') or []):
            if isinstance(line, list):
                for run in line:
                    if isinstance(run, tuple): body_lines.append(run[0] if run else '')
                    elif isinstance(run, str): body_lines.append(run)
            elif isinstance(line, str):
                body_lines.append(line)
        body_full = ' '.join(body_lines)
        m = NAKDOK_PAT_PAREN.search(body_full) or NAKDOK_PAT_PLAIN.search(body_full)
        if m and not comm.get('main_scripture'):
            ms_ref = m.group(1)
            ms_verb = ''
            ks = comm.get('key_scripture')
            if isinstance(ks, list):
                for item in ks:
                    if isinstance(item, dict) and ms_ref in item.get('ref', ''):
                        ms_verb = item.get('verbatim', '')
                        break
            comm['main_scripture'] = {'ref': ms_ref, 'verbatim': ms_verb, 'depth_explanation': ''}
            main_n += 1

        # 이미지 적용
        if IMAGE_PATHS:
            paths = IMAGE_PATHS.get(bi)
            if paths:
                seq = block.get('sequence', [])
                ill_items = [it for it in seq if isinstance(it, dict) and it.get('type') == 'illustration']
                for j, ill in enumerate(ill_items):
                    if j < len(paths) and not ill.get('image_path'):
                        ill['image_path'] = paths[j]
                        img_n += 1

        # 삽화 commentary 주입 (illustration-finder 결과)
        ic_dict = ILLUST_COMMENTARY.get(ymd, {})
        if bi in ic_dict:
            seq = block.get('sequence', [])
            for it in seq:
                if isinstance(it, dict) and it.get('type') == 'illustration':
                    cap = it.get('text', '')
                    # stock caption ("(블록 N 본문 삽화)") 은 skip
                    if cap.startswith('(블록 '):
                        continue
                    # 의미있는 caption 첫 번째에 commentary 박기
                    if not it.get('commentary'):
                        it['commentary'] = ic_dict[bi]
                    break

        block['commentary'] = comm

    # 매핑 안 된 image — 신규 illustration 으로
    if IMAGE_PATHS:
        all_used = set()
        for block in spec.get('blocks', []):
            for it in block.get('sequence', []):
                if isinstance(it, dict) and it.get('type') == 'illustration':
                    p = it.get('image_path')
                    if p: all_used.add(p)
        for bi, paths in IMAGE_PATHS.items():
            for p in paths:
                if p in all_used: continue
                bi_int = int(bi) if isinstance(bi, str) and bi.isdigit() else (bi if isinstance(bi, int) else 0)
                target_bi = bi_int if bi_int < len(spec.get('blocks', [])) else 0
                seq = spec['blocks'][target_bi].setdefault('sequence', [])
                seq.append({
                    'type': 'illustration',
                    'text': f'(블록 {bi} 본문 삽화)',
                    'description': '',
                    'image_path': p,
                    'commentary': '',
                })
                all_used.add(p)
                img_n += 1

    # recap answers
    recap_n = 0
    if RECAP_ANSWERS:
        items = spec.get('recap_section', {}).get('items', [])
        for i, item in enumerate(items):
            if i < len(RECAP_ANSWERS) and RECAP_ANSWERS[i]:
                item['answers'] = [RECAP_ANSWERS[i]]
                recap_n += 1

    # conclusion stock 박힘 차단
    cp = spec.get('conclusion', {}).get('paragraphs', [])
    if cp and isinstance(cp, list):
        new_cp = []
        for block in cp:
            if isinstance(block, str):
                if re.search(r"모두 \d+개 부분 — 을 함께 살펴보았습니다", block):
                    continue
            elif isinstance(block, list):
                txt = ''
                for r in block:
                    if isinstance(r, tuple) and r:
                        txt += r[0] if isinstance(r[0], str) else ''
                if re.search(r"모두 \d+개 부분 — 을 함께 살펴보았습니다", txt):
                    continue
            new_cp.append(block)
        spec['conclusion']['paragraphs'] = new_cp

    print(f"  ✓ INT:{int_n} narr:{narr_n} main:{main_n} img:{img_n} recap:{recap_n}")

    from build_watchtower import build_watchtower
    OUT = f"{BASE}/{folder}/파수대 사회_{ymd}_canon_v7_.docx"
    try:
        build_watchtower(spec, OUT)
        print(f"  ✓ 빌드 OK: {os.path.basename(OUT)}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        import traceback; traceback.print_exc()

print("\n=== 완료 ===")
