echo off
set USR_INPUT_STR=
rem 入力要求
set /P USR_INPUT_STR="検索キーワードを入力してください: "
rem 入力値echo
echo %USR_INPUT_STR% を検索します。

cd /d "C:\merukari\pkg"

start merukari.exe %USR_INPUT_STR%

pause


