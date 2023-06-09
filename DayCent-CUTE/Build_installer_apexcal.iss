; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A25DDF94-D21F-4000-90C3-86AA33B305E7}
AppName=DayCent-CUTE
AppVersion=1.0
AppPublisher=Agoro Carbon Alliance
AppPublisherURL=https://agorocarbonalliance.com/
DefaultDirName=C:\DayCent\DayCent-CUTE
DefaultGroupName=DayCent-CUTE
OutputBaseFilename=DayCent-CUTE_v1_winamd64_DDCentEVI
SetupIconFile=E:\AWorkshop\CUTE\CUTE2.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "E:\AWorkshop\CUTE\build\DayCent-CUTE.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\AWorkshop\CUTE\build\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\AWorkshop\CUTE\project\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\DayCent-CUTE 1.0"; Filename: "{app}\DayCent-CUTE.exe"
Name: "{group}\{cm:UninstallProgram,DayCent-CUTE}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\DayCent-CUTE 1.0"; Filename: "{app}\DayCent-CUTE.exe"; IconFilename: {app}\CUTE2.ico; 

[Run]
Filename: "{app}\DayCent-CUTE.exe"; Description: "{cm:LaunchProgram,DayCent-CUTE}"; Flags: nowait postinstall skipifsilent

