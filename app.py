from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hydra Q FincaOS", layout="wide", page_icon="🌱")

EXCEL_CANDIDATES = [
    "Hydra_Q_FincaOS_V9_Streamlit.xlsx",
]

BASE_DIR = Path(__file__).parent
FILE_PATH = next((BASE_DIR / f for f in POSSIBLE_FILES if (BASE_DIR / f).exists()), BASE_DIR / POSSIBLE_FILES[0])

CROP_META = {
    "Lechuga": {"icon": "🥬", "class": "leafy"},
    "Acelga": {"icon": "☘️", "class": "chard"},
    "Pepino": {"icon": "🥒", "class": "cucumber"},
    "Sandía": {"icon": "🍉", "class": "watermelon"},
    "Ayote": {"icon": "🎃", "class": "squash"},
    "Albahaca": {"icon": "🌱", "class": "basil"},
    "Tomate cherry": {"icon": "🍅", "class": "tomato-cherry"},
    "Tomate normal": {"icon": "🍅", "class": "tomato"},
    "Culantro": {"icon": "🌿", "class": "cilantro"},
    "Cebolla blanca": {"icon": "⚪🧅", "class": "onion-white"},
    "Cebolla morada": {"icon": "🟣🧅", "class": "onion-purple"},
    "Chile dulce": {"icon": "🫑", "class": "pepper"},
    "Arúgula": {"icon": "🍃", "class": "arugula"},
    "Zucchini": {"icon": "🥒", "class": "zucchini"},
    "Zuchinni": {"icon": "🥒", "class": "zucchini"},
    "Zanahoria": {"icon": "🥕", "class": "carrot"},
    "Cebollino": {"icon": "🌾", "class": "chives"},
    "Apio": {"icon": "🥬", "class": "celery"},
    "Espinaca": {"icon": "🍀", "class": "spinach"},
}

