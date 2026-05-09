#!/usr/bin/env python3
"""SessionStart 훅 — 회중 자료 작업 시작 시 자동 git pull.

원준님 지시 (2026-05-07): 다중 기기 작업 시 항상 최신 상태로 시작.
대상:
  1. {project}/.git (main branch — META)
  2. {project}/_automation/.git (master branch — automation)

정책:
- working tree dirty 면 SKIP + 경고 (자동 stash·rebase 안 함, 사용자 의도 보호)
- git pull --ff-only 만 시도 (merge commit 자동 생성 금지)
- 네트워크·권한 오류는 non-blocking — 세션은 진행
- 결과를 stderr 로 출력 (Claude 가 보는 컨텍스트)
"""
import os, subprocess, sys
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", "")).resolve()
if not PROJECT_DIR.exists():
    sys.exit(0)

REPOS = [
    (PROJECT_DIR, "main", "META"),
    (PROJECT_DIR / "_automation", "master", "automation"),
]

def run(cmd, cwd, timeout=15):
    try:
        r = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"

def pull_repo(repo_path: Path, branch: str, label: str):
    if not (repo_path / ".git").exists():
        return f"[{label}] .git 없음 — skip"

    # 1. clean check
    rc, out, _ = run(["git", "status", "--porcelain"], repo_path, timeout=8)
    if rc != 0:
        return f"[{label}] status 실패 — skip"
    if out:
        n = len([ln for ln in out.splitlines() if ln.strip()])
        return f"[{label}] dirty ({n} 변경) — pull SKIP (사용자 의도 보호)"

    # 2. fetch + ff-only pull
    rc, out, err = run(["git", "pull", "--ff-only", "origin", branch], repo_path, timeout=20)
    if rc == 0:
        if "Already up to date" in out or "이미 최신" in out:
            return f"[{label}] 최신 ({branch})"
        # extract last non-empty line for summary
        summary = (out.splitlines() + err.splitlines())[-1] if (out or err) else ""
        return f"[{label}] pulled ({branch}): {summary[:80]}"
    else:
        # network or auth fail — non-blocking
        return f"[{label}] pull 실패 ({branch}) — 계속 진행: {(err or out)[:120]}"

print("🔄 git pull (회중 자료 동기화)", file=sys.stderr)
for repo, branch, label in REPOS:
    print(f"  → {pull_repo(repo, branch, label)}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────
# 사용자 품질 표준 + 진행 상황 자동 인식 (2026-05-09 추가)
# 사용자 핵심 pain — "매번 새 클로드와 같은 이야기 또 하는 것" 해결.
# 회중 cwd 일 때 매 세션 시작 시 표준·NG·HANDOFF 핵심 자동 stderr 주입.
# ─────────────────────────────────────────────────────────────────────

SHARED = PROJECT_DIR / ".claude" / "shared"
STANDARD_FILE = SHARED / "user-quality-standard.md"
VOCAB_FILE = SHARED / "banned-vocabulary.md"

# 가장 최근 HANDOFF 파일 자동 발견
handoff_files = sorted(PROJECT_DIR.glob("HANDOFF-*.md"), reverse=True)
latest_handoff = handoff_files[0] if handoff_files else None


def extract_section(path: Path, heading_match: str, max_lines: int = 30) -> str:
    """파일에서 특정 헤더 섹션 추출."""
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        section_lines = []
        in_section = False
        for line in lines:
            if heading_match in line:
                in_section = True
                section_lines.append(line)
                continue
            if in_section:
                if line.startswith("## ") and len(section_lines) > 1:
                    break
                section_lines.append(line)
                if len(section_lines) >= max_lines:
                    break
        return "\n".join(section_lines)
    except Exception:
        return ""


print("\n📚 회중 자료 작업 컨텍스트 (매 세션 자동 주입 — 2026-05-09)", file=sys.stderr)
print("=" * 60, file=sys.stderr)

# 1. 사용자 품질 표준 핵심 원칙
if STANDARD_FILE.exists():
    section = extract_section(STANDARD_FILE, "🎯 핵심 원칙", 15)
    if section:
        print(f"\n📋 사용자 품질 표준 (정본: {STANDARD_FILE.relative_to(PROJECT_DIR)}):", file=sys.stderr)
        print(section, file=sys.stderr)

# 2. 사용자 NG 어휘 (최근 추가)
if VOCAB_FILE.exists():
    try:
        vocab_text = VOCAB_FILE.read_text(encoding="utf-8")
        # 2-bis 사용자 직접 명시 NG 섹션
        if "## 2-bis" in vocab_text:
            start = vocab_text.find("## 2-bis")
            end = vocab_text.find("## 2-ter", start)
            ng_section = vocab_text[start:end] if end > 0 else vocab_text[start:start+1500]
            print(f"\n🚫 사용자 NG 어휘 (정본: banned-vocabulary.md §2-bis):", file=sys.stderr)
            for line in ng_section.splitlines()[:20]:
                if line.strip().startswith("|") and "**" in line:
                    print(f"  {line}", file=sys.stderr)
    except Exception:
        pass

# 3. 가장 최근 HANDOFF 진행 상황
if latest_handoff:
    print(f"\n🚧 진행 상황 (HANDOFF: {latest_handoff.name}):", file=sys.stderr)
    # 핵심 의도 + 미해결 섹션
    for marker in ["사용자 핵심 의도", "진행 중 작업", "다음 세션 진입점"]:
        section = extract_section(latest_handoff, marker, 12)
        if section:
            print(section[:1200], file=sys.stderr)
            print("", file=sys.stderr)

print("=" * 60, file=sys.stderr)
print("→ 위 표준·NG·진행 상황 인식하고 작업 시작.", file=sys.stderr)
print("→ 사용자가 한 번 한 이야기는 영구 자산 — 또 묻지 말 것.", file=sys.stderr)

sys.exit(0)
