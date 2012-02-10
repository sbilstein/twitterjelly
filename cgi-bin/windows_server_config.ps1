echo "" > .\GetCelebMatchesJSON.py.tmp
Get-Content .\GetCelebMatchesJSON.py | ForEach-Object { $_ -replace "#!/usr/bin/env python", "#!C:\Python32\python.exe" } | Set-Content .\GetCelebMatchesJSON.py.tmp

rm .\GetCelebMatchesJSON.py
mv .\GetCelebMatchesJSON.py.tmp .\GetCelebMatchesJSON.py
rm .\GetCelebMatchesJSON.py.tmp

