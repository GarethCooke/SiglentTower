@echo off
rem Builds publish\makerworld\SiglentTower-STLs.zip from the fitted STLs (parts\, jigs\, coupons\spacers\) for the MakerWorld model files.
rem Run from the repo root. The zip is not committed.
cd /d "%~dp0..\.."
powershell -NoProfile -Command "Compress-Archive -Force -Path parts\*.stl, parts\column\*.stl, parts\door\*.stl, parts\drawer\*.stl, parts\inserts\*.stl, parts\mini\*.stl, parts\sill\*.stl, parts\tiles\*.stl, parts\top\*.stl, parts\tpu\*.stl, parts\wiring\*.stl, jigs\*.stl, coupons\spacers\*.stl -DestinationPath publish\makerworld\SiglentTower-STLs.zip"
echo publish\makerworld\SiglentTower-STLs.zip
