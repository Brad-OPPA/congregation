import fitz
import os
import re
import json

SRC = r"C:\Users\yoone\Dropbox\congregation\research-public-talk\S-34_KO_공개강연_골자_1-194.pdf"
OUT_DIR = r"C:\Users\yoone\Dropbox\congregation\research-public-talk\S-34_split"
OCR_DIR = r"C:\Users\yoone\tmp_ocr_text"

os.makedirs(OUT_DIR, exist_ok=True)

src = fitz.open(SRC)
N = len(src)

def get_text_or_ocr(page_num):
    """Return text for page_num (1-indexed). Use OCR if text layer is garbled."""
    t = src[page_num - 1].get_text()
    kor = sum(1 for c in t if 0xAC00 <= ord(c) <= 0xD7A3)
    if len(t) > 300 and kor < 50:
        ocr_path = os.path.join(OCR_DIR, f"page_{page_num:03d}.txt")
        if os.path.exists(ocr_path):
            with open(ocr_path, "r", encoding="utf-8") as f:
                return f.read()
    return t

def clean_title(s):
    """Clean title for filename use."""
    if not s:
        return ""
    # Remove invalid filename chars
    s = re.sub(r'[<>:"/\\|?*\n\r\t]', "", s).strip()
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s)
    # Remove trailing punctuation residues
    s = s.strip(" -—ㅡ.")
    # Limit length
    return s[:60]

def extract_title_from_chunk(pages):
    """First page of chunk: title is the prominent top line (not '연사의 유의 사항' or starting with '제')."""
    first_page_text = get_text_or_ocr(pages[0])
    lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]
    if not lines:
        return ""

    # Strategy: the title is usually the line(s) before "연사의 유의 사항" or "유의 사항"
    # OR: the line right after "제 N 번"
    title_lines = []

    for idx, line in enumerate(lines[:12]):
        # Skip "제N번" lines
        if re.match(r"^제\s*\d+\s*번\s*$", line):
            continue
        # Stop at common body keywords
        if re.match(r"^(연사의\s*)?유의\s*사항", line):
            break
        if re.search(r"유의\s*사항", line):
            break
        # Sometimes the title line is followed by a time marker like "(3분)"
        if re.search(r"\(\s*\d+\s*분\s*\)", line):
            break
        # Skip lines that are just numbers
        if re.fullmatch(r"[\d\s]+", line):
            continue
        # Skip footer-like
        if re.search(r"\bNo\.\s*\d+", line):
            continue
        title_lines.append(line)
        # Title usually 1-2 lines
        if len(title_lines) >= 2:
            break

    title = " ".join(title_lines).strip()
    return clean_title(title)

# Build chunks
chunks = []
for i in range(0, N, 2):
    pages = [i + 1]
    if i + 1 < N:
        pages.append(i + 2)
    chunks.append(pages)

# Assign talk numbers
# chunk idx 0 (pages 1-2) = Talk #40 NEW
# chunk idx 39 (pages 79-80) = Talk #40 ORIGINAL
# chunk idx N-1 = Talk #N for all other N (N=2..194, skipping 40 which has been handled)
results = []

for idx, pages in enumerate(chunks):
    chunk_num = idx + 1  # 1-indexed
    if chunk_num == 1:
        talk_num = 40
        suffix = "_신2026"  # The new 2026 version at front
    else:
        talk_num = chunk_num
        suffix = ""

    title = extract_title_from_chunk(pages)

    # Build filename
    num_s = f"{talk_num:03d}"
    base = f"{num_s}번"
    if title:
        base += f"_{title}"
    base += suffix + ".pdf"
    # Clean filename further
    base = re.sub(r"\s+", " ", base).strip()

    out_path = os.path.join(OUT_DIR, base)
    results.append({
        "chunk": chunk_num,
        "talk": talk_num,
        "suffix": suffix,
        "pages": pages,
        "title": title,
        "filename": base,
    })

    # Write the PDF
    new_pdf = fitz.open()
    new_pdf.insert_pdf(src, from_page=pages[0]-1, to_page=pages[-1]-1)
    new_pdf.save(out_path)
    new_pdf.close()

src.close()

# Write manifest
manifest_path = os.path.join(OUT_DIR, "_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Also write a readable manifest
txt_path = os.path.join(OUT_DIR, "_manifest.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(f"S-34 공개강연 골자 분할 매니페스트 ({len(results)}개 파일)\n")
    f.write("=" * 80 + "\n\n")
    for r in results:
        suffix_note = f"  [{r['suffix']}]" if r["suffix"] else ""
        f.write(f"#{r['talk']:3d}  pages {r['pages']}{suffix_note}\n")
        f.write(f"     title: {r['title'] or '(제목 추출 실패)'}\n")
        f.write(f"     file:  {r['filename']}\n\n")

print(f"Split done. {len(results)} files written to:")
print(f"  {OUT_DIR}")
print(f"Manifest: {manifest_path}")
print(f"Readable:  {txt_path}")

# Summary of any that might need attention
missing_titles = [r for r in results if not r["title"]]
print(f"\nFiles without extracted title: {len(missing_titles)}")
for r in missing_titles[:20]:
    print(f"  #{r['talk']:3d} pages {r['pages']}")
