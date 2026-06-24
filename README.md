# Hydra Q FincaOS V23.2

Streamlit app connected to Google Sheets public CSV.

Files required in the GitHub repo root:
- app.py
- requirements.txt
- README.md
- hydraq_logo.png
- cama_6_y_3.jpeg
- vista_sur.jpeg
- vista_este.jpeg

Changes in V23.2:
- Smaller bed reference photos.
- Calendar weeks run Monday to Sunday.
- Tree history shown as embedded chronological table.
- Climate tab adjusted to Frailes/weekly by default and reference thresholds.
- Progress tab uses aligned photo frames and placeholders per bed.


## V24 - Cambios incluidos

- Agrega soporte visual para fotos reales de junio en Camas 2 a 7.
- Las fotos se usan tanto en la sección Camas como en Avance.
- Elimina las referencias a fotos de muestra anteriores.
- Mejora eventos de cosecha para aceptar cantidad, unidad y cantidad normalizada para reportes.
- La sección de árboles ya no muestra una recomendación separada de dosis; la referencia queda centralizada en la pestaña Insumos.

### Archivos de fotos esperados en la raíz del repositorio

- cama_2_junio.jpeg
- cama_3_junio.jpeg
- cama_4_junio.jpeg
- cama_5_junio.jpeg
- cama_6_junio.jpeg
- cama_7_junio.jpeg

### Columnas recomendadas para EventosAgricolas / cosechas

- Cantidad
- Unidad_Medida
- Cantidad_Normalizada
- Unidad_Normalizada
- Tipo_Cosecha
- Destino
- Afecta_Inventario
- Notas_Cosecha
