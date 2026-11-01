"""Static site checks. Run with py check_site.py; Python standard library only.

Checks published HTML/CSS/JS/SVG, not local scripts or documentation.
Locale checks use asset names, not OCR. Browser behavior needs a browser check.
"""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
HOST = "gameofview.com"
BRAND = "Game of View"
OLD_BRAND = re.compile(r"우아한차트|woowa\s*chart", re.I)
EXCLUDED = {".git", "docs", "__pycache__", "node_modules", ".agents", ".codex"}
BANNED = re.compile(
    r"trading\s*view|트레이딩\s*뷰|트뷰|go\s*charting|고차팅|"
    r"trend\s*spider|트렌드\s*스파이더|meta\s*trader|메타\s*트레이더|"
    r"매억남|사\s*보세요|수익\s*보장|guaranteed\s+(?:profits?|returns?)",
    re.I,
)
# Drawing tools are real features; only product-category wording is forbidden.
OLD_CATEGORY = re.compile(r"연습\s*도구|차트\s*도구|도구를\s*사용|(?:practice|trading)\s+tool\b", re.I)
LEGAL_PAGES = ("terms.html", "privacy.html", "refund.html", "contact.html")


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.ids = set()
        self.words = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.add(attrs["id"])

    handle_startendtag = handle_starttag

    def handle_data(self, data):
        self.words.append(data)


