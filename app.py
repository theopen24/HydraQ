from pathlib import Path
from datetime import date, datetime, timedelta
import calendar
from textwrap import dedent

import pandas as pd
import streamlit as st
import gspread

st.set_page_config(page_title="Finca OS Dev", layout="wide", page_icon="🌱")

SPREADSHEET_ID = "1ixV756fBEQPzMck3kNuG24X2JJkgnauXE5IXAIAGwR8"
BASE_DIR = Path(__file__).parent
LOGO_FILE = BASE_DIR / "hydraq_logo.png"

CROP_META = {
    "Disponible": {"icon": "➕", "class": "available"},
    "Lechuga": {"icon": "🥬", "class": "lettuce"},
    "Acelga": {"icon": "🍀", "class": "chard"},
    "Pepino": {"icon": "🥒", "class": "cucumber"},
    "Sandía": {"icon": "🍉", "class": "watermelon"},
    "Ayote": {"icon": "🎃", "class": "squash"},
    "Albahaca": {"icon": "🌱", "class": "basil"},
    "Tomate cherry": {"icon": "🍅", "class": "tomato-cherry"},
    "Tomate normal": {"icon": "🍅", "class": "tomato"},
    "Culantro": {"icon": "🌿", "class": "cilantro"},
    "Cebolla blanca": {"icon": "🧅", "class": "onion"},
    "Cebolla morada": {"icon": "🧅", "class": "onion"},
    "Chile dulce": {"icon": "🫑", "class": "pepper"},
    "Arúgula": {"icon": "🥗", "class": "arugula"},
    "Arugula": {"icon": "🥗", "class": "arugula"},
    "Zucchini": {"icon": "🥒", "class": "zucchini"},
    "Zuchinni": {"icon": "🥒", "class": "zucchini"},
    "Zanahoria": {"icon": "🥕", "class": "carrot"},
    "Cebollino": {"icon": "🌱", "class": "chives"},
    "Perejil italiano": {"icon": "☘️", "class": "parsley"},
    "Perejil normal": {"icon": "🌿", "class": "parsley-normal"},
    "Apio": {"icon": "🥬", "class": "celery"},
    "Espinaca": {"icon": "🍃", "class": "spinach"},
}

STATUS_CLASS = {
    "Activa": "ok",
    "Dato faltante": "bad",
    "No activa": "inactive",
    "Disponible": "available-badge",
}

