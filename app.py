import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Hydra Q FincaOS MVP", layout="wide", page_icon="🌱")

FILE_PATH = Path(__file__).parent / "Hydra_Q_FincaOS_V6_MVP_DEV_LookerReady.xlsx"

CROP_ICONS = {
    "Tomate normal": "🍅",
    "Tomate cherry": "🍅",
    "Lechuga": "🥬",
    "Pepino": "🥒",
    "Zanahoria": "🥕",
    "Cebollino": "🌱",
    "Apio": "🥬",
    "Espinaca": "🍃",
    "Vainica": "🫛",
    "Cebolla blanca": "🧅",
    "Cebolla morada": "🧅",
    "Acelga": "🥬",
    "Arúgula": "🌿",
    "Sandía": "🍉",
    "Ayote": "🎃",
    "Albahaca": "🌿",
}

STATUS_CLASS = {
    "Activa": "ok",
    "Próxima cosecha": "warn",
    "Dato faltante": "bad",
}

st.markdown("""
<style>
.main-title {font-size: 44px; font-weight: 800; color: #063b1f; margin-bottom: 0px;}
.subtitle {font-size: 18px; color: #5b5b5b; margin-bottom: 18px;}
.section-title {font-size: 30px; font-weight: 800; color: #063b1f; margin: 28px 0 14px 0; border-bottom: 2px solid #7FB069; padding-bottom: 6px;}
.card {background: white; border: 1px solid #e6e6e6; border-radius: 16px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); min-height: 210px; margin-bottom: 18px;}
.card.bad-border {border: 2px dashed #e53935;}
.bed-title {font-size: 20px; font-weight: 800; color: #063b1f; margin-bottom: 8px;}
.badge {display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 13px; font-weight: 700; margin-bottom: 10px;}
.ok {background: #dff3dc; color: #176b1a;}
.warn {background: #fff0c2; color: #9a6800;}
.bad {background: #ffdada; color: #b00020;}
.crop {display: inline-block; text-align: center; min-width: 105px; padding: 8px 10px; margin: 4px 4px; border-right: 1px solid #eeeeee;}
.icon {font-size: 50px; line-height: 1.1;}
.crop-name {font-weight: 700; font-size: 15px; margin-top: 6px;}
.qty {font-size: 18px; font-weight: 800; color: #222;}
.metric-box {background:#f7faf7; border:1px solid #e2eee2; border-radius:14px; padding:14px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    xl = pd.ExcelFile(FILE_PATH)
    if "VistaCultivos" in xl.sheet_names:
        df = pd.read_excel(FILE_PATH, sheet_name="VistaCultivos")
        return clean_view(df)

    fincas = pd.read_excel(FILE_PATH, sheet_name="Fincas")
    unidades = pd.read_excel(FILE_PATH, sheet_name="Unidades")
    cultivos = pd.read_excel(FILE_PATH, sheet_name="CatalogoCultivos")
    siembras = pd.read_excel(FILE_PATH, sheet_name="CultivosSembrados")

    df = siembras.merge(fincas, on="Finca_ID", how="left")
    df = df.merge(unidades, on=["Unidad_ID", "Finca_ID"], how="left")
    df = df.merge(cultivos, on="Cultivo_ID", how="left")
    return clean_view(df)


def first_existing(df, options, default=""):
    for col in options:
        if col in df.columns:
            return df[col]
    return pd.Series([default] * len(df))


def clean_view(df):
    out = pd.DataFrame()
    out["Finca"] = first_existing(df, ["Finca", "Finca_Nombre", "Nombre_Finca"])
    out["Unidad"] = first_existing(df, ["Unidad", "Unidad_Nombre", "Nombre_Unidad"])
    out["Cultivo"] = first_existing(df, ["Cultivo", "Cultivo_Nombre", "Nombre_Cultivo"])
    out["Cantidad"] = pd.to_numeric(first_existing(df, ["Cantidad"], 0), errors="coerce").fillna(0).astype(int)
    out["Estado"] = first_existing(df, ["Estado", "Estado_Actual"], "Sin estado")
    out["Alerta_Datos"] = first_existing(df, ["Alerta_Datos", "Estado_Ficha"], "")

    for new_col, candidates in {
        "Fecha_Base": ["Fecha_Base"],
        "Cosecha_Min": ["Cosecha_Min", "Fecha_Cosecha_Min"],
        "Cosecha_Max": ["Cosecha_Max", "Fecha_Cosecha_Max"],
    }.items():
        out[new_col] = pd.to_datetime(first_existing(df, candidates), errors="coerce")

    if "Mes_Cosecha" in df.columns:
        out["Mes_Cosecha"] = df["Mes_Cosecha"].fillna("Sin fecha")
    else:
        out["Mes_Cosecha"] = out["Cosecha_Min"].dt.strftime("%Y-%m").fillna("Sin fecha")

    def status(row):
        if pd.isna(row["Fecha_Base"]) or str(row["Alerta_Datos"]).lower().find("incompleta") >= 0:
            return "Dato faltante"
        if pd.notna(row["Cosecha_Min"]):
            days = (row["Cosecha_Min"].date() - date.today()).days
            if 0 <= days <= 30:
                return "Próxima cosecha"
        return "Activa"

    out["Visual_Status"] = out.apply(status, axis=1)
    return out


def crop_html(row):
    cultivo = row["Cultivo"]
    icon = CROP_ICONS.get(cultivo, "🌱")
    return f"""
    <div class="crop">
      <div class="icon">{icon}</div>
      <div class="crop-name">{cultivo}</div>
      <div class="qty">({row['Cantidad']})</div>
    </div>
    """


def bed_card(unidad, group):
    status_priority = "Activa"
    if (group["Visual_Status"] == "Dato faltante").any():
        status_priority = "Dato faltante"
    elif (group["Visual_Status"] == "Próxima cosecha").any():
        status_priority = "Próxima cosecha"
    badge_class = STATUS_CLASS[status_priority]
    bad_border = " bad-border" if status_priority == "Dato faltante" else ""
    crops = "".join(crop_html(row) for _, row in group.iterrows())
    return f"""
    <div class="card{bad_border}">
      <div class="bed-title">{unidad}</div>
      <div class="badge {badge_class}">{status_priority}</div>
      <div>{crops}</div>
    </div>
    """


df = load_data()

st.markdown('<div class="main-title">Qué hay sembrado en cada cama</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Hydra Q FincaOS MVP · vista interactiva</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtros")
    finca_filter = st.multiselect("Finca", sorted(df["Finca"].dropna().unique()), default=sorted(df["Finca"].dropna().unique()))
    unidad_filter = st.multiselect("Unidad", sorted(df["Unidad"].dropna().unique()))
    cultivo_filter = st.multiselect("Cultivo", sorted(df["Cultivo"].dropna().unique()))
    estado_filter = st.multiselect("Estado visual", sorted(df["Visual_Status"].dropna().unique()))

filtered = df[df["Finca"].isin(finca_filter)] if finca_filter else df.copy()
if unidad_filter:
    filtered = filtered[filtered["Unidad"].isin(unidad_filter)]
if cultivo_filter:
    filtered = filtered[filtered["Cultivo"].isin(cultivo_filter)]
if estado_filter:
    filtered = filtered[filtered["Visual_Status"].isin(estado_filter)]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cultivos activos", len(filtered))
m2.metric("Camas / unidades", filtered["Unidad"].nunique())
m3.metric("Próxima cosecha", int((filtered["Visual_Status"] == "Próxima cosecha").sum()))
m4.metric("Datos faltantes", int((filtered["Visual_Status"] == "Dato faltante").sum()))

for finca, finca_df in filtered.groupby("Finca", sort=True):
    st.markdown(f'<div class="section-title">📍 {finca}</div>', unsafe_allow_html=True)
    unidades = list(finca_df.groupby("Unidad", sort=True))
    for i in range(0, len(unidades), 3):
        cols = st.columns(3)
        for col, (unidad, group) in zip(cols, unidades[i:i+3]):
            with col:
                st.markdown(bed_card(unidad, group), unsafe_allow_html=True)

st.divider()
st.subheader("Detalle")
show_cols = ["Finca", "Unidad", "Cultivo", "Cantidad", "Estado", "Fecha_Base", "Cosecha_Min", "Cosecha_Max", "Visual_Status"]
st.dataframe(filtered[show_cols].sort_values(["Finca", "Unidad", "Cultivo"]), use_container_width=True, hide_index=True)
