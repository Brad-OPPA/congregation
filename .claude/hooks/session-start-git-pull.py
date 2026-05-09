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

sys.exit(0)
