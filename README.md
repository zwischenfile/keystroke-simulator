# Keystroke Simulator

Windows 환경에서 ID와 비밀번호를 클립보드에 복사하거나, 선택한 입력창에 자동으로 타이핑해 주는 PySide6 기반 GUI 도구입니다.

## 주요 기능

- 호스트 ID를 `호스트명\administrator` 형식으로 복사 또는 자동 입력
- PW 복사 또는 자동 입력
- 자동 입력 전 5초 카운트다운
- 항상 위에 표시 옵션
- ID/PW 입력값 삭제 버튼
- ID와 PW가 모두 입력된 상태에서 복사 또는 자동 입력 버튼을 누르면 `Log.txt`에 시간, ID, PW 기록
- 실행 시 관리자 권한 확인 후 권한이 없으면 경고 표시 및 종료

## 실행 환경

- Windows
- Python 3.10 이상 권장
- 관리자 권한

`PW.py`에서 사용하는 외부 패키지는 `requirements.txt`에 정리되어 있습니다.

## 설치

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

가상환경을 사용하지 않는 경우에도 의존성 설치는 다음 명령으로 가능합니다.

```powershell
py -m pip install -r requirements.txt
```

## 실행

이 프로그램은 관리자 권한으로 실행해야 합니다. 관리자 권한이 없으면 경고창을 표시한 뒤 종료합니다.

```powershell
py .\PW.py
```

## 사용 방법

1. `ID (호스트네임)` 입력칸에 호스트명 또는 ID 값을 입력합니다.
2. `PW` 입력칸에 비밀번호를 입력합니다.
3. 필요한 버튼을 누릅니다.
   - `ID 복사`: `입력한ID\administrator` 값을 클립보드에 복사합니다.
   - `PW 복사`: PW 값을 클립보드에 복사합니다.
   - `ID 타이핑`: 5초 뒤 `입력한ID\administrator` 값을 현재 포커스된 입력창에 자동 입력합니다.
   - `PW 타이핑`: 5초 뒤 PW 값을 현재 포커스된 입력창에 자동 입력합니다.
4. 자동 입력 버튼을 누른 뒤 5초 안에 실제 입력 대상 창으로 포커스를 옮깁니다.

## 로그

ID와 PW가 모두 입력된 상태에서 ID/PW 복사 또는 타이핑 버튼을 누르면 실행 파일과 같은 폴더의 `Log.txt`에 다음 형식으로 기록됩니다.

```text
2026-06-23 11:12:34 | ID=MYHOST | PW=password
```

`Log.txt`에는 민감한 정보가 포함될 수 있으므로 Git에 포함하지 않도록 `.gitignore`에 등록되어 있습니다.

## 보안 참고

- 현재 PW 입력칸은 마스킹되어 있지 않습니다.
- `Log.txt`에는 비밀번호가 평문으로 저장됩니다.
- 클립보드에 복사한 ID/PW는 다른 프로그램에서 읽을 수 있으므로 사용 후 필요한 경우 클립보드를 지워 주세요.
