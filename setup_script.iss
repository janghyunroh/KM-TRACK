; 스크립트 파일명: setup_script.iss 로 저장하세요.

[Setup]
; 프로그램 기본 정보
AppName=HAR Sensor
AppVersion=1.0
DefaultDirName={autopf}\HARSensor
DefaultGroupName=HAR Sensor
UninstallDisplayName=HAR Sensor (데이터 수집 도구)

; 결과물(설치파일) 설정
OutputDir=userdocs:Desktop
OutputBaseFilename=HAR_Sensor_Setup
Compression=lzma
SolidCompression=yes

; 관리자 권한 필수 (Program Files 설치 및 권한 부여를 위해)
PrivilegesRequired=admin

[Files]
; 1. 실행 파일 (경로 수정 필수!)
Source: "D:\Projects\00_NRF\00_Data_Collection\00_Virtual_Sensor\dist\sensor_gui.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2. 설명서 파일 (경로 수정 필수!)
Source: "D:\Projects\00_NRF\00_Data_Collection\00_Virtual_Sensor\README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; ★ [핵심] Data 폴더 생성 및 쓰기 권한 부여
; Users 그룹에게 Modify 권한을 주어, 관리자 권한 없이도 파일 저장 가능하게 함
Name: "{app}\Data"; Permissions: users-modify

[Icons]
; 바탕화면 및 시작 메뉴 바로가기
Name: "{group}\HAR Sensor"; Filename: "{app}\sensor_gui.exe"
Name: "{commondesktop}\HAR Sensor"; Filename: "{app}\sensor_gui.exe"
; 시작 프로그램 자동 등록
Name: "{commonstartup}\HAR Sensor"; Filename: "{app}\sensor_gui.exe"

[Run]
; 설치 완료 후 즉시 실행 옵션
Filename: "{app}\sensor_gui.exe"; Description: "설치 완료 후 프로그램 실행"; Flags: nowait postinstall skipifsilent