MONTHS_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f3d25 0%, #14532d 42%, #0f3d25 100%);
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);} 
.block-container {padding-top: 1.35rem;}
.app-title {
    color:#ffffff; font-size:42px; font-weight:950; letter-spacing:0.5px;
    margin:0 0 18px 0; text-shadow:0 2px 8px rgba(0,0,0,0.35);
}
.metric-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 18px;
    padding: 13px 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.14);
    min-height: 88px;
}
.metric-label {color:#31543d; font-size:12px; font-weight:900; margin-bottom:6px;}
.metric-value {color:#0f3d25; font-size:24px; font-weight:950; line-height:1.05;}
.metric-note {color:#64748b; font-size:11px; margin-top:5px;}
.dashboard-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
    gap:10px;
    margin: 6px 0 14px 0;
}
.dash-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(255,255,255,0.50);
    border-radius: 14px;
    padding: 10px 10px;
    box-shadow: 0 5px 14px rgba(0,0,0,0.12);
    min-height: 62px;
}
.dash-label {color:#31543d; font-size:10px; font-weight:950; text-transform:uppercase; letter-spacing:.2px;}
.dash-value {color:#0f3d25; font-size:20px; font-weight:950; line-height:1.05; margin-top:3px;}
.dash-note {color:#64748b; font-size:10px; margin-top:4px; line-height:1.15;}
.dash-panel {
    background: rgba(255,255,255,0.94);
    border-radius: 16px;
    padding: 13px 14px;
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 5px 16px rgba(0,0,0,0.12);
    margin-bottom:12px;
}
.dash-panel-title {font-size:16px; font-weight:950; color:#0f3d25; margin-bottom:8px;}
.dash-line {font-size:13px; color:#334155; margin:5px 0;}
.dash-pill {display:inline-block; padding:3px 8px; border-radius:999px; font-size:11px; font-weight:900; margin-right:5px;}
.pill-green {background:#dcfce7; color:#166534;}
.pill-yellow {background:#fef3c7; color:#92400e;}
.pill-red {background:#fee2e2; color:#991b1b;}
.pill-blue {background:#dbeafe; color:#1d4ed8;}
.section-title {
    font-size: 28px;
    font-weight: 950;
    color: white;
    margin: 26px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(255,255,255,0.25);
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2.5px solid rgba(255,255,255,0.86) !important;
    border-radius: 20px !important;
    background: rgba(255,255,255,0.10) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255,255,255,1.0) !important;
}
.bed-header {display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:8px;}
.bed-title {font-size: 20px; font-weight: 950; color: #ffffff; text-shadow:0 1px 4px rgba(0,0,0,0.35);}
.badge {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:900;}
.ok {background:#dcfce7; color:#166534;}
.bad {background:#fee2e2; color:#991b1b;}
.inactive {background:#e5e7eb; color:#374151;}
.available-badge {background:#dbeafe; color:#1d4ed8;}
.crop-card {
    border: 1px solid #e3eadf;
    background: #ffffff;
    border-radius: 16px;
    padding: 12px 10px;
    margin-bottom: 10px;
    min-height: 188px;
    box-shadow: 0 2px 8px rgba(15, 61, 37, 0.08);
}
.crop-card.harvest-ready {
    background: #e7f8df;
    border: 2px solid #86c96f;
    box-shadow: 0 4px 14px rgba(34, 197, 94, 0.18);
}
.crop-card.available-card {
    background: #eef8ff;
    border: 2px dashed #60a5fa;
    min-height: 150px;
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
.onion {background:#f3f4f6;}
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
.info-line.past-harvest {color:#b91c1c; font-weight:950;}
.empty-card {padding: 24px 10px; text-align:center; color:#d1d5db; font-weight:800;}
[data-testid="stSidebar"] {background: #0b2f1a;}
[data-testid="stSidebar"] * {color: #ffffff !important;}
[data-testid="stSidebar"] div[data-baseweb="select"] * {color: #0f172a !important;}
[data-testid="stSidebar"] input {color: #0f172a !important;}
[data-testid="stSidebar"] label {color: #ffffff !important; font-weight: 800;}
.calendar-toolbar {
    background: rgba(255,255,255,0.96);
    border-radius: 18px;
    padding: 16px 18px;
    margin: 10px 0 16px 0;
    border: 1px solid rgba(255,255,255,0.65);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.calendar-title {color:#0f172a; font-size:26px; font-weight:950; margin-bottom:4px;}
.calendar-note {color:#64748b; font-size:13px; font-weight:700;}
.calendar-filter-panel {
    background: rgba(8, 28, 18, 0.86);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 18px;
    padding: 14px 16px;
    margin: 8px 0 16px 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.16);
}
.calendar-filter-panel label, .calendar-filter-panel p, .calendar-filter-panel span {
    color: #ffffff !important;
    font-weight: 800;
}
.week-card {
    background: rgba(255,255,255,0.94);
    border: 2px solid rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 10px;
    min-height: 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    margin-bottom: 12px;
}
.week-title {font-size:16px; font-weight:950; color:#0f3d25; margin-bottom:2px;}
.week-range {font-size:11px; color:#64748b; font-weight:800; margin-bottom:8px;}
.event-card {
    border-radius: 12px;
    padding: 7px 8px;
    margin-bottom: 6px;
    border: 1px solid #e5e7eb;
    background:#ffffff;
}
.event-card.ready {background:#e7f8df; border:2px solid #86c96f;}
.event-card.soon {background:#fffbeb; border:2px solid #fbbf24;}
.event-card.future {background:#f8fafc; border:1px solid #cbd5e1;}
.event-card.overdue {background:#fee2e2; border:2px solid #ef4444;}
.event-card.available {background:#e7f8df; border:2px solid #86c96f;}
.event-row {display:flex; gap:9px; align-items:flex-start;}
.event-icon {font-size:20px; width:26px; text-align:center;}
.event-crop {font-weight:950; color:#0f172a; font-size:13px;}
.event-meta {font-size:11px; color:#475569; margin-top:2px; font-weight:700;}
.event-date {font-size:11px; margin-top:4px; font-weight:950;}
.ready-text {color:#15803d;}
.soon-text {color:#b45309;}
.future-text {color:#2563eb;}
.overdue-text {color:#b91c1c; font-weight:950;}
.wip-card {
    background: rgba(255,255,255,0.95);
    border: 2px solid rgba(255,255,255,0.85);
    border-radius: 18px;
    padding: 28px 24px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.14);
    color:#0f172a;
    font-weight:900;
}
.wip-title {font-size:24px; font-weight:950; color:#0f3d25; margin-bottom:8px;}
.wip-text {font-size:15px; color:#475569; font-weight:700;}
.no-events {color:#94a3b8; font-size:12px; font-weight:800; text-align:center; margin-top:12px;}
/* Quitar barra/línea larga debajo de las pestañas */
[data-baseweb="tab-list"] {border-bottom: none !important; box-shadow:none !important; gap: 22px !important;}
[data-baseweb="tab-border"] {display:none !important;}
[data-baseweb="tab-highlight"] {background-color:#ffffff !important; height:3px !important;}
[data-baseweb="tab"] {color:#ffffff !important; font-weight:900 !important;}
[data-baseweb="tab"][aria-selected="true"] {color:#ffffff !important;}
.tree-card {
    background: rgba(255,255,255,0.95);
    border: 2px solid rgba(255,255,255,0.88);
    border-radius: 18px;
    padding: 14px 14px;
    min-height: 154px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.16);
    margin-bottom: 14px;
}
.tree-row {display:flex; gap:14px; align-items:center;}
.tree-icon {font-size:48px; width:66px; height:66px; border-radius:50%; background:#dcfce7; display:flex; align-items:center; justify-content:center; flex-shrink:0;}
.tree-name {font-size:18px; color:#0f172a; font-weight:950; margin-bottom:8px;}
.tree-line {font-size:13px; color:#334155; font-weight:750; margin-top:4px;}
.tree-pill {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:950; margin-left:5px;}
.phen-vegetativo {background:#dcfce7; color:#166534;}
.phen-floracion {background:#fce7f3; color:#9d174d;}
.phen-fructificacion {background:#fef3c7; color:#92400e;}
.phen-llenado {background:#dbeafe; color:#1d4ed8;}
.phen-recuperacion {background:#ede9fe; color:#5b21b6;}
.health-bueno {background:#dcfce7; color:#166534;}
.health-atencion {background:#fef3c7; color:#92400e;}
.health-estres {background:#fee2e2; color:#991b1b;}

.event-section-title {font-size:24px; font-weight:950; color:#ffffff; margin:24px 0 12px 0; border-bottom:2px solid rgba(255,255,255,0.25); padding-bottom:6px;}
.ag-event-card {background: rgba(255,255,255,0.95); border: 2px solid rgba(255,255,255,0.88); border-radius: 16px; padding: 12px 14px; margin-bottom: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.14);}
.ag-event-top {display:flex; justify-content:space-between; gap:10px; align-items:flex-start;}
.ag-event-title {font-size:16px; font-weight:950; color:#0f172a;}
.ag-event-meta {font-size:12px; color:#475569; font-weight:750; margin-top:3px;}
.ag-event-pill {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:950;}
.event-completado {background:#dcfce7; color:#166534;}
.event-pendiente {background:#fef3c7; color:#92400e;}
.event-no-empezado {background:#e0f2fe; color:#075985;}
.event-vencido {background:#fee2e2; color:#991b1b;}
.control-line {font-size:12px; color:#334155; font-weight:750; margin-top:6px;}
.control-pill {display:inline-block; padding:3px 8px; border-radius:999px; font-size:11px; font-weight:950; margin-left:5px;}
.insumo-card {background:rgba(255,255,255,0.95); border:2px solid rgba(255,255,255,0.85); border-radius:16px; padding:12px; margin-bottom:10px; color:#0f172a;}
.insumo-name {font-size:16px; font-weight:950; color:#0f3d25;}
.insumo-meta {font-size:12px; color:#475569; font-weight:750; margin-top:4px;}
.history-line {font-size:12px; color:#334155; font-weight:750; margin-top:6px;}
.history-pill {display:inline-block; padding:3px 8px; border-radius:999px; background:#eef2ff; color:#3730a3; font-size:11px; font-weight:950; margin:2px 3px 2px 0;}
.next-abono {font-size:12px; color:#0f172a; font-weight:800; margin-top:6px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:7px 8px;}
.next-abono.overdue {background:#fef2f2; border-color:#fecaca; color:#991b1b;}

</style>
""",
    unsafe_allow_html=True,
)


def find_col(df, candidates, default=None):
    for c in candidates:
        if c in df.columns:
            return c
    return default


def is_available_placeholder(row):
    return str(row.get("Cultivo", "")).strip().lower() == "disponible" or str(row.get("Estado_Actual", "")).strip().lower() == "disponible"


def is_harvest_ready(row):
    if is_available_placeholder(row):
        return False
    today = date.today()
    for col in ["Cosecha_Min", "Cosecha_Max"]:
        val = row.get(col)
        if pd.notna(val) and pd.to_datetime(val).date() < today:
            return True
    return False


def visual_status(row):
    if str(row.get("Estado_Unidad", "")).lower().startswith("no activa"):
        return "No activa"
    if is_available_placeholder(row):
        return "Disponible"
    if pd.isna(row["Fecha_Base"]) or "falta" in str(row["Alerta_Datos"]).lower() or "incompleta" in str(row["Alerta_Datos"]).lower():
        return "Dato faltante"
    if is_harvest_ready(row):
        return "Disponible"
    return "Activa"


def _get_gsheet_client():
    try:
        creds = dict(st.secrets["gcp_service_account"])
    except Exception:
        st.error("Faltan credenciales en Streamlit Secrets: gcp_service_account")
        st.stop()

    if "private_key" in creds and isinstance(creds["private_key"], str):
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")

    return gspread.service_account_from_dict(creds)


def _read_sheet(workbook, sheet_name, empty_columns=None):
    try:
        ws = workbook.worksheet(sheet_name)
        rows = ws.get_all_records()
        return pd.DataFrame(rows)
    except gspread.WorksheetNotFound:
        return pd.DataFrame(columns=empty_columns or [])


@st.cache_data(ttl=300, show_spinner="Cargando datos desde Google Sheets...")
def load_data():
    client = _get_gsheet_client()
    workbook = client.open_by_key(SPREADSHEET_ID)
    sheet_names = [ws.title for ws in workbook.worksheets()]

    fincas = _read_sheet(workbook, "Fincas")
    unidades = _read_sheet(workbook, "Unidades")

    if "VistaCultivos" in sheet_names:
        df = _read_sheet(workbook, "VistaCultivos")
    else:
        cultivos = _read_sheet(workbook, "CatalogoCultivos")
        siembras = _read_sheet(workbook, "CultivosSembrados")
        df = siembras.merge(fincas, on="Finca_ID", how="left")
        df = df.merge(unidades, on=["Unidad_ID", "Finca_ID"], how="left")
        df = df.merge(cultivos, on="Cultivo_ID", how="left")

    arboles = _read_sheet(workbook, "Arboles") if "Arboles" in sheet_names else pd.DataFrame(TREE_DATA)

    eventos = _read_sheet(
        workbook,
        "EventosAgricolas",
        ["ID_Evento","Tipo_Evento","ID_Insumo","Nombre_Insumo","Target_Tipo","Target_ID",
         "Target_Label","Finca","Unidad","Cultivo","Arbol","Fecha_Programada",
         "Fecha_Realizada","Estado","Notas"]
    )

    insumos = _read_sheet(
        workbook,
        "Insumos",
        ["ID_Insumo","Nombre","Tipo","Disponible","Uso_Principal","Restricciones/Notas","Compra_Requerida"]
    )

    return clean_view(df), clean_units(unidades, fincas), clean_trees(arboles), clean_events(eventos), insumos


def clean_units(unidades, fincas):
    out = unidades.copy()
    if "Finca_Nombre" not in out.columns:
        out = out.merge(fincas[["Finca_ID", "Finca_Nombre"]], on="Finca_ID", how="left")
    out["Unidad"] = out.get("Unidad_Nombre", out.get("Unidad", ""))
    out["Finca"] = out.get("Finca_Nombre", out.get("Finca", ""))
    out["Estado_Unidad"] = out.get("Estado", "Activa")
    return out



def clean_trees(arboles):
    out = arboles.copy()
    if "Arbol_ID" not in out.columns:
        out["Arbol_ID"] = [f"ARB_{i:03d}" for i in range(len(out))]
    if "Arbol" not in out.columns and "Nombre" in out.columns:
        out["Arbol"] = out["Nombre"]
    for col in ["Finca", "Arbol", "Icono", "Estado_Fenologico", "Trasplante", "Estado_Sanitario", "Evento_Agricola"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("N/A" if col == "Trasplante" else "").astype(str)
    return out


def clean_events(eventos):
    out = eventos.copy()
    for col in ["Fecha_Programada", "Fecha_Realizada"]:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
        else:
            out[col] = pd.NaT
    for col in ["Tipo_Evento", "Nombre_Insumo", "Target_Tipo", "Target_ID", "Target_Label", "Finca", "Unidad", "Cultivo", "Arbol", "Estado", "Notas"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    return out


def event_effective_date(row):
    if pd.notna(row.get("Fecha_Programada")):
        return row.get("Fecha_Programada")
    return row.get("Fecha_Realizada")


def event_status_class(status, effective_date=None):
    s = str(status).strip().lower()
    if "complet" in s:
        return "event-completado"
    if effective_date is not None and pd.notna(effective_date) and pd.to_datetime(effective_date).date() < date.today() and "complet" not in s:
        return "event-vencido"
    if "pend" in s:
        return "event-pendiente"
    return "event-no-empezado"


def latest_control_status(events, target_id):
    if events is None or events.empty or not target_id:
        return None
    subset = events[(events["Target_ID"].astype(str) == str(target_id)) & (events["Tipo_Evento"].str.lower() == "control fitosanitario")].copy()
    if subset.empty:
        return None
    subset["_date"] = subset.apply(event_effective_date, axis=1)
    subset = subset.sort_values("_date", na_position="last")
    row = subset.iloc[-1]
    return {"estado": row.get("Estado", ""), "insumo": row.get("Nombre_Insumo", ""), "fecha": row.get("_date")}


def control_status_html(control):
    if not control:
        return '<div class="control-line">Control fitosanitario <span class="control-pill event-no-empezado">Sin evento</span></div>'
    cls = event_status_class(control.get("estado"), control.get("fecha"))
    insumo = control.get("insumo") or "Sin insumo"
    fecha = fmt_date(control.get("fecha")) if pd.notna(control.get("fecha")) else "Sin fecha"
    return f'<div class="control-line">Control fitosanitario <span class="control-pill {cls}">{control.get("estado", "")}</span> · {insumo} · {fecha}</div>'



def completed_events_for_target(events, target_id, year=None):
    if events is None or events.empty or not target_id:
        return pd.DataFrame()
    subset = events[events["Target_ID"].astype(str) == str(target_id)].copy()
    if subset.empty:
        return subset
    subset["_date"] = subset.apply(event_effective_date, axis=1)
    subset = subset[subset["_date"].notna()]
    subset = subset[subset["Estado"].astype(str).str.lower().str.contains("complet", na=False)]
    if year is not None:
        subset = subset[pd.to_datetime(subset["_date"]).dt.year == year]
    return subset


def history_summary_html(events, target_id):
    year = date.today().year
    subset = completed_events_for_target(events, target_id, year)
    if subset.empty:
        return '<div class="history-line">Historial año: <span class="history-pill">Sin eventos completados</span></div>'
    subset["_key"] = subset["Tipo_Evento"].fillna("") + ": " + subset["Nombre_Insumo"].fillna("Sin insumo")
    counts = subset.groupby("_key").size().sort_values(ascending=False)
    pills = "".join([f'<span class="history-pill">{k} x{v}</span>' for k, v in counts.items()])
    return f'<div class="history-line">Historial año: {pills}</div>'


def insumo_metadata(insumos, insumo_id=None, nombre=None):
    if insumos is None or insumos.empty:
        return {}
    df = insumos.copy()
    row = None
    if insumo_id and "ID_Insumo" in df.columns:
        m = df[df["ID_Insumo"].astype(str) == str(insumo_id)]
        if not m.empty:
            row = m.iloc[0]
    if row is None and nombre and "Nombre" in df.columns:
        m = df[df["Nombre"].astype(str).str.lower() == str(nombre).lower()]
        if not m.empty:
            row = m.iloc[0]
    if row is None:
        return {}
    return {k: row.get(k, "") for k in df.columns}


def next_soil_abono_html(events, insumos, target_id, estado_fenologico=""):
    if events is None or events.empty or not target_id:
        return '<div class="next-abono">Próximo abono: sin historial para calcular frecuencia.</div>'
    subset = completed_events_for_target(events, target_id)
    subset = subset[subset["Tipo_Evento"].astype(str).str.lower() == "abono tierra"] if not subset.empty else subset
    if subset.empty:
        return '<div class="next-abono">Próximo abono: sin abonada de tierra registrada.</div>'
    subset = subset.sort_values("_date")
    last = subset.iloc[-1]
    meta = insumo_metadata(insumos, last.get("ID_Insumo"), last.get("Nombre_Insumo"))
    freq = pd.to_numeric(meta.get("Frecuencia_Dias", None), errors="coerce")
    insumo = last.get("Nombre_Insumo") or meta.get("Nombre") or "Abono tierra"
    last_date = pd.to_datetime(last.get("_date")).date()
    cantidad = meta.get("Cantidad_Guia", "") or "Según criterio"
    momento = meta.get("Momento_Aplicacion", "") or "Según estado del árbol"
    if pd.isna(freq) or float(freq) <= 0:
        return f'<div class="next-abono">Último abono: {insumo} · {fmt_date(last_date)} · Cantidad: {cantidad}</div>'
    next_date = last_date + timedelta(days=int(freq))
    days = (next_date - date.today()).days
    cls = "next-abono overdue" if days <= 0 else "next-abono"
    timing = "vencido" if days < 0 else "hoy" if days == 0 else f"en {days} días"
    return f'<div class="{cls}">Próximo abono sugerido: {insumo} · {fmt_date(next_date)} ({timing})<br>Cantidad guía: {cantidad}<br>Momento: {momento}</div>'

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

    mask_disp = out.apply(is_available_placeholder, axis=1)
    out.loc[mask_disp, ["Fecha_Siembra", "Fecha_Trasplante", "Fecha_Base", "Cosecha_Min", "Cosecha_Max"]] = pd.NaT

    out["Cosecha_Disponible"] = out.apply(is_harvest_ready, axis=1)
    out["Mes_Cosecha"] = out["Cosecha_Min"].dt.strftime("%Y-%m").fillna("Sin fecha")
    out["Visual_Status"] = out.apply(visual_status, axis=1)
    return out


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


def days_html(value, prefix):
    if pd.isna(value):
        return f'<div class="info-line">{prefix}: Sin fecha</div>'
    days = (pd.to_datetime(value).date() - date.today()).days
    if days > 0:
        return f'<div class="info-line">{prefix}: en {days} días</div>'
    if days == 0:
        return f'<div class="info-line past-harvest"><b>{prefix}: hoy</b></div>'
    return f'<div class="info-line past-harvest"><b>{prefix}: hace {abs(days)} días</b></div>'


def display_state(row):
    if row.get("Visual_Status") == "Disponible":
        return "Disponible"
    return row["Estado_Actual"]


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


def html_block(markup):
    st.markdown(dedent(str(markup)).strip(), unsafe_allow_html=True)


def dashboard_metric_cards(cards):
    parts = ['<div class="dashboard-grid">']
    for label, value, note in cards:
        parts.append(f'<div class="dash-card"><div class="dash-label">{label}</div><div class="dash-value">{value}</div><div class="dash-note">{note}</div></div>')
    parts.append('</div>')
    html_block(''.join(parts))


def render_dashboard_view(filtered, filtered_units, events, trees):
    active_crops = filtered[(filtered["Cultivo"] != "Disponible") & (filtered["Estado_Unidad"] != "No activa")].copy()
    available_harvest = active_crops[active_crops["Cosecha_Disponible"]].copy()
    explicit_available = filtered[filtered["Cultivo"] == "Disponible"].copy()
    errors = int((filtered["Visual_Status"] == "Dato faltante").sum())

    next_harvest_value = "Sin fecha"
    next_harvest_note = "No hay cosechas disponibles"
    if not available_harvest.empty:
        item = available_harvest.sort_values("Cosecha_Min").iloc[0]
        next_harvest_value = fmt_date(item["Cosecha_Min"])
        next_harvest_note = f"{item['Cultivo']} · {item['Unidad']}"

    pending_events = pd.DataFrame()
    next_15_events = pd.DataFrame()
    overdue_events = pd.DataFrame()
    pending_controls = pd.DataFrame()
    if events is not None and not events.empty:
        pending_events = events[~events["Estado"].astype(str).str.lower().str.contains("complet", na=False)].copy()
        if not pending_events.empty:
            pending_events["_date"] = pending_events.apply(event_effective_date, axis=1)
            dated = pending_events[pending_events["_date"].notna()].copy()
            if not dated.empty:
                dated["_date"] = pd.to_datetime(dated["_date"]).dt.date
                today = date.today()
                next_15_events = dated[(dated["_date"] >= today) & (dated["_date"] <= today + timedelta(days=15))]
                overdue_events = dated[dated["_date"] < today]
            pending_controls = pending_events[pending_events["Tipo_Evento"].astype(str).str.lower() == "control fitosanitario"]

    active_trees = 0 if trees is None or trees.empty else len(trees)
    cards = [
        ("Cultivos", len(active_crops), "activos visibles"),
        ("Camas", filtered_units["Unidad"].nunique(), "según filtros"),
        ("Cosecha", next_harvest_value, next_harvest_note),
        ("Cosechas disp.", len(available_harvest), "mínima en el pasado"),
        ("Espacios", len(explicit_available), "disponibles"),
        ("Errores", errors, "datos faltantes"),
        ("Árboles", active_trees, "registrados"),
        ("Eventos 15d", len(next_15_events), "pendientes próximos"),
    ]
    dashboard_metric_cards(cards)

    c1, c2 = st.columns([1,1])
    with c1:
        html_block('''
        <div class="dash-panel">
            <div class="dash-panel-title">🌧️ Lluvias y clima</div>
            <div class="dash-line"><span class="dash-pill pill-blue">Moravia</span> Pendiente integrar lluvia real.</div>
            <div class="dash-line"><span class="dash-pill pill-blue">Frailes</span> Pendiente integrar lluvia real.</div>
            <div class="dash-line"><span class="dash-pill pill-yellow">Uso previsto</span> mover foliares, riego y controles según pronóstico.</div>
        </div>
        ''')
    with c2:
        lines = []
        if len(overdue_events) > 0:
            lines.append(f'<div class="dash-line"><span class="dash-pill pill-red">Vencidos</span> {len(overdue_events)} eventos sin completar.</div>')
        if len(next_15_events) > 0:
            sample = next_15_events.sort_values("_date").head(3)
            for _, r in sample.iterrows():
                lines.append(f'<div class="dash-line"><span class="dash-pill pill-yellow">{fmt_date(r["_date"])}</span> {r.get("Tipo_Evento", "Evento")} · {r.get("Target_Label", "")}</div>')
        if not lines:
            lines.append('<div class="dash-line"><span class="dash-pill pill-green">Sin alertas</span> No hay eventos próximos en 15 días.</div>')
        html_block(f'''
        <div class="dash-panel">
            <div class="dash-panel-title">⚠️ Eventos especiales</div>
            {''.join(lines)}
        </div>
        ''')

    html_block('<div class="dash-panel"><div class="dash-panel-title">📝 Notas rápidas</div><div class="dash-line">Captura temporal para ideas, observaciones o mensajes que luego GPT puede convertir en cambios de datos.</div></div>')
    note = st.text_area("Nueva nota", placeholder="Ejemplo: En Frailes vi hojas con manchas en pepino. Programar control fitosanitario con Mistral.", height=90, key="quick_note")
    if note.strip():
        st.download_button("Descargar nota", data=note.strip(), file_name=f"fincaos_nota_{date.today().isoformat()}.txt", mime="text/plain")


def crop_card(row, idx, events=None):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})

    control_html = control_status_html(latest_control_status(events, row.get("Siembra_ID")))

    if is_available_placeholder(row):
        st.markdown(
            f"""
            <div class="crop-card available-card">
                <div class="icon-circle {meta['class']}">{meta['icon']}</div>
                <div class="crop-name">Disponible</div>
                <div class="qty">Espacio disponible</div>
                <div class="info-line">Estado: <b>Disponible</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    card_class = "crop-card harvest-ready" if row.get("Cosecha_Disponible", False) else "crop-card"
    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="icon-circle {meta['class']}">{meta['icon']}</div>
            <div class="crop-name">{crop}</div>
            <div class="qty">{row['Cantidad']}</div>
            <div class="info-line">Estado: <b>{display_state(row)}</b></div>
            <div class="info-line">{base_date_label(row)}</div>
            {days_html(row['Cosecha_Min'], 'Cosecha min')}
            {days_html(row['Cosecha_Max'], 'Cosecha max')}
            {control_html}
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
    return "Activa"


def sort_crops_for_display(crops_df):
    if crops_df is None or crops_df.empty:
        return crops_df
    tmp = crops_df.copy()
    tmp["_available_sort"] = tmp.apply(lambda r: 1 if is_available_placeholder(r) else 0, axis=1)
    tmp["_ready_sort"] = tmp["Cosecha_Disponible"].apply(lambda x: 0 if bool(x) else 1)
    return tmp.sort_values(["_available_sort", "_ready_sort", "Cultivo"]).drop(columns=["_available_sort", "_ready_sort"])


def bed_panel(unit_row, crops_df, events=None):
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
        records = list(sort_crops_for_display(crops_df).iterrows())
        for start in range(0, len(records), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, (idx, row) in zip(cols, records[start:start + cols_per_row]):
                with col:
                    crop_card(row, idx, events)


def app_week_number(d):
    # Semana 1 empieza el 1 de enero y sigue cada 7 días: semana del 01 de enero = semana 1.
    return ((d - date(d.year, 1, 1)).days // 7) + 1


def week_range_for_number(year, week_number):
    start = date(year, 1, 1) + pd.Timedelta(days=(week_number - 1) * 7)
    end = start + pd.Timedelta(days=6)
    return start, end


def month_week_numbers(year, month):
    first = date(year, month, 1)
    last = date(year, month, calendar.monthrange(year, month)[1])
    start_week = app_week_number(first)
    end_week = app_week_number(last)
    return list(range(start_week, end_week + 1))


def event_status(row):
    if pd.isna(row["Cosecha_Min"]):
        return "Sin fecha", "future"
    min_date = pd.to_datetime(row["Cosecha_Min"]).date()
    max_date = pd.to_datetime(row["Cosecha_Max"]).date() if pd.notna(row["Cosecha_Max"]) else None
    days = (min_date - date.today()).days
    if max_date is not None and max_date < date.today():
        return "Cosecha máxima vencida", "overdue"
    if days <= 0:
        return "Cosecha disponible", "available"
    if days <= 15:
        return "Próxima cosecha", "soon"
    return "Cosecha futura", "future"


def calendar_event_card(row):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})
    status_label, status_class = event_status(row)
    date_class = "overdue-text" if status_class == "overdue" else "ready-text" if status_class == "available" else "soon-text" if status_class == "soon" else "future-text"
    st.markdown(
        f"""
        <div class="event-card {status_class}">
            <div class="event-row">
                <div class="event-icon">{meta['icon']}</div>
                <div>
                    <div class="event-crop">{crop}</div>
                    <div class="event-meta">{row['Finca']} · {row['Unidad']}</div>
                    <div class="event-date {date_class}">{status_label}: {fmt_date(row['Cosecha_Min'])}</div>
                    <div class="event-meta">Máx: {fmt_date(row['Cosecha_Max'])}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_calendar_view(all_df):
    today = date.today()
    month_options = []
    for offset in range(-6, 7):
        m = today.month + offset
        y = today.year
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        month_options.append((f"{MONTHS_ES[m]} {y}", y, m))

    labels = [x[0] for x in month_options]
    default_label = f"{MONTHS_ES[today.month]} {today.year}"

    c1, c2, c3, c4 = st.columns([1.15, 1.15, 1.35, 1.25])
    with c1:
        selected_label = st.selectbox("Mes", labels, index=labels.index(default_label) if default_label in labels else 0, key="cal_mes")
    _, selected_year, selected_month = next(x for x in month_options if x[0] == selected_label)

    calendar_base = all_df.copy()
    calendar_base = calendar_base[
        (calendar_base["Cultivo"] != "Disponible")
        & (calendar_base["Estado_Unidad"] != "No activa")
        & calendar_base["Cosecha_Min"].notna()
    ].copy()
    calendar_base["Cosecha_Date"] = calendar_base["Cosecha_Min"].dt.date

    with c2:
        fincas = ["Todas"] + [f for f in ["Moravia", "Frailes"] if f in set(calendar_base["Finca"].dropna().unique())]
        fincas += [f for f in sorted(calendar_base["Finca"].dropna().unique()) if f not in fincas]
        cal_finca = st.selectbox("Finca", fincas, key="cal_finca")
    if cal_finca != "Todas":
        calendar_base = calendar_base[calendar_base["Finca"] == cal_finca]

    with c3:
        camas = ["Todas"] + sorted(calendar_base["Unidad"].dropna().unique())
        cal_cama = st.selectbox("Cama", camas, key="cal_cama")
    if cal_cama != "Todas":
        calendar_base = calendar_base[calendar_base["Unidad"] == cal_cama]

    with c4:
        only_soon = st.checkbox("Solo próximos 15 días", value=False, key="cal_only_soon")

    calendar_df = calendar_base.copy()
    month_mask = calendar_df["Cosecha_Date"].apply(lambda d: d.year == selected_year and d.month == selected_month)
    if only_soon:
        soon_mask = (calendar_df["Cosecha_Date"] >= today) & (calendar_df["Cosecha_Date"] <= today + pd.Timedelta(days=15))
        calendar_df = calendar_df[month_mask & soon_mask]
    else:
        # Default: todos los cultivos activos ubicados por Cosecha_Min en el mes seleccionado.
        calendar_df = calendar_df[month_mask]

    if not calendar_df.empty:
        calendar_df["Week_Num"] = calendar_df["Cosecha_Date"].apply(app_week_number)
        week_nums = sorted(calendar_df["Week_Num"].unique().tolist())
    else:
        week_nums = []

    def build_event_html(row):
        crop = row["Cultivo"]
        meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})
        status_label, status_class = event_status(row)
        date_class = "overdue-text" if status_class == "overdue" else "ready-text" if status_class == "available" else "soon-text" if status_class == "soon" else "future-text"
        return (
            f'<div class="event-card {status_class}">'
            f'<div class="event-row">'
            f'<div class="event-icon">{meta["icon"]}</div>'
            f'<div>'
            f'<div class="event-crop">{crop}</div>'
            f'<div class="event-meta">{row["Finca"]} · {row["Unidad"]}</div>'
            f'<div class="event-date {date_class}">{status_label}: {fmt_date(row["Cosecha_Min"])}</div>'
            f'<div class="event-meta">Máx: {fmt_date(row["Cosecha_Max"])}</div>'
            f'</div></div></div>'
        )


    for start in range(0, len(week_nums), 4):
        cols = st.columns(4)
        for col, week_num in zip(cols, week_nums[start:start + 4]):
            with col:
                week_start, week_end = week_range_for_number(selected_year, int(week_num))
                events = calendar_df[calendar_df["Week_Num"] == week_num].sort_values(["Cosecha_Min", "Finca", "Unidad", "Cultivo"])
                events_html = "".join(build_event_html(row) for _, row in events.iterrows())
                if not events_html:
                    events_html = '<div class="no-events">Sin cosechas</div>'
                html_block(
                    f'<div class="week-card"><div class="week-title">Semana {int(week_num)}</div>'
                    f'<div class="week-range">{week_start.strftime("%d %b")} – {week_end.strftime("%d %b")}</div>'
                    f'{events_html}</div>'
                )

    if len(week_nums) == 0:
        msg = "No hay cosechas próximas en los próximos 15 días para los filtros seleccionados." if only_soon else "No hay cultivos con cosecha mínima en el mes seleccionado."
        html_block(f'<div class="calendar-toolbar"><div class="calendar-note">{msg}</div></div>')


TREE_DATA = [
    {"Finca":"Moravia", "Arbol":"Manzano tico", "Icono":"🍎", "Estado_Fenologico":"Llenado", "Trasplante":"N/A", "Estado_Sanitario":"Bueno"},
    {"Finca":"Moravia", "Arbol":"Guayabita del Perú", "Icono":"🌳", "Estado_Fenologico":"Vegetativo", "Trasplante":"N/A", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Guayaba", "Icono":"🌳", "Estado_Fenologico":"Floración", "Trasplante":"N/A", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Guanábana", "Icono":"🌳", "Estado_Fenologico":"Fructificación", "Trasplante":"N/A", "Estado_Sanitario":"Atención"},
    {"Finca":"Frailes", "Arbol":"Naranja Washington", "Icono":"🍊", "Estado_Fenologico":"Vegetativo", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Naranja Valencia", "Icono":"🍊", "Estado_Fenologico":"Vegetativo", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Limón mandarina", "Icono":"🍋", "Estado_Fenologico":"Vegetativo", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Limón mesino", "Icono":"🍋", "Estado_Fenologico":"Vegetativo", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Limón dulce", "Icono":"🍋", "Estado_Fenologico":"Vegetativo", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Mandarina", "Icono":"🍊", "Estado_Fenologico":"Brotes", "Trasplante":"Jul 2025", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Anona", "Icono":"🌳", "Estado_Fenologico":"Recuperación", "Trasplante":"N/A", "Estado_Sanitario":"Estrés"},
    {"Finca":"Frailes", "Arbol":"Níspero", "Icono":"🌳", "Estado_Fenologico":"Establecimiento", "Trasplante":"Reciente", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Durazno", "Icono":"🌸", "Estado_Fenologico":"Vegetativo", "Trasplante":"N/A", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Mango peludo", "Icono":"🥭", "Estado_Fenologico":"Vegetativo", "Trasplante":"N/A", "Estado_Sanitario":"Bueno"},
    {"Finca":"Frailes", "Arbol":"Mamón chino", "Icono":"🌳", "Estado_Fenologico":"Recuperación", "Trasplante":"N/A", "Estado_Sanitario":"Atención"},
]

def phen_class(value):
    v = str(value).lower()
    if "flora" in v:
        return "phen-floracion"
    if "fruct" in v:
        return "phen-fructificacion"
    if "llen" in v:
        return "phen-llenado"
    if "recup" in v or "estable" in v or "brote" in v:
        return "phen-recuperacion"
    return "phen-vegetativo"

def health_class(value):
    v = str(value).lower()
    if "estr" in v:
        return "health-estres"
    if "aten" in v:
        return "health-atencion"
    return "health-bueno"

def render_tree_card(row, events=None, insumos=None):
    control_html = control_status_html(latest_control_status(events, row.get("Arbol_ID")))
    history_html = history_summary_html(events, row.get("Arbol_ID"))
    next_abono_html = next_soil_abono_html(events, insumos, row.get("Arbol_ID"), row.get("Estado_Fenologico", ""))
    st.markdown(f"""
    <div class="tree-card">
        <div class="tree-row">
            <div class="tree-icon">{row['Icono']}</div>
            <div style="width:100%;">
                <div class="tree-name">{row['Arbol']}</div>
                <div class="tree-line">Estado fenológico <span class="tree-pill {phen_class(row['Estado_Fenologico'])}">{row['Estado_Fenologico']}</span></div>
                <div class="tree-line">Trasplante <b>{row['Trasplante']}</b></div>
                <div class="tree-line">Estado sanitario <span class="tree-pill {health_class(row['Estado_Sanitario'])}">● {row['Estado_Sanitario']}</span></div>
                {control_html}
                {history_html}
                {next_abono_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_arboles_view(trees, events, insumos):
    c1, c2 = st.columns([1,1])
    with c1:
        finca_sel = st.selectbox("Finca", ["Todas"] + [f for f in ["Moravia","Frailes"] if f in trees["Finca"].unique()], key="tree_finca")
    with c2:
        health_sel = st.selectbox("Estado sanitario", ["Todos"] + sorted(trees["Estado_Sanitario"].unique()), key="tree_health")
    if finca_sel != "Todas":
        trees = trees[trees["Finca"] == finca_sel]
    if health_sel != "Todos":
        trees = trees[trees["Estado_Sanitario"] == health_sel]
    for finca, group in trees.groupby("Finca", sort=False):
        st.markdown(f'<div class="section-title">📍 {finca}</div>', unsafe_allow_html=True)
        records = list(group.iterrows())
        for start in range(0, len(records), 4):
            cols = st.columns(4)
            for col, (_, row) in zip(cols, records[start:start+4]):
                with col:
                    render_tree_card(row, events, insumos)


def render_eventos_view(events, insumos):
    c1, c2, c3 = st.columns([1.1, 1.1, 1.1])
    with c1:
        tipo_options = ["Todos"] + sorted([x for x in events["Tipo_Evento"].dropna().unique() if x])
        tipo_sel = st.selectbox("Tipo de evento", tipo_options, key="evt_tipo")
    with c2:
        finca_options = ["Todas"] + sorted([x for x in events["Finca"].dropna().unique() if x])
        finca_sel = st.selectbox("Finca", finca_options, key="evt_finca")
    with c3:
        estado_options = ["Todos"] + sorted([x for x in events["Estado"].dropna().unique() if x])
        estado_sel = st.selectbox("Estado", estado_options, key="evt_estado")

    filtered_events = events.copy()
    if tipo_sel != "Todos":
        filtered_events = filtered_events[filtered_events["Tipo_Evento"] == tipo_sel]
    if finca_sel != "Todas":
        filtered_events = filtered_events[filtered_events["Finca"] == finca_sel]
    if estado_sel != "Todos":
        filtered_events = filtered_events[filtered_events["Estado"] == estado_sel]

    if filtered_events.empty:
        st.markdown('<div class="calendar-toolbar"><div class="calendar-note">No hay eventos agrícolas para los filtros seleccionados.</div></div>', unsafe_allow_html=True)
    else:
        for tipo, group in filtered_events.groupby("Tipo_Evento", sort=False):
            st.markdown(f'<div class="event-section-title">{tipo}</div>', unsafe_allow_html=True)
            group = group.copy()
            group["_date"] = group.apply(event_effective_date, axis=1)
            group = group.sort_values(["_date", "Finca", "Target_Label"], na_position="last")
            records = list(group.iterrows())
            for start in range(0, len(records), 3):
                cols = st.columns(3)
                for col, (_, row) in zip(cols, records[start:start+3]):
                    with col:
                        effective = row.get("_date")
                        cls = event_status_class(row.get("Estado"), effective)
                        fecha_txt = fmt_date(effective) if pd.notna(effective) else "Sin fecha"
                        insumo = row.get("Nombre_Insumo") or "Sin insumo"
                        target = row.get("Target_Label") or row.get("Target_ID")
                        html = f"""
                        <div class="ag-event-card">
                            <div class="ag-event-top">
                                <div>
                                    <div class="ag-event-title">{target}</div>
                                    <div class="ag-event-meta">{row.get("Finca", "")} · {row.get("Target_Tipo", "")}</div>
                                </div>
                                <span class="ag-event-pill {cls}">{row.get("Estado", "")}</span>
                            </div>
                            <div class="ag-event-meta"><b>Insumo:</b> {insumo}</div>
                            <div class="ag-event-meta"><b>Fecha:</b> {fecha_txt}</div>
                            <div class="ag-event-meta">{row.get("Notas", "")}</div>
                        </div>
                        """
                        st.markdown(html, unsafe_allow_html=True)

    with st.expander("Catálogo de insumos"):
        if insumos is None or insumos.empty:
            st.write("Sin insumos registrados.")
        else:
            for tipo, group in insumos.groupby("Tipo", sort=False):
                st.markdown(f"**{tipo}**")
                records = list(group.iterrows())
                for start in range(0, len(records), 3):
                    cols = st.columns(3)
                    for col, (_, row) in zip(cols, records[start:start+3]):
                        with col:
                            compra = "Compra requerida" if str(row.get("Compra_Requerida", "")).lower().startswith("s") else "Disponible"
                            html = f"""
                            <div class="insumo-card">
                                <div class="insumo-name">{row.get("Nombre", "")}</div>
                                <div class="insumo-meta">{row.get("Uso_Principal", "")}</div>
                                <div class="insumo-meta"><b>Cantidad guía:</b> {row.get("Cantidad_Guia", "Según criterio")}</div>
                                <div class="insumo-meta"><b>Momento:</b> {row.get("Momento_Aplicacion", "Según estado")}</div>
                                <div class="insumo-meta"><b>Frecuencia:</b> {row.get("Frecuencia_Dias", "") if str(row.get("Frecuencia_Dias", "")).strip() else "Sin regla"} días</div>
                                <div class="insumo-meta"><b>{compra}</b></div>
                            </div>
                            """
                            st.markdown(html, unsafe_allow_html=True)



def render_account_view():
    st.markdown("""
    <div style="background:#0f2f24;border:1px solid rgba(255,255,255,.18);border-radius:18px;padding:18px 20px;margin-bottom:16px;color:#fff;">
      <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
        <div style="background:#ffffff;border-radius:14px;padding:10px;min-width:120px;text-align:center;">
    """, unsafe_allow_html=True)
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=150)
    else:
        st.markdown('<div style="color:#0f2f24;font-size:24px;font-weight:800;">Hydra Q</div>', unsafe_allow_html=True)
    st.markdown("""
        </div>
        <div>
          <div style="font-size:26px;font-weight:800;line-height:1.1;">Cuenta</div>
          <div style="opacity:.88;font-size:14px;margin-top:4px;">Perfil y configuración general de FincaOS</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.15, 1])
    with c1:
        st.markdown("""
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;margin-bottom:14px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">Usuario</div>
          <div style="font-size:15px;color:#1f2937;"><b>Nombre:</b> Pablo Castro</div>
          <div style="font-size:15px;color:#1f2937;"><b>Correo:</b> no configurado</div>
        </div>
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">Permisos de acceso</div>
          <div style="font-size:14px;color:#374151;">Módulo reservado para administrar accesos. No desarrollado en esta versión.</div>
          <div style="display:inline-block;margin-top:10px;padding:6px 10px;border-radius:999px;background:#e5e7eb;color:#374151;font-size:12px;font-weight:700;">Trabajo futuro</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;margin-bottom:14px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">Versión</div>
          <div style="font-size:15px;color:#1f2937;"><b>Developer Version:</b> 20.1</div>
          <div style="font-size:15px;color:#1f2937;"><b>Fecha:</b> 2026-06-08</div>
          <div style="font-size:15px;color:#1f2937;"><b>Desarrollado con:</b> ChatGPT, MS Excel / Google Sheets, GitHub y Streamlit</div>
        </div>
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">🔌 PlugIns</div>
          <div style="font-size:14px;color:#374151;">Espacio reservado para integraciones futuras: clima, lluvia, GPT Actions y Google Sheets.</div>
        </div>
        """, unsafe_allow_html=True)

df, units, trees, eventos, insumos = load_data()

st.markdown('<div class="app-title">Finca OS Dev</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtros")
    st.caption(f"Datos: {DATA_FILE}")
    finca_options = [f for f in ["Moravia", "Frailes"] if f in set(units["Finca"].dropna().unique())] + [f for f in sorted(units["Finca"].dropna().unique()) if f not in ["Moravia", "Frailes"]]
    finca_filter = st.multiselect("Finca", finca_options, default=finca_options)
    unidad_options = sorted(units[units["Finca"].isin(finca_filter)]["Unidad"].dropna().unique()) if finca_filter else sorted(units["Unidad"].dropna().unique())
    unidad_filter = st.multiselect("Cama", unidad_options)
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

tab_dashboard, tab_camas, tab_arboles, tab_eventos, tab_calendario, tab_cuenta = st.tabs(["📊 Dashboard", "🛏️ Camas", "🌳 Árboles", "🧪 Eventos", "📅 Calendario", "👤 Cuenta"])

with tab_dashboard:
    render_dashboard_view(filtered, filtered_units, eventos, trees)

with tab_camas:
    for finca, unit_group in filtered_units.groupby("Finca", sort=False):
        st.markdown(f'<div class="section-title">📍 {finca}</div>', unsafe_allow_html=True)
        unit_records = list(unit_group.sort_values("Unidad").iterrows())
        for start in range(0, len(unit_records), 2):
            cols = st.columns(2)
            for col, (_, unit_row) in zip(cols, unit_records[start:start + 2]):
                with col:
                    crops = filtered[filtered["Unidad"] == unit_row["Unidad"]]
                    bed_panel(unit_row, crops, eventos)

with tab_arboles:
    render_arboles_view(trees, eventos, insumos)

with tab_eventos:
    render_eventos_view(eventos, insumos)

with tab_calendario:
    render_calendar_view(df)

with tab_cuenta:
    render_account_view()

if show_detail_table:
    st.divider()
    st.subheader("Detalle de datos")
    show_cols = [
        "Finca", "Unidad", "Cultivo", "Cantidad", "Estado_Actual",
        "Fecha_Siembra", "Fecha_Trasplante", "Cosecha_Min", "Cosecha_Max", "Visual_Status"
    ]
    table = filtered[show_cols].copy().sort_values(["Finca", "Unidad", "Cultivo"])
    st.dataframe(table, use_container_width=True, hide_index=True)
