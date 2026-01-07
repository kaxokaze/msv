rd /s /q "build"
rd /s /q "release"

call obfuscate.bat

py -3 create_executable.py

mkdir "release\\data\\"
mkdir "release\\bin\\"
mkdir "release\\legal\\"
mkdir "release\\cfg\\"

echo "copying binaries"
copy /y "..\\bin\\similarweb_5.5.7.xpi" "release\\bin\\"
copy /y "..\\bin\\similarweb_6_8_1_0.crx" "release\\bin\\"
copy /y "..\\bin\\chromedriver.exe" "release\\bin\\"
copy /y "..\\bin\\geckodriver.exe" "release\\bin\\"
copy /y "..\\bin\\phantomjs.exe" "release\\bin\\"
echo "copying data"
copy /y "..\\data\\proxies.txt" "release\\data\\"
copy /y "..\\data\\refs.txt" "release\\data\\"
copy /y "..\\data\\ua.txt" "release\\data\\"
copy /y "..\\data\\cookies.json" "release\\data\\"
copy /y "..\\cfg\\phantomjs_config.json" "release\\cfg\\"
copy /y "..\\legal\\*.txt" "release\\legal\\"
copy /y "assets\\icon.ico" "release\\"
copy /y "..\\docs\\Instruction-Manual.pdf" "release\\"
echo "All is said and done."