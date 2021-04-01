@echo off
tree /F

echo do you want to create the foldes?(y/n)
set /p INPUT= (y/n): %=%
IF %INPUT%==y (goto test) else pause
exit

:test
echo creating folders:
md models
md models\darknet
md models\onnx
md scripts
tree
pause
EXIT /B 0

