echo off
set USR_INPUT_STR=
rem ���͗v��
set /P USR_INPUT_STR="�����L�[���[�h����͂��Ă�������: "
rem ���͒lecho
echo %USR_INPUT_STR% ���������܂��B

cd /d "C:\merukari\pkg"

call merukari.exe %USR_INPUT_STR%

explorer C:\merukari\pkg\datum

pause

