"""gameofview.com(Cloudflare Pages 프로젝트 gameofview)에 홈페이지를 올린다.

사용: py -X utf8 deploy_cloudflare.py
키: C:/Users/wildm/.config/cloudflare/api_token (계정 토큰, Pages Write + Zone DNS Edit). 키는 출력·저장하지 않는다.
git에 올라간 사이트 파일만 임시 폴더에 모아 wrangler로 올린다(검사 스크립트·README·docs 제외).
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY_FILE = Path("C:/Users/wildm/.config/cloudflare/api_token")
ACCOUNT_ID = "7ab01a4153b553b8f1f6fe2b59485e14"
PROJECT = "gameofview"
SKIP = ("check_site.py", "README.md", ".gitignore", ".nojekyll", "deploy_cloudflare.py")


def main():
    files = subprocess.run(["git", "ls-files"], cwd=HERE, capture_output=True, text=True, check=True).stdout.split()
    with tempfile.TemporaryDirectory(prefix="gov-site-") as tmp:
        out = Path(tmp) / "site"
        for f in files:
            if f in SKIP or f.startswith("docs/"):
                continue
            dest = out / f
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(HERE / f, dest)
        env = dict(os.environ, CLOUDFLARE_API_TOKEN=KEY_FILE.read_text().strip(), CLOUDFLARE_ACCOUNT_ID=ACCOUNT_ID)
        # wrangler가 현재 폴더에 설정 파일을 만들지 않게 임시 폴더에서 실행
        rc = subprocess.run("npx --yes wrangler@4 pages deploy site --project-name %s --branch main --commit-dirty=true" % PROJECT,
                            cwd=tmp, env=env, shell=True).returncode
    sys.exit(rc)


if __name__ == "__main__":
    main()
