# Keystroke Simulator

Windows 환경에서 ID와 PW를 클립보드에 복사하거나 지정한 입력창에 자동 타이핑하는 간단한 PySide6 GUI 도구입니다.

## 주요 기능

- ID를 `호스트명\administrator` 형식으로 복사
- PW 복사
- ID 또는 PW 자동 타이핑
- 항상 위에 표시 옵션
- ID와 PW가 모두 입력된 상태에서 ID/PW 관련 버튼을 누르면 `Log.txt`에 시간, ID, PW 기록

## 실행 환경

- Windows
- Python 3.10 이상 권장
- 관리자 권한
- PySide6
- pydirectinput
- pyperclip

## 설치

```powershell
py -m pip install -r requirements.txt
```

## 실행

이 프로그램은 관리자 권한으로 실행되어야 합니다. 관리자 권한이 없는 상태로 실행하면 경고창을 표시한 뒤 자동으로 종료됩니다.

```powershell
py .\PW.py
```

## 사용 방법

1. `ID` 입력칸에 호스트명 또는 ID 값을 입력합니다.
2. `PW` 입력칸에 비밀번호를 입력합니다.
3. 필요한 버튼을 누릅니다.
   - `ID 복사`: `ID\administrator` 형식으로 클립보드에 복사합니다.
   - `PW 복사`: PW를 클립보드에 복사합니다.
   - `ID 타이핑`: 5초 뒤 `ID\administrator` 형식을 자동 입력합니다.
   - `PW 타이핑`: 5초 뒤 PW를 자동 입력합니다.
4. 자동 타이핑 버튼을 누른 뒤에는 5초 안에 실제 입력할 창으로 포커스를 옮깁니다.

## 로그

ID와 PW가 모두 입력된 상태에서 ID/PW 관련 버튼을 누르면 소스 파일이 있는 폴더의 `Log.txt`에 아래 형식으로 기록됩니다.

```text
2026-06-23 11:12:34 | ID=MYHOST | PW=password
```

`Log.txt`에는 민감한 정보가 포함될 수 있으므로 GitHub에 올리지 않도록 `.gitignore`에 포함되어 있습니다.
