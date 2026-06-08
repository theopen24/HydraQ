# Hydra Q FincaOS MVP - Streamlit

## Archivos
- `app.py`: dashboard interactivo.
- `requirements.txt`: librerías necesarias.
- `Hydra_Q_FincaOS_V6_MVP_DEV_LookerReady.xlsx`: datos DEV del MVP.

## Cómo usar en Streamlit Cloud
1. Crear un repositorio en GitHub.
2. Subir estos 3 archivos al repo.
3. Entrar a Streamlit Cloud.
4. New app / Create app.
5. Seleccionar el repo.
6. Main file path: `app.py`.
7. Deploy.

## Cómo usar local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Uso
El dashboard lee la hoja `VistaCultivos`. Si esa hoja no existe, intenta construir la vista desde las 4 tablas del MVP.
