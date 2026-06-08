from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hydra Q FincaOS", layout="wide", page_icon="🌱")

DATA_FILE = "FincaOS_Data.xlsx"
BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / DATA_FILE
if not FILE_PATH.exists():
    st.error(f"No se encontró el archivo de datos requerido: {DATA_FILE}")
    st.stop()

CROP_META = {
    "Disponible": {"icon": "➕", "class": "available"},
    "Lechuga": {"icon": "🥬", "class": "lettuce"},
    "Acelga": {"icon": "🍂", "class": "chard"},
    "Pepino": {"icon": "🥒", "class": "cucumber"},
    "Sandía": {"icon": "🍉", "class": "watermelon"},
    "Ayote": {"icon": "🎃", "class": "squash"},
    "Albahaca": {"icon": "🌱", "class": "basil"},
    "Tomate cherry": {"icon": "🍅", "class": "tomato-cherry"},
    "Tomate normal": {"icon": "🍅", "class": "tomato"},
    "Culantro": {"icon": "🌿", "class": "cilantro"},
    "Cebolla blanca": {"icon": "🧅", "class": "onion-white"},
    "Cebolla morada": {"icon": "🧅", "class": "onion-purple"},
    "Chile dulce": {"icon": "🫑", "class": "pepper"},
    "Arúgula": {"icon": "🌶️", "class": "arugula"},
    "Zucchini": {"icon": "🥒", "class": "zucchini"},
    "Zuchinni": {"icon": "🥒", "class": "zucchini"},
    "Zanahoria": {"icon": "🥕", "class": "carrot"},
    "Cebollino": {"icon": "🌾", "class": "chives"},
    "Perejil italiano": {"icon": "☘️", "class": "parsley"},
    "Perejil normal": {"icon": "🌿", "class": "parsley-normal"},
    "Apio": {"icon": "🥬", "class": "celery"},
    "Espinaca": {"icon": "🍃", "class": "spinach"},
}

