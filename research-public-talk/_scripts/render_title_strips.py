import fitz
import os

p = r"C:\Users\yoone\Dropbox\congregation\research-public-talk\S-34_KO_공개강연_골자_1-194.pdf"
out_dir = r"C:\Users\yoone\tmp_titles2"
os.makedirs(out_dir, exist_ok=True)

d = fitz.open(p)
N = len(d)

for chunk_num in range(1, N // 2 + 1):
    first_page = 2 * chunk_num - 1
    if first_page > N:
        break
    page = d[first_page - 1]
    blocks = page.get_text("blocks")
    blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
    if not blocks:
        continue
    top_text = blocks[0][4].strip()
    kor = sum(1 for c in top_text if 0xAC00 <= ord(c) <= 0xD7A3)
    if kor >= 3 or len(top_text) < 3:
        continue

    # Use EXACT bbox of topmost block
    x0, y0, x1, y1, _, _, _ = blocks[0]
    # Add a small margin and cap left-right around block
    margin = 2
    rect = fitz.Rect(max(0, x0 - margin), max(0, y0 - margin),
                     min(page.rect.width, x1 + margin),
                     min(page.rect.height, y1 + margin))
    mat = fitz.Matrix(600/72, 600/72)  # 600 DPI
    pix = page.get_pixmap(matrix=mat, clip=rect)
    out_path = os.path.join(out_dir, f"title_{chunk_num:03d}.png")
    pix.save(out_path)

print("done, rendered", len(os.listdir(out_dir)), "title images")
