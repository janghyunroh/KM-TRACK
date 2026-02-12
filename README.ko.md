# 🟦 KM-TRACK

[![Language](https://img.shields.io/badge/language-English-green)](README.md)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

<img src="./image.png"/>

**K**eyboard & **M**ouse **T**race for **R**ecognition of **A**ctivity **C**omputing **K**ernel

**KM-TRACK**은 사용자의 키보드 및 마우스 사용량을 실시간으로 수집하고 모니터링하여 **HAR (Human Activity Recognition)** 연구 데이터셋을 구축하기 위한 전문 도구입니다. 사용자의 키보드, 마우스 클릭, 마우스 이동 이벤트를 백그라운드에서 수집하며, 실시간 그래프 모니터링 기능을 제공합니다.

---

## 📥 1. 다운로드 및 설치 (Download)

아래 링크를 클릭하여 최신 설치 프로그램(`KM_TRACK_Setup.exe`)을 다운로드하세요.

👉 **[최신 버전 다운로드 (Click Here)](https://github.com/janghyunroh/KM-TRACK/releases/latest/download/KM_TRACK_Setup.exe)**

> **참고:** 윈도우 보안 경고(SmartScreen)가 뜰 경우, **'추가 정보' -> '실행'**을 클릭해 주세요. (개인 개발자 서명이 없는 경우 발생할 수 있습니다.)

---

## ✨ 2. 주요 기능 (Features)

- **자동 수집:** PC 부팅 시 자동 실행되어 백그라운드에서 데이터를 수집합니다.
- **실시간 모니터링:** 트레이 아이콘을 통해 실시간 활동량 그래프를 확인할 수 있습니다.
- **데이터 효율화:** 이벤트가 발생하지 않는 유휴 시간(Idle)은 0으로 처리하여 저장 용량을 최적화합니다.
- **개인화:** 설치 시 PC 식별 이름(Participant ID)을 설정하여 데이터를 구분합니다.
- **안전한 데이터 보존:** 프로그램을 삭제하더라도 수집된 데이터 파일은 보존됩니다.

---

## 🚀 3. 사용 방법 (Usage)

### 1. 초기 설정

1. 설치 완료 후 프로그램이 자동 실행됩니다.
2. **PC 식별 이름 입력창**이 뜨면, 부여받은 ID(예: `User_01`, `Participant_A`)를 입력하세요.

### 2. 작동 확인

- 윈도우 우측 하단 작업 표시줄(트레이)에 **파란색 네모 아이콘(🟦)**이 보이면 정상 작동 중입니다.
- 아이콘을 **우클릭**하면 메뉴가 나타납니다.
  - **모니터링 열기:** 실시간 그래프 대시보드를 엽니다.
  - **종료:** 데이터 수집을 중단하고 프로그램을 끕니다.

### 3. 그래프 모니터링

- **1분 / 30분 / 6시간 / 24시간** 단위로 활동량 변화를 확인할 수 있습니다.
- Y축 값은 **10초당 평균 이벤트 발생 횟수(Counts/10s)**로 정규화되어 표시됩니다.

---

## 📊 4. 데이터 저장 형식 (Data Format)

데이터는 `내 문서 > HAR_Data` 폴더(또는 설치 폴더 내 `Data`)에 CSV 파일로 저장됩니다.  
파일명 예시: `2026-02-12_User_01.csv`

| 컬럼명 (Column)       | 설명 (Description)                         |
| :-------------------- | :----------------------------------------- |
| **Timestamp**         | 데이터 기록 시간 (YYYY-MM-DD HH:MM:SS)     |
| **Keyboard_Count**    | 3초 간 입력된 키보드 타건 횟수 합계        |
| **Mouse_Click_Count** | 3초 간 입력된 마우스 클릭 횟수 합계        |
| **Mouse_Move_Count**  | 3초 간 감지된 마우스 이동 이벤트 횟수 합계 |

---

## 🛠️ 개발 환경 설정 (For Developers)

이 소프트웨어를 직접 수정하거나 빌드하고 싶다면 아래 절차를 따르세요.

#### 1. 저장소 클론

```bash
git clone [https://github.com/janghyunroh/KM-TRACK.git](https://github.com/janghyunroh/KM-TRACK.git)

```

#### 2. 필수 라이브러리 설치

```bash
pip install -r requirements.txt

```

#### 3. 실행

```bash
python sensor_gui.py

```

#### 4. EXE 파일 빌드 (PyInstaller 필요)

```bash
python -m PyInstaller --noconsole --onefile --hidden-import=pynput --hidden-import=pystray --hidden-import=matplotlib --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=tkinter sensor_gui.py

```

이후 배포를 위해 셋업 프로그램을 생성하려면 `Inno Setup`을 다운받아 `iss` 스크립트를 수정 후 컴파일하시면 됩니다.

---

## 📝 라이선스 (License)

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---