def check_site(root=ROOT):
    root = Path(root).resolve()
    errors = []
    files = sorted(p for p in root.rglob("*") if p.is_file()
                   and not EXCLUDED.intersection(p.relative_to(root).parts)
                   and p.suffix in {".html", ".css", ".js", ".svg"})
    sources = {p: p.read_text(encoding="utf-8-sig") for p in files}
    pages = {p: Page(s) for p, s in sources.items() if p.suffix == ".html"}
    refs = 0
    media = set()

    def require(condition, message):
        if not condition:
            errors.append(message)

    def check_ref(owner, value, asset=False):
        nonlocal refs
        parsed = urlsplit(value)
        if parsed.netloc and parsed.netloc != HOST:
            require(not asset, f"{owner.name}: external asset {value}")
            return
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            require(not asset or parsed.scheme == "data", f"{owner.name}: unsupported asset {value}")
            return
        path = unquote(parsed.path)
        if parsed.netloc or path.startswith("/"):
            target = root / path.lstrip("/")
        else:
            target = owner.parent / path if path else owner
        target = target.resolve()
        if target.is_dir():
            target /= "index.html"
        refs += 1
        require(target.is_relative_to(root) and target.is_file(), f"{owner.name}: missing local path {value}")
        if parsed.fragment and target in pages:
            require(unquote(parsed.fragment) in pages[target].ids, f"{owner.name}: missing anchor {value}")
        if target.suffix in {".jpg", ".png", ".webp", ".svg", ".mp4", ".webm"}:
            media.add(target)
        locale = "ko" if owner == root / "index.html" else "en" if owner == root / "en/index.html" else None
        if locale and "media" in target.parts:
            if "shots" in target.parts:
                require(target.name.startswith(locale + "-"), f"{owner.name}: wrong screenshot language {value}")
            elif target.name.startswith("promo_"):
                require(target.name.startswith("promo_" + locale), f"{owner.name}: wrong promo language {value}")

    for path, source in sources.items():
        label = path.relative_to(root).as_posix()
        text = source
        if path in pages:
            page = pages[path]
            text += " " + " ".join(page.words)
            text += " " + " ".join(str(v) for _, a in page.tags for v in a.values() if v)
            for tag, attrs in page.tags:
                for key in ("href", "src", "poster", "action", "data" if tag == "object" else "xlink:href"):
                    if attrs.get(key):
                        check_ref(path, attrs[key], asset=tag in {"script", "img", "video", "audio", "source", "object"}
                                  or (tag == "link" and attrs.get("rel") in {"stylesheet", "icon"}))
                for item in attrs.get("srcset", "").split(","):
                    if item.strip():
                        check_ref(path, item.strip().split()[0], asset=True)
                if tag == "meta" and attrs.get("property") in {"og:image", "og:url"}:
                    check_ref(path, attrs.get("content", ""), asset=attrs["property"] == "og:image")
                require(not (tag == "script" and not attrs.get("src")), f"{label}: inline script")
        for match in BANNED.finditer(text):
            errors.append(f"{label}: forbidden wording: {match.group()}")
        # The contact address and one-time storage migration are intentional.
        brand_text = text.replace("woowachart@gmail.com", "")
        if path == root / "lang.js":
            brand_text = brand_text.replace('"woowachart-language"', "")
        for match in OLD_BRAND.finditer(brand_text):
            errors.append(f"{label}: old product name: {match.group()}")
        if path in pages:
            for match in OLD_CATEGORY.finditer(text):
                errors.append(f"{label}: old product category: {match.group()}")
        if path.suffix == ".css":
            for value in re.findall(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", source):
                check_ref(path, value.strip(), asset=True)
            for value in re.findall(r"@import\s+['\"]([^'\"]+)", source):
                check_ref(path, value, asset=True)

    for relative, locale, category, subtitle in (
        ("index.html", "ko", "차트 트레이딩 게임", "과거 차트로 하는 트레이딩 게임"),
        ("en/index.html", "en", "chart trading game", "A trading game played on real past charts"),
    ):
        path = root / relative
        require(path in pages, f"Missing page: {relative}")
        if path not in pages:
            continue
        page, source = pages[path], sources[path]
        title = re.search(r"<title>(.*?)</title>", source, re.S)
        require(title and category in title[1], f"{relative}: game category missing from title")
        require(subtitle in re.sub(r"<[^>]+>", "", source), f"{relative}: hero game subtitle missing")
        metadata = {a.get("property", a.get("name")): a.get("content", "") for t, a in page.tags if t == "meta"}
        expected_home = f"https://{HOST}/" + ("en/" if locale == "en" else "")
        require(any(t == "link" and a.get("rel") == "canonical" and a.get("href") == expected_home
                    for t, a in page.tags), f"{relative}: wrong canonical URL")
        require(metadata.get("og:url") == expected_home, f"{relative}: wrong OG URL")
        require(metadata.get("og:site_name") == BRAND, f"{relative}: wrong OG product name")
        require(BRAND in metadata.get("og:title", ""), f"{relative}: OG product title missing")
        require(category in metadata.get("og:description", ""), f"{relative}: OG game category missing")
        footer = source.split("<footer", 1)[-1]
        notice = ("차트 트레이딩 게임이에요 · 실제 거래·실제 돈이 오가지 않아요 · 투자 조언이 아니에요"
                  if locale == "ko" else "It's a chart trading game · No real trading or real money involved · It's not investment advice")
        require(notice in re.sub(r"<[^>]+>", "", footer), f"{relative}: game notice missing")
        alternates = {a.get("hreflang"): a.get("href") for t, a in page.tags if t == "link" and a.get("rel") == "alternate"}
        for language, suffix in (("ko", "/"), ("en", "/en/"), ("x-default", "/")):
            require(alternates.get(language) == f"https://{HOST}{suffix}", f"{relative}: invalid hreflang {language}")
        header = Page(source.split("<header", 1)[-1].split("</header>", 1)[0])
        choices = {a.get("data-language"): a for t, a in header.tags if t == "a" and "data-language" in a}
        for language in ("ko", "en"):
            require(bool(choices.get(language, {}).get("href")), f"{relative}: missing language link {language}")
        require(choices.get(locale, {}).get("aria-current") == "page", f"{relative}: current language not marked")
        scripts = [a for t, a in page.tags if t == "script"]
        require(bool(scripts) and scripts[0].get("src", "").endswith("lang.js")
                and not {"async", "defer", "type"}.intersection(scripts[0]), f"{relative}: blocking lang.js must load first")
        if scripts and scripts[0].get("src", "").endswith("lang.js"):
            before_script = source.split("<script", 1)[0]
            require("<link" not in before_script and "<title" not in before_script, f"{relative}: lang.js must be at start of head")

    # Policy pages must be present as readable HTML, including without JavaScript.
    for locale, prefix in (("ko", ""), ("en", "en/")):
        for name in LEGAL_PAGES:
            path = root / (prefix + name)
            require(path in pages, f"Missing page: {prefix}{name}")

    site_js = sources.get(root / "site.js", "")
    settings = {}
    for key in ("SELLER_NAME", "CONTACT_EMAIL"):
        match = re.search(rf'const {key} = "([^"\n]+)";', site_js)
        require(bool(match), f"site.js: missing {key} constant")
        if match:
            settings[key] = match[1]

    for path, page in pages.items():
        label = path.relative_to(root).as_posix()
        source = sources[path]
        title = re.search(r"<title>(.*?)</title>", source, re.S)
        require(title and BRAND in title[1], f"{label}: product name missing from title")
        for class_name in ("brand", "footer-name"):
            match = re.search(rf'<(?:a|span)\b[^>]*class="{class_name}"[^>]*>(.*?)</(?:a|span)>', source, re.S)
            require(match and BRAND in "".join(Page(match[1]).words),
                    f"{label}: product name missing from {class_name}")
        locale = "en" if path.parent == root / "en" else "ko"
        prefix = "" if path.name != "404.html" else "/"
        footer_match = re.search(r"<footer\b[^>]*>(.*?)</footer>", source, re.S)
        require(bool(footer_match), f"{label}: missing footer")
        footer = Page(footer_match[1] if footer_match else "")
        links = {a.get("href") for t, a in footer.tags if t == "a"}
        for name in LEGAL_PAGES:
            require(prefix + name in links, f"{label}: missing footer policy link {name}")
        for marker, key in (("data-seller-name", "SELLER_NAME"), ("data-contact-email", "CONTACT_EMAIL")):
            require(any(marker in a for _, a in footer.tags), f"{label}: missing footer {marker}")
            for match in re.finditer(rf'<(span|a)\b[^>]*\b{marker}\b[^>]*>(.*?)</\1>', source, re.S):
                require(match[2] == settings.get(key), f"{label}: {marker} HTML fallback differs from {key}")
        for tag, attrs in page.tags:
            if tag == "a" and "data-contact-email" in attrs:
                require(attrs.get("href") == "mailto:" + settings.get("CONTACT_EMAIL", ""),
                        f"{label}: email href differs from CONTACT_EMAIL")
        require(any(t == "script" and a.get("src", "").endswith("site.js") for t, a in page.tags),
                f"{label}: missing shared site.js")

        if path.name == "index.html":
            notice = re.search(r'<p class="purchase-policy">(.*?)</p>', source, re.S)
            require(bool(notice) and all(f'href="{name}"' in notice[1] for name in ("terms.html", "refund.html")),
                    f"{label}: missing purchase policy links")
        if path.name not in LEGAL_PAGES:
            continue
        require('datetime="2026-10-31"' in source, f"{label}: missing effective date")
        require('id="main"' in source and len([t for t, _ in page.tags if t == "h1"]) == 1,
                f"{label}: missing main or unique heading")
        require(any(t == "html" and a.get("lang") == locale for t, a in page.tags), f"{label}: wrong language")
        expected = f"https://{HOST}/" + ("en/" if locale == "en" else "") + path.name
        require(any(t == "link" and a.get("rel") == "canonical" and a.get("href") == expected
                    for t, a in page.tags), f"{label}: wrong canonical URL")
        alternates = {a.get("hreflang"): a.get("href") for t, a in page.tags if t == "link" and a.get("rel") == "alternate"}
        for language, directory in (("ko", ""), ("en", "en/"), ("x-default", "")):
            require(alternates.get(language) == f"https://{HOST}/{directory}{path.name}",
                    f"{label}: wrong policy alternate {language}")
        header = Page(source.split("<header", 1)[-1].split("</header>", 1)[0])
        choices = {a.get("data-language"): a for t, a in header.tags if t == "a" and "data-language" in a}
        for language in ("ko", "en"):
            expected_link = (("../" if language == "ko" else "") if locale == "en"
                             else ("" if language == "ko" else "en/")) + path.name
            require(choices.get(language, {}).get("href") == expected_link,
                    f"{label}: language switch must preserve document ({language})")
        require(choices.get(locale, {}).get("aria-current") == "page", f"{label}: missing current language")
        scripts = [a for t, a in page.tags if t == "script"]
        require(bool(scripts) and scripts[0].get("src", "").endswith("lang.js")
                and not {"async", "defer", "type"}.intersection(scripts[0]), f"{label}: blocking lang.js must load first")

    ignored = (root / ".gitignore").read_text(encoding="utf-8-sig").splitlines()
    for pattern in ("/media/enc.py", "/docs/superpowers/"):
        require(pattern in ignored, f".gitignore: missing {pattern}")
    return list(dict.fromkeys(errors)), len(pages), refs, len(media)


if __name__ == "__main__":
    failures, page_count, ref_count, media_count = check_site()
    for failure in failures:
        print("FAIL:", failure)
    print(f"{'FAIL' if failures else 'PASS'}: {page_count} HTML pages, {ref_count} local references, "
          f"{media_count} media files, {len(failures)} errors")
    print("Static checks only; screenshot locale is checked by filename, not OCR.")
    sys.exit(bool(failures))
