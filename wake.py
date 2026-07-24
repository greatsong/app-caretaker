# -*- coding: utf-8 -*-
"""apps.txt의 스트림릿 앱들을 진짜 브라우저로 방문해 깨워 둔다."""
import sys

from playwright.sync_api import sync_playwright

WAKE_BUTTON_TEXTS = ["get this app back up", "app back up", "Wake up"]
SLEEP_SCREEN_TEXTS = ["gone to sleep", "Zzzz"]


def visit(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    page.wait_for_timeout(10_000)  # 앱 또는 휴면 화면이 뜰 때까지 대기

    # 휴면 화면이면 깨우기 버튼을 눌러 준다
    for text in WAKE_BUTTON_TEXTS:
        button = page.get_by_text(text, exact=False)
        if button.count() > 0:
            print("  휴면 상태였음 → 깨우는 중 (잠시 대기)")
            button.first.click()
            page.wait_for_timeout(60_000)
            break

    # 다 기다린 뒤에도 휴면 화면 문구가 남아 있으면 실패로 계산한다.
    # 조용한 거짓 성공을 막아야 GitHub이 실패 메일로 고장을 알려 준다.
    for text in WAKE_BUTTON_TEXTS + SLEEP_SCREEN_TEXTS:
        if page.get_by_text(text, exact=False).count() > 0:
            raise RuntimeError(f"휴면 화면이 그대로임 (감지 문구: {text})")

    print("  방문 완료")


def main(list_path):
    urls = []
    with open(list_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)

    if not urls:
        print("apps.txt에 등록된 앱이 없습니다 — 통과")
        return 0

    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in urls:
            print(url)
            try:
                visit(page, url)
            except Exception as e:  # 한 앱이 실패해도 나머지는 계속
                failures += 1
                print(f"  실패: {e}")
        browser.close()

    print(f"\n총 {len(urls)}개 중 실패 {failures}개")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "apps.txt"))
