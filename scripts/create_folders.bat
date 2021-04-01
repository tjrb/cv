@echo off
tree /F

echo do you want to create the foldes?(y/n)
set /p INPUT= (y/n): %=%
IF %INPUT%==y (goto test) else pause
exit

:test
echo creating folders:
md data
md data\images
md data\segmentations
md output
md output\preprocess_data
md output\train_data
tree
pause
EXIT /B 0

