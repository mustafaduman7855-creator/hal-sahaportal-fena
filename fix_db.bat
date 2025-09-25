@echo off
echo ==============================
echo HALI SAHA PORTAL VERITABANI RESET
echo ==============================

REM Sanal ortamı aktive et
call venv\Scripts\activate

REM Eski veritabanını sil
if exist db.sqlite3 (
    del db.sqlite3
    echo db.sqlite3 silindi.
)

REM Migrations klasörlerini temizle (opsiyonel)
for /d %%i in (core\migrations) do (
    if exist "%%i\*.py" (
        del /Q "%%i\*.py"
        echo Migrations temizlendi.
    )
)

REM Yeni migration oluştur ve uygula
python manage.py makemigrations core
python manage.py migrate

echo ==============================
echo VERITABANI YENILENDI ✅
echo Simdi admin olusturmak icin:
echo python manage.py createsuperuser
echo ==============================

pause