STATUS_CLASS = {
    "Activa": "ok",
    "Próxima cosecha": "warn",
    "Dato faltante": "bad",
    "No activa": "inactive",
}

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f3d25 0px, #0f3d25 260px, #f4f7f2 260px, #f4f7f2 100%);
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);} 
.hero {
    padding: 26px 10px 18px 10px;
    margin-bottom: 10px;
}
.main-title {
    font-size: 46px;
    line-height: 1.05;
    font-weight: 900;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-chip {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    color: #e9ffe8;
    padding: 7px 12px;
    border-radius: 999px;
    margin-top: 12px;
    font-size: 14px;
    font-weight: 700;
}
.section-title {
    font-size: 28px;
    font-weight: 900;
    color: white;
    background: #14532d;
    border-radius: 16px;
    padding: 12px 18px;
    margin: 22px 0 14px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.12);
}
.small-muted {color:#5f6f61; font-size:13px;}
.bed-header {display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:8px;}
.bed-title {font-size: 20px; font-weight: 900; color: #0f3d25;}
.badge {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:800;}
.ok {background:#dcfce7; color:#166534;}
.warn {background:#fef3c7; color:#92400e;}
.bad {background:#fee2e2; color:#991b1b;}
.inactive {background:#e5e7eb; color:#374151;}
.crop-card {
    border: 1px solid #e3eadf;
    background: #ffffff;
    border-radius: 16px;
    padding: 12px 10px;
    margin-bottom: 10px;
    min-height: 150px;
    box-shadow: 0 2px 8px rgba(15, 61, 37, 0.06);
}
.icon-circle {
    width: 58px; height: 58px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; margin-bottom: 8px;
}
.leafy {background:#dcfce7;}
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
.arugula {background:#ecfccb;}
.zucchini {background:#ccfbf1;}
.carrot {background:#fed7aa;}
.chives {background:#ecfccb;}
.celery {background:#e0f2fe;}
.spinach {background:#dcfce7;}
.crop-name {font-weight: 900; color:#123d24; font-size: 15px; margin-bottom:2px;}
.qty {font-size: 18px; font-weight: 900; color:#111827;}
.info-line {font-size: 13px; color:#475569; margin-top: 2px;}
.detail-box {background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:10px; margin-top:8px; font-size:13px;}
.empty-card {padding: 24px 10px; text-align:center; color:#6b7280; font-weight:700;}
.stButton button {width: 100%; border-radius: 10px; font-weight: 700;}
</style>
""",
    unsafe_allow_html=True,
)


def find_col(df, candidates, default=None):
    for c in candidates:
        if c in df.columns:
            return c
    return default


@st.cache_data
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


def days_to_harvest(row):
    if pd.isna(row["Cosecha_Min"]):
        return "Sin cosecha estimada"
    days = (row["Cosecha_Min"].date() - date.today()).days
    if days > 0:
        return f"Cosecha en {days} días"
    if days == 0:
        return "Cosecha desde hoy"
    return f"Cosecha estimada hace {abs(days)} días"


def crop_card(row, idx):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "leafy"})
    detail_key = f"detail_{row['Siembra_ID']}_{idx}"

    st.markdown(
        f"""
        <div class="crop-card">
            <div class="icon-circle {meta['class']}">{meta['icon']}</div>
            <div class="crop-name">{crop}</div>
            <div class="qty">{row['Cantidad']}</div>
            <div class="info-line">Estado: <b>{row['Estado_Actual']}</b></div>
            <div class="info-line">{base_date_label(row)}</div>
            <div class="info-line">{days_to_harvest(row)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Ver fechas" if not st.session_state.get(detail_key, False) else "Ocultar fechas", key=f"btn_{detail_key}"):
        st.session_state[detail_key] = not st.session_state.get(detail_key, False)

    if st.session_state.get(detail_key, False):
        st.markdown(
            f"""
            <div class="detail-box">
                <b>Fecha usada para cálculo:</b> {base_date_label(row)}<br>
                <b>Fecha siembra:</b> {fmt_date(row['Fecha_Siembra'])}<br>
                <b>Fecha trasplante:</b> {fmt_date(row['Fecha_Trasplante'])}<br>
                <b>Cosecha mínima:</b> {fmt_date(row['Cosecha_Min'])}<br>
                <b>Cosecha máxima:</b> {fmt_date(row['Cosecha_Max'])}
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
        if crops_df is None or crops_df.empty:
            st.markdown('<div class="empty-card">Sin cultivos activos</div>', unsafe_allow_html=True)
            return
        cols_per_row = 2 if len(crops_df) <= 4 else 3
        records = list(crops_df.sort_values("Cultivo").iterrows())
        for start in range(0, len(records), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, (idx, row) in zip(cols, records[start:start + cols_per_row]):
                with col:
                    crop_card(row, idx)


df, units = load_data()

st.markdown(
    '<div class="hero"><h1 class="main-title">¿Qué hay sembrado en cada cama?</h1>'
    '<div class="hero-chip">Vista interactiva por finca, cama y cultivo</div></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filtros")
    finca_options = sorted(units["Finca"].dropna().unique())
    finca_filter = st.multiselect("Finca", finca_options, default=finca_options)
    unidad_options = sorted(units[units["Finca"].isin(finca_filter)]["Unidad"].dropna().unique()) if finca_filter else sorted(units["Unidad"].dropna().unique())
    unidad_filter = st.multiselect("Unidad", unidad_options)
    cultivo_filter = st.multiselect("Cultivo", sorted(df["Cultivo"].dropna().unique()))
    estado_filter = st.multiselect("Estado visual", sorted(set(list(df["Visual_Status"].dropna().unique()) + ["No activa"])))
    show_detail_table = st.checkbox("Mostrar tabla detalle", value=True)

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

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cultivos", len(filtered))
m2.metric("Camas visibles", filtered_units["Unidad"].nunique())
m3.metric("Próxima cosecha", int((filtered["Visual_Status"] == "Próxima cosecha").sum()))
m4.metric("No activas", int((filtered_units["Estado_Unidad"] == "No activa").sum()))

for finca, unit_group in filtered_units.groupby("Finca", sort=True):
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
