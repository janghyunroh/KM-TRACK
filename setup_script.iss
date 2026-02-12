[Setup]
AppName=KM-TRACK
AppVersion=1.0
DefaultDirName={autopf}\KM-TRACK
DefaultGroupName=KM-TRACK
UninstallDisplayName=KM-TRACK (Keyboard & Mouse HAR Tracker)

OutputDir=Output
OutputBaseFilename=KM_TRACK_Setup

Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

; Show language selection dialog at startup
ShowLanguageDialog=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[CustomMessages]
english.LaunchApp=Launch KM-TRACK
korean.LaunchApp=KM-TRACK 실행하기

english.AppDescription=Keyboard & Mouse activity tracker for HAR research
korean.AppDescription=HAR 연구를 위한 키보드 및 마우스 활동 추적기

[Files]
Source: "dist\sensor_gui.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\Data"; Permissions: users-modify

[Icons]
Name: "{group}\KM-TRACK"; Filename: "{app}\sensor_gui.exe"
Name: "{commondesktop}\KM-TRACK"; Filename: "{app}\sensor_gui.exe"
Name: "{commonstartup}\KM-TRACK"; Filename: "{app}\sensor_gui.exe"

[Run]
Filename: "{app}\sensor_gui.exe"; Description: "{cm:LaunchApp}"; Flags: nowait postinstall skipifsilent
