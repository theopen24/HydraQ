# FincaOS - Google Sheets Public Version

Esta versión lee datos directamente desde Google Sheets usando URL CSV pública.

## Archivos requeridos en GitHub
- app.py
- requirements.txt
- README.md

## Importante
El Google Sheet debe estar compartido como:
Cualquier persona con el enlace → Lector

## Verificación en app.py
Debe existir:
SPREADSHEET_ID = "1ixV756fBEQPzMck3kNuG24X2JJkgnauXE5IXAIAGwR8"

No debe existir:
- FILE_PATH
- pd.ExcelFile
- FincaOS_Data.xlsx
- gspread
- google-auth
