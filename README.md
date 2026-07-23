# app-caretaker — 잠자는 앱 돌보미 🤖

무료로 배포한 앱들이 잠들지 않게, 정해진 시간마다 로봇이 대신 찾아가는 저장소입니다.

## 왜 필요한가

| 서비스 | 무료 티어의 잠 | 이 저장소의 처방 |
|--------|---------------|-----------------|
| **Streamlit Community Cloud** | 방문이 끊기면 앱이 휴면 → 다음 방문자가 "깨우기" 화면에서 1~2분 대기 | 매일 2회, 진짜 브라우저(Playwright)로 접속해 깨워 둠 |
| **Supabase 무료 프로젝트** | 7일 미사용 시 일시정지 → 수동 복구 필요 | 매일 REST 요청 한 번으로 사용 기록 남김 |
| 구글 시트 + Apps Script | 잠들지 않음 | 할 일 없음 |

핵심: 스트림릿의 방문 감지는 웹소켓 기준이라 단순 핑(curl, UptimeRobot)으로는 안 됩니다.
꼭 브라우저로 접속해야 해서 Playwright를 씁니다.

## 사용법

### 스트림릿 앱 추가
[`apps.txt`](apps.txt)에 앱 주소를 한 줄에 하나씩 적으면 끝. `#`으로 시작하는 줄은 무시됩니다.

### Supabase 프로젝트 추가
키는 공개 저장소에 두면 안 되므로 **Settings → Secrets and variables → Actions**에
`SUPABASE_PINGS` 시크릿을 만들고, 한 줄에 하나씩 다음 형식으로 넣습니다.

```
프로젝트별명|https://xxxx.supabase.co|publishable키
```

### 바로 시험하기
Actions 탭 → **caretaker** → **Run workflow** 버튼으로 즉시 실행해 볼 수 있습니다.

## 실행 시간표

`.github/workflows/caretaker.yml`의 cron 두 줄 — 매일 **07:23 · 19:23 (한국시간)**.
GitHub Actions의 cron은 UTC 기준이라 한국시간에서 9시간을 빼서 적습니다.
무료 러너는 정시보다 몇 분 늦게 도는 것이 정상입니다.

## 수업 연계

서울대 평생교육원 「데이터 기반 바이브 코딩」 5일차 심화 자료의 실물 교보재입니다.
"내 앱이 잠든다"는 문제를 cron 자동화로 해결하는 첫 예시로 소개하고,
같은 원리의 더 큰 활용(데이터 자동 수집)은 [modudata](https://github.com/greatsong/modudata)에서 보여줍니다.