STATUS_CLASS = {
    "Activa": "ok",
    "Próxima cosecha": "warn",
    "Dato faltante": "bad",
    "No activa": "inactive",
    "Disponible": "available-badge",
}

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f3d25 0%, #14532d 42%, #0f3d25 100%);
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);} 
.block-container {padding-top: 1.5rem;}
.metric-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.14);
    min-height: 86px;
}
.metric-label {color:#31543d; font-size:13px; font-weight:800; margin-bottom:6px;}
.metric-value {color:#0f3d25; font-size:28px; font-weight:950; line-height:1;}
.metric-note {color:#64748b; font-size:12px; margin-top:5px;}
.section-title {
    font-size: 28px;
    font-weight: 950;
    color: white;
    margin: 26px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(255,255,255,0.25);
}
.bed-header {display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:8px;}
.bed-title {font-size: 20px; font-weight: 950; color: #ffffff; text-shadow:0 1px 4px rgba(0,0,0,0.35);}
.badge {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:900;}
.ok {background:#dcfce7; color:#166534;}
.warn {background:#fef3c7; color:#92400e;}
.bad {background:#fee2e2; color:#991b1b;}
.inactive {background:#e5e7eb; color:#374151;}
.available-badge {background:#dbeafe; color:#1d4ed8;}
.crop-card {
    border: 1px solid #e3eadf;
    background: #ffffff;
    border-radius: 16px;
    padding: 12px 10px;
    margin-bottom: 10px;
    min-height: 190px;
    box-shadow: 0 2px 8px rgba(15, 61, 37, 0.08);
}
.icon-circle {
    width: 56px; height: 56px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 29px; margin-bottom: 8px;
}
.lettuce {background:#dcfce7;}
.chard {background:#d9f99d;}
.cucumber {background:#bbf7d0;}
.watermelon {background:#fee2e2;}
.squash {background:#ffedd5;}
.basil {background:#ccfbf1;}
.tomato-cherry {background:#fecaca;}
.tomato {background:#fee2e2;}
.cilantro {background:#d1fae5;}
.onion-white {background:#f3f4f6;}
.onion-purple {background:#ede9fe;}
.pepper {background:#dcfce7;}
.arugula {background:#fef3c7;}
.zucchini {background:#ccfbf1;}
.carrot {background:#fed7aa;}
.chives {background:#ecfccb;}
.parsley {background:#d1fae5;}
.parsley-normal {background:#bbf7d0;}
.celery {background:#e0f2fe;}
.spinach {background:#dcfce7;}
.available {background:#dbeafe;}
.crop-name {font-weight: 950; color:#123d24; font-size: 15px; margin-bottom:2px;}
.qty {font-size: 18px; font-weight: 950; color:#111827;}
.info-line {font-size: 13px; color:#475569; margin-top: 3px;}
.empty-card {padding: 24px 10px; text-align:center; color:#6b7280; font-weight:800;}
[data-testid="stSidebar"] {background: #0b2f1a;}
[data-testid="stSidebar"] * {color: #ffffff !important;}
[data-testid="stSidebar"] div[data-baseweb="select"] * {color: #0f172a !important;}
[data-testid="stSidebar"] input {color: #0f172a !important;}
[data-testid="stSidebar"] label {color: #ffffff !important; font-weight: 800;}
.app-title {color:#ffffff; font-size:42px; font-weight:950; letter-spacing:0.5px; margin:0 0 18px 0; text-shadow:0 2px 8px rgba(0,0,0,0.35);} 
</style>
""",
    unsafe_allow_html=True,
)


def find_col(df, candidates, default=None):
    for c in candidates:
        if c in df.columns:
            return c
    return default


def load_data():
    xl = pd.ExcelFile(FILE_PATH)
    fincas = pd.read_excel(FILE_PATH, sheet_name="Fincas")
    unidades = pd.read_excel(FILE_PATH, sheet_name="Unidades")

    if "VistaCultivos" in xl.sheet_names:
        df = pd.read_excel(FILE_PATH, sheet_name="VistaCultivos")
    else:
        cultivos = pd.read_excel(FILE_PATH, sheet_name="CatalogoCultivos")
        siembras = pd.read_excel(FILE_PATH, sheet_name="CultivosSembrados")
        df = siembras.merge(fincas, on="Finca_ID", how="left")
        df = df.merge(unidades, on=["Unidad_ID", "Finca_ID"], how="left")
        df = df.merge(cultivos, on="Cultivo_ID", how="left")

    return clean_view(df), clean_units(unidades, fincas)


def clean_units(unidades, fincas):
    out = unidades.copy()
    if "Finca_Nombre" not in out.columns:
        out = out.merge(fincas[["Finca_ID", "Finca_Nombre"]], on="Finca_ID", how="left")
    out["Unidad"] = out.get("Unidad_Nombre", out.get("Unidad", ""))
    out["Finca"] = out.get("Finca_Nombre", out.get("Finca", ""))
    out["Estado_Unidad"] = out.get("Estado", "Activa")
    return out


def clean_view(df):
    out = pd.DataFrame()
    out["Siembra_ID"] = df[find_col(df, ["Siembra_ID"], None)] if "Siembra_ID" in df.columns else [f"ROW_{i}" for i in range(len(df))]
    out["Finca"] = df[find_col(df, ["Finca", "Finca_Nombre", "Nombre_Finca"], None)].astype(str)
    out["Unidad"] = df[find_col(df, ["Unidad", "Unidad_Nombre", "Nombre_Unidad"], None)].astype(str)
    out["Cultivo"] = df[find_col(df, ["Cultivo", "Cultivo_Nombre", "Nombre_Cultivo"], None)].astype(str)
    out["Cantidad"] = pd.to_numeric(df[find_col(df, ["Cantidad"], None)], errors="coerce").fillna(0).astype(int)
    out["Estado_Actual"] = df[find_col(df, ["Estado_Actual", "Estado"], None)].fillna("Sin estado").astype(str)
    out["Estado_Unidad"] = df[find_col(df, ["Estado_Unidad"], None)].fillna("Activa").astype(str) if "Estado_Unidad" in df.columns else "Activa"
    out["Alerta_Datos"] = df[find_col(df, ["Alerta_Datos", "Estado_Ficha"], None)].fillna("").astype(str) if ("Alerta_Datos" in df.columns or "Estado_Ficha" in df.columns) else ""

    for col in ["Fecha_Siembra", "Fecha_Trasplante", "Fecha_Base", "Cosecha_Min", "Cosecha_Max"]:
        source = find_col(df, [col], None)
        out[col] = pd.to_datetime(df[source], errors="coerce") if source else pd.NaT

    out["Mes_Cosecha"] = out["Cosecha_Min"].dt.strftime("%Y-%m").fillna("Sin fecha")
    out["Visual_Status"] = out.apply(visual_status, axis=1)
    return out


def visual_status(row):
    if str(row.get("Cultivo", "")).lower() == "disponible" or str(row.get("Estado_Actual", "")).lower() == "disponible":
        return "Disponible"
    if str(row.get("Estado_Unidad", "")).lower().startswith("no activa"):
        return "No activa"
    if pd.isna(row["Fecha_Base"]) or "falta" in str(row["Alerta_Datos"]).lower() or "incompleta" in str(row["Alerta_Datos"]).lower():
        return "Dato faltante"
    if pd.notna(row["Cosecha_Min"]):
        days = (row["Cosecha_Min"].date() - date.today()).days
        if 0 <= days <= 30:
            return "Próxima cosecha"
    return "Activa"


def fmt_date(value):
    if pd.isna(value):
        return "Sin fecha"
    return pd.to_datetime(value).strftime("%d %b %Y")


def base_date_label(row):
    if pd.notna(row["Fecha_Trasplante"]):
        return f"Trasplante: {fmt_date(row['Fecha_Trasplante'])}"
    if pd.notna(row["Fecha_Siembra"]):
        return f"Siembra: {fmt_date(row['Fecha_Siembra'])}"
    return "Sin fecha base"


def days_label(value, prefix):
    if pd.isna(value):
        return f"{prefix}: Sin fecha"
    days = (pd.to_datetime(value).date() - date.today()).days
    if days > 0:
        return f"{prefix}: en {days} días"
    if days == 0:
        return f"{prefix}: hoy"
    return f"{prefix}: hace {abs(days)} días"


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def crop_card(row, idx):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})
    quantity = row["Cantidad"] if crop != "Disponible" else ""

    st.markdown(
        f"""
        <div class="crop-card">
            <div class="icon-circle {meta['class']}">{meta['icon']}</div>
            <div class="crop-name">{crop}</div>
            <div class="qty">{quantity}</div>
            <div class="info-line">Estado: <b>{row['Estado_Actual']}</b></div>
            <div class="info-line">{base_date_label(row)}</div>
            <div class="info-line">{days_label(row['Cosecha_Min'], 'Cosecha min')}</div>
            <div class="info-line">{days_label(row['Cosecha_Max'], 'Cosecha max')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def unit_status(unit_row, group):
    if str(unit_row.get("Estado_Unidad", "")).lower().startswith("no activa"):
        return "No activa"
    if group is not None and len(group) > 0:
        if (group["Visual_Status"] == "Dato faltante").any():
            return "Dato faltante"
        if (group["Visual_Status"] == "Disponible").any():
            return "Disponible"
        if (group["Visual_Status"] == "Próxima cosecha").any():
            return "Próxima cosecha"
    return "Activa"


def bed_panel(unit_row, crops_df):
    unidad = unit_row["Unidad"]
    status = unit_status(unit_row, crops_df)
    badge_class = STATUS_CLASS.get(status, "ok")
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="bed-header">
                <div class="bed-title">{unidad}</div>
                <span class="badge {badge_class}">{status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if str(unit_row.get("Estado_Unidad", "")).lower().startswith("no activa"):
            st.markdown('<div class="empty-card">No activa</div>', unsafe_allow_html=True)
            return
        if crops_df is None or crops_df.empty:
            st.markdown('<div class="empty-card">Sin cultivos activos</div>', unsafe_allow_html=True)
            return
        cols_per_row = 2 if len(crops_df) <= 4 else 3
        records = list(crops_df.sort_values(["Visual_Status", "Cultivo"]).iterrows())
        for start in range(0, len(records), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, (idx, row) in zip(cols, records[start:start + cols_per_row]):
                with col:
                    crop_card(row, idx)


df, units = load_data()

st.markdown('<div class="app-title">FincaOS</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtros")
    st.caption(f"Datos: {DATA_FILE}")
    finca_options = [f for f in ["Moravia", "Frailes"] if f in set(units["Finca"].dropna().unique())] + [f for f in sorted(units["Finca"].dropna().unique()) if f not in ["Moravia", "Frailes"]]
    finca_filter = st.multiselect("Finca", finca_options, default=finca_options)
    unidad_options = sorted(units[units["Finca"].isin(finca_filter)]["Unidad"].dropna().unique()) if finca_filter else sorted(units["Unidad"].dropna().unique())
    unidad_filter = st.multiselect("Unidad", unidad_options)
    cultivo_filter = st.multiselect("Cultivo", sorted(df["Cultivo"].dropna().unique()))
    estado_filter = st.multiselect("Estado visual", sorted(set(list(df["Visual_Status"].dropna().unique()) + ["No activa"])))
    show_detail_table = st.checkbox("Mostrar tabla detalle", value=False)

filtered_units = units[units["Finca"].isin(finca_filter)] if finca_filter else units.copy()
if unidad_filter:
    filtered_units = filtered_units[filtered_units["Unidad"].isin(unidad_filter)]

filtered = df[df["Finca"].isin(finca_filter)] if finca_filter else df.copy()
if unidad_filter:
    filtered = filtered[filtered["Unidad"].isin(unidad_filter)]
if cultivo_filter:
    filtered = filtered[filtered["Cultivo"].isin(cultivo_filter)]
if estado_filter:
    filtered = filtered[filtered["Visual_Status"].isin(estado_filter)]
    active_units = filtered["Unidad"].unique().tolist()
    filtered_units = filtered_units[(filtered_units["Unidad"].isin(active_units)) | ((filtered_units["Estado_Unidad"] == "No activa") & ("No activa" in estado_filter))]

active_crops = filtered[(filtered["Cultivo"] != "Disponible") & (filtered["Estado_Unidad"] != "No activa")]
next_rows = active_crops[pd.notna(active_crops["Cosecha_Min"])].copy()
next_date = "Sin próxima"
next_note = ""
if not next_rows.empty:
    next_rows["days"] = (next_rows["Cosecha_Min"].dt.date - date.today()).apply(lambda x: x.days)
    next_rows = next_rows[next_rows["days"] >= 0]
    if not next_rows.empty:
        upcoming = next_rows.sort_values("Cosecha_Min").iloc[0]
        next_date = fmt_date(upcoming["Cosecha_Min"])
        next_note = f"{upcoming['Cultivo']} · {upcoming['Unidad']}"

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    metric_card("Cultivos activos", len(active_crops), "sin contar espacios disponibles")
with m2:
    metric_card("Camas visibles", filtered_units["Unidad"].nunique(), "según filtros")
with m3:
    metric_card("Próxima Cosecha Disponible", next_date, next_note)
with m4:
    metric_card("Espacios disponibles", int((filtered["Visual_Status"] == "Disponible").sum()), "oportunidad de siembra")
with m5:
    metric_card("Errores de datos", int((filtered["Visual_Status"] == "Dato faltante").sum()), "falta información")

for finca, unit_group in filtered_units.groupby("Finca", sort=False):
    st.markdown(f'<div class="section-title">📍 {finca}</div>', unsafe_allow_html=True)
    unit_records = list(unit_group.sort_values("Unidad").iterrows())
    for start in range(0, len(unit_records), 2):
        cols = st.columns(2)
        for col, (_, unit_row) in zip(cols, unit_records[start:start + 2]):
            with col:
                crops = filtered[filtered["Unidad"] == unit_row["Unidad"]]
                bed_panel(unit_row, crops)

if show_detail_table:
    st.divider()
    st.subheader("Detalle de datos")
    show_cols = [
        "Finca", "Unidad", "Cultivo", "Cantidad", "Estado_Actual",
        "Fecha_Siembra", "Fecha_Trasplante", "Cosecha_Min", "Cosecha_Max", "Visual_Status"
    ]
    table = filtered[show_cols].copy().sort_values(["Finca", "Unidad", "Cultivo"])
    st.dataframe(table, use_container_width=True, hide_index=True)
