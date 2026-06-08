from pathlib import Path
from datetime import date, timedelta
import calendar

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finca OS Dev", layout="wide", page_icon="🌱")

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "FincaOS_Data.xlsx"
TODAY = date.today()

CROP_META = {
    "Disponible": {"icon": "⬚", "class": "available"},
    "Lechuga": {"icon": "🥬", "class": "leafy"},
    "Acelga": {"icon": "☘️", "class": "chard"},
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
    "Arúgula": {"icon": "🥗", "class": "arugula"},
    "Zucchini": {"icon": "🥒", "class": "zucchini"},
    "Zuchinni": {"icon": "🥒", "class": "zucchini"},
    "Zanahoria": {"icon": "🥕", "class": "carrot"},
    "Cebollino": {"icon": "🌾", "class": "chives"},
    "Apio": {"icon": "🥬", "class": "celery"},
    "Espinaca": {"icon": "🍀", "class": "spinach"},
    "Perejil italiano": {"icon": "🌿", "class": "parsley"},
    "Perejil normal": {"icon": "🌿", "class": "parsley"},
}

EVENT_ICON = {
    "Control fitosanitario": "🛡️",
    "Abono tierra": "🌱",
    "Abono foliar": "💧",
    "Poda": "✂️",
}

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f3d25 0px, #0f3d25 230px, #f4f7f2 230px, #f4f7f2 100%);
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);} 
.main-title {
    font-size: 42px;
    line-height: 1.05;
    font-weight: 900;
    color: white;
    margin: 18px 0 12px 0;
    letter-spacing: -0.5px;
}
.filter-panel {
    background:#0b2f1d;
    border:1px solid rgba(255,255,255,.18);
    border-radius:18px;
    padding: 14px 16px;
    margin-bottom: 18px;
    color:white;
    box-shadow: 0 3px 14px rgba(0,0,0,.18);
}
.filter-title {font-size:14px; color:#d9fbe0; font-weight:800; margin-bottom:4px;}
.section-title {
    font-size: 26px;
    font-weight: 900;
    color: white;
    background: #14532d;
    border-radius: 16px;
    padding: 10px 16px;
    margin: 18px 0 14px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.12);
}
.bed-box, .tree-box, .week-box, .event-box {
    border: 2px solid #0b2f1d;
    background: #ffffff;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(15, 61, 37, 0.15);
}
.bed-title, .tree-title {
    font-size: 20px;
    font-weight: 900;
    color: white;
    background:#14532d;
    border-radius:12px;
    padding:8px 12px;
    margin-bottom:10px;
}
.crop-card {
    border: 1px solid #dbe7d6;
    background: #ffffff;
    border-radius: 16px;
    padding: 12px 10px;
    margin-bottom: 10px;
    min-height: 168px;
    box-shadow: 0 2px 8px rgba(15, 61, 37, 0.08);
}
.crop-card.available-card {background:#e8f5e9; border:2px solid #74a86b;}
.crop-card.overdue-card {background:#fef2f2; border:2px solid #dc2626;}
.icon-circle {
    width: 56px; height: 56px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 29px; margin-bottom: 8px;
}
.available {background:#e8f5e9;}
.leafy {background:#dcfce7;} .chard {background:#d9f99d;} .cucumber {background:#bbf7d0;} .watermelon {background:#fee2e2;}
.squash {background:#ffedd5;} .basil {background:#ccfbf1;} .tomato-cherry {background:#fecaca;} .tomato {background:#fee2e2;}
.cilantro {background:#d1fae5;} .onion-white {background:#f3f4f6;} .onion-purple {background:#ede9fe;} .pepper {background:#dcfce7;}
.arugula {background:#ecfccb;} .zucchini {background:#ccfbf1;} .carrot {background:#fed7aa;} .chives {background:#ecfccb;}
.celery {background:#e0f2fe;} .spinach {background:#dcfce7;} .parsley {background:#d1fae5;}
.crop-name {font-weight: 900; color:#123d24; font-size: 15px; margin-bottom:2px;}
.qty {font-size: 18px; font-weight: 900; color:#111827;}
.info-line {font-size: 13px; color:#475569; margin-top: 2px;}
.red-bold {font-weight:900; color:#b91c1c;}
.badge {display:inline-block; padding:4px 9px; border-radius:999px; font-size:12px; font-weight:900; margin: 2px 4px 2px 0;}
.ok {background:#dcfce7; color:#166534;} .warn {background:#fef3c7; color:#92400e;} .bad {background:#fee2e2; color:#991b1b;} .neutral {background:#e5e7eb; color:#374151;}
.blue {background:#dbeafe; color:#1e40af;} .purple {background:#ede9fe; color:#5b21b6;}
.control-pill {font-size:12px; padding:5px 8px; border-radius:10px; margin-top:6px; display:inline-block; font-weight:800;}
.tree-icon {font-size:36px; margin-right:8px;}
.tree-name {font-size:18px; font-weight:900; color:#123d24;}
.history-box {background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:9px; margin-top:8px; font-size:13px;}
.week-title {font-size:17px; font-weight:900; color:#123d24; margin-bottom:8px;}
.cal-item {border-radius:12px; padding:8px 9px; margin-bottom:7px; font-size:13px; border:1px solid #e5e7eb; background:#ffffff;}
.cal-overdue {background:#fee2e2; border:2px solid #dc2626;}
.cal-event {background:#eff6ff; border:1px solid #bfdbfe;}
.event-type-title {font-size:20px; font-weight:900; color:#123d24; margin-bottom:10px;}
.event-row {padding:9px; border-radius:12px; border:1px solid #e5e7eb; margin-bottom:8px; background:#fafafa;}
.metric-card {background:white; border-radius:16px; padding:14px; box-shadow:0 2px 10px rgba(0,0,0,.10); border:1px solid #dbe7d6;}
.metric-value {font-size:26px; font-weight:900; color:#123d24;}
.metric-label {font-size:12px; color:#4b5563; font-weight:800; text-transform:uppercase;}
</style>
""",
    unsafe_allow_html=True,
)


def first_existing(df, candidates, fallback=None):
    for c in candidates:
        if c in df.columns:
            return c
    return fallback


def safe_str(v):
    if pd.isna(v):
        return ""
    return str(v)


def fmt_date(v):
    if pd.isna(v) or v is None or safe_str(v).strip() == "":
        return "Sin fecha"
    return pd.to_datetime(v).strftime("%d %b %Y")


def to_date(v):
    if pd.isna(v) or v is None or safe_str(v).strip() == "":
        return pd.NaT
    return pd.to_datetime(v, errors="coerce")


def days_from_today(v):
    if pd.isna(v):
        return None
    return (pd.to_datetime(v).date() - TODAY).days


def base_date_label(row):
    if pd.notna(row.get("Fecha_Trasplante")):
        return f"Trasplante: {fmt_date(row.get('Fecha_Trasplante'))}"
    if pd.notna(row.get("Fecha_Siembra")):
        return f"Siembra: {fmt_date(row.get('Fecha_Siembra'))}"
    return "Sin fecha base"


def normalize_status(status):
    s = safe_str(status).strip().lower()
    if s in ["completado", "completada"]:
        return "Completado"
    if s in ["pendiente"]:
        return "Pendiente"
    if s in ["no empezado", "no iniciado"]:
        return "No empezado"
    return safe_str(status) or "Sin estado"


@st.cache_data
def load_data():
    xl = pd.ExcelFile(FILE_PATH)
    fincas = pd.read_excel(FILE_PATH, sheet_name="Fincas") if "Fincas" in xl.sheet_names else pd.DataFrame()
    camas = pd.read_excel(FILE_PATH, sheet_name="Camas") if "Camas" in xl.sheet_names else pd.read_excel(FILE_PATH, sheet_name="Unidades")
    vista = pd.read_excel(FILE_PATH, sheet_name="VistaCultivos") if "VistaCultivos" in xl.sheet_names else pd.DataFrame()
    arboles = pd.read_excel(FILE_PATH, sheet_name="Arboles") if "Arboles" in xl.sheet_names else pd.DataFrame()
    eventos = pd.read_excel(FILE_PATH, sheet_name="EventosAgricolas") if "EventosAgricolas" in xl.sheet_names else pd.DataFrame()
    insumos = pd.read_excel(FILE_PATH, sheet_name="Insumos") if "Insumos" in xl.sheet_names else pd.DataFrame()
    return clean_vista(vista), clean_camas(camas, fincas), clean_arboles(arboles), clean_eventos(eventos), clean_insumos(insumos)


def clean_vista(df):
    out = df.copy()
    if out.empty:
        return out
    for col in ["Fecha_Siembra", "Fecha_Trasplante", "Fecha_Base", "Cosecha_Min", "Cosecha_Max"]:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
        else:
            out[col] = pd.NaT
    for col in ["Finca", "Unidad", "Cultivo", "Estado_Actual", "Estado_Unidad"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    if "Cantidad" in out.columns:
        out["Cantidad"] = pd.to_numeric(out["Cantidad"], errors="coerce").fillna(0).astype(int)
    else:
        out["Cantidad"] = 0
    out["Es_Disponible"] = out["Cultivo"].str.lower().str.contains("disponible", na=False)
    out["Cosecha_Min_Dias"] = out["Cosecha_Min"].apply(days_from_today)
    out["Cosecha_Max_Dias"] = out["Cosecha_Max"].apply(days_from_today)
    out["Cosecha_Max_Vencida"] = out["Cosecha_Max_Dias"].apply(lambda x: x is not None and x < 0)
    out["Cosecha_Disponible"] = out["Cosecha_Min_Dias"].apply(lambda x: x is not None and x <= 0)
    return out


def clean_camas(camas, fincas):
    out = camas.copy()
    if "Finca_Nombre" not in out.columns and not fincas.empty:
        out = out.merge(fincas[["Finca_ID", "Finca_Nombre"]], on="Finca_ID", how="left")
    out["Finca"] = out.get("Finca_Nombre", out.get("Finca", "")).fillna("").astype(str)
    out["Unidad"] = out.get("Unidad_Nombre", out.get("Unidad", "")).fillna("").astype(str)
    return out


def clean_arboles(df):
    out = df.copy()
    if out.empty:
        return out
    if "Fecha_Trasplante" in out.columns:
        out["Fecha_Trasplante"] = pd.to_datetime(out["Fecha_Trasplante"], errors="coerce")
    else:
        out["Fecha_Trasplante"] = pd.NaT
    for col in ["Finca_Nombre", "Arbol_Nombre", "Especie", "Icono", "Estado_Fenologico", "Estado_Sanitario"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    return out


def clean_eventos(df):
    out = df.copy()
    if out.empty:
        return out
    for col in ["Fecha_Programada", "Fecha_Realizada", "Proxima_Fecha_Calculada"]:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
        else:
            out[col] = pd.NaT
    for col in ["Tipo_Evento", "Objeto_Tipo", "Estado", "Insumo_Nombre", "Cultivo_Nombre", "Arbol_Nombre", "Siembra_ID", "Arbol_ID", "Cama_ID", "Momento_Aplicacion"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    out["Estado"] = out["Estado"].apply(normalize_status)
    out["Fecha_Efectiva"] = out["Fecha_Realizada"].combine_first(out["Fecha_Programada"])
    out["Es_Completado"] = out["Estado"].eq("Completado")
    out["Es_Pendiente"] = ~out["Estado"].eq("Completado")
    return out


def clean_insumos(df):
    out = df.copy()
    if out.empty:
        return out
    for col in ["Nombre", "Tipo", "Disponible", "Uso_Principal", "Restricciones/Notas", "Compra_Requerida", "Cantidad_Guia", "Unidad_Medida", "Momento_Aplicacion"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    if "Frecuencia_Dias" in out.columns:
        out["Frecuencia_Dias"] = pd.to_numeric(out["Frecuencia_Dias"], errors="coerce")
    return out


def latest_event_for(events, tipo, siembra_id=None, arbol_id=None, completed=None):
    if events.empty:
        return None
    subset = events[events["Tipo_Evento"].eq(tipo)].copy()
    if siembra_id:
        subset = subset[subset["Siembra_ID"].eq(siembra_id)]
    if arbol_id:
        subset = subset[subset["Arbol_ID"].eq(arbol_id)]
    if completed is True:
        subset = subset[subset["Estado"].eq("Completado")]
    elif completed is False:
        subset = subset[~subset["Estado"].eq("Completado")]
    subset = subset.dropna(subset=["Fecha_Efectiva"])
    if subset.empty:
        return None
    return subset.sort_values("Fecha_Efectiva", ascending=False).iloc[0]


def next_event_for(events, siembra_id=None, arbol_id=None):
    if events.empty:
        return None
    subset = events[~events["Estado"].eq("Completado")].copy()
    if siembra_id:
        subset = subset[subset["Siembra_ID"].eq(siembra_id)]
    if arbol_id:
        subset = subset[subset["Arbol_ID"].eq(arbol_id)]
    subset = subset.dropna(subset=["Fecha_Programada"])
    if subset.empty:
        return None
    return subset.sort_values("Fecha_Programada").iloc[0]


def status_badge(status):
    s = normalize_status(status)
    cls = "ok" if s == "Completado" else "warn" if s == "Pendiente" else "neutral"
    return f"<span class='badge {cls}'>{s}</span>"


def control_indicator(events, siembra_id=None, arbol_id=None):
    pending = latest_event_for(events, "Control fitosanitario", siembra_id, arbol_id, completed=False)
    if pending is not None:
        return f"<span class='control-pill warn'>🛡️ Control: {pending['Estado']} · {pending.get('Insumo_Nombre','')} · {fmt_date(pending.get('Fecha_Programada'))}</span>"
    completed = latest_event_for(events, "Control fitosanitario", siembra_id, arbol_id, completed=True)
    if completed is not None:
        return f"<span class='control-pill ok'>🛡️ Último control: {completed.get('Insumo_Nombre','')} · {fmt_date(completed.get('Fecha_Realizada'))}</span>"
    return "<span class='control-pill neutral'>🛡️ Control: sin registro</span>"


def history_summary(events, arbol_id=None, siembra_id=None):
    if events.empty:
        return "Sin historial"
    subset = events[events["Estado"].eq("Completado")].copy()
    if arbol_id:
        subset = subset[subset["Arbol_ID"].eq(arbol_id)]
    if siembra_id:
        subset = subset[subset["Siembra_ID"].eq(siembra_id)]
    subset = subset.dropna(subset=["Fecha_Realizada"])
    subset = subset[subset["Fecha_Realizada"].dt.year.eq(TODAY.year)]
    if subset.empty:
        return "Sin eventos completados este año"
    g = subset.groupby(["Tipo_Evento", "Insumo_Nombre"]).size().reset_index(name="n")
    parts = []
    for _, r in g.iterrows():
        ins = r["Insumo_Nombre"] if r["Insumo_Nombre"] else "Sin insumo"
        parts.append(f"{r['Tipo_Evento']}: {ins} x{int(r['n'])}")
    return " · ".join(parts[:5])


def crop_card(row, events):
    crop = row.get("Cultivo", "")
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "leafy"})
    is_available = bool(row.get("Es_Disponible"))
    max_overdue = bool(row.get("Cosecha_Max_Vencida"))
    card_class = "available-card" if is_available or max_overdue else ""
    if max_overdue:
        card_class = "overdue-card"
    state = "Disponible" if is_available or max_overdue else row.get("Estado_Actual", "")
    if is_available:
        harvest_min = ""
        harvest_max = ""
        date_line = "Espacio disponible"
        control = ""
    else:
        min_days = row.get("Cosecha_Min_Dias")
        max_days = row.get("Cosecha_Max_Dias")
        min_txt = "Sin fecha" if min_days is None or pd.isna(min_days) else (f"hace {abs(int(min_days))} días" if min_days < 0 else f"en {int(min_days)} días")
        max_txt = "Sin fecha" if max_days is None or pd.isna(max_days) else (f"hace {abs(int(max_days))} días" if max_days < 0 else f"en {int(max_days)} días")
        min_cls = "red-bold" if min_days is not None and pd.notna(min_days) and min_days < 0 else ""
        max_cls = "red-bold" if max_days is not None and pd.notna(max_days) and max_days < 0 else ""
        harvest_min = f"<div class='info-line {min_cls}'>Cosecha mín: {min_txt}</div>"
        harvest_max = f"<div class='info-line {max_cls}'>Cosecha máx: {max_txt}</div>"
        date_line = base_date_label(row)
        control = control_indicator(events, siembra_id=safe_str(row.get("Siembra_ID")))
    html = f"""
    <div class='crop-card {card_class}'>
      <div class='icon-circle {meta['class']}'>{meta['icon']}</div>
      <div class='crop-name'>{crop}</div>
      <div class='qty'>{int(row.get('Cantidad',0))}</div>
      <div class='info-line'>Estado: <b>{state}</b></div>
      <div class='info-line'>{date_line}</div>
      {harvest_min}{harvest_max}{control}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metrics(df):
    active = df[~df["Es_Disponible"]]
    espacios = int(df["Es_Disponible"].sum())
    errores = int(df[["Fecha_Base", "Cultivo"]].isna().any(axis=1).sum()) if "Fecha_Base" in df.columns else 0
    disponibles = int(active["Cosecha_Min_Dias"].apply(lambda x: x is not None and pd.notna(x) and x <= 0).sum())
    prox = active.dropna(subset=["Cosecha_Min"])
    prox = prox[prox["Cosecha_Min"].dt.date >= TODAY].sort_values("Cosecha_Min")
    prox_txt = "Sin fecha"
    if not prox.empty:
        r = prox.iloc[0]
        prox_txt = f"{fmt_date(r['Cosecha_Min'])} · {r['Cultivo']}"
    metrics = [
        ("Cultivos activos", len(active)),
        ("Cosecha Disponible", prox_txt),
        ("Cosechas disponibles", disponibles),
        ("Espacios disponibles", espacios),
        ("Errores datos", errores),
    ]
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics):
        col.markdown(f"<div class='metric-card'><div class='metric-value'>{value}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)


def camas_view(df, camas, events):
    render_metrics(df)
    st.markdown("<div class='filter-panel'><div class='filter-title'>Filtros</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    fincas = ["Todas"] + sorted([x for x in df["Finca"].dropna().unique().tolist() if x])
    f_finca = c1.selectbox("Finca", fincas, key="camas_finca")
    base = df if f_finca == "Todas" else df[df["Finca"].eq(f_finca)]
    unidades = ["Todas"] + sorted([x for x in base["Unidad"].dropna().unique().tolist() if x])
    f_unidad = c2.selectbox("Cama", unidades, key="camas_unidad")
    st.markdown("</div>", unsafe_allow_html=True)
    view = base if f_unidad == "Todas" else base[base["Unidad"].eq(f_unidad)]
    for finca in sorted(view["Finca"].dropna().unique()):
        st.markdown(f"<div class='section-title'>🛏️ {finca}</div>", unsafe_allow_html=True)
        finca_df = view[view["Finca"].eq(finca)]
        for unidad in sorted(finca_df["Unidad"].dropna().unique()):
            st.markdown("<div class='bed-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='bed-title'>{unidad}</div>", unsafe_allow_html=True)
            bed = finca_df[finca_df["Unidad"].eq(unidad)].copy()
            bed["sort_available"] = bed["Es_Disponible"].astype(int)
            bed = bed.sort_values(["sort_available", "Cultivo"])
            cols = st.columns(4)
            for i, (_, row) in enumerate(bed.iterrows()):
                with cols[i % 4]:
                    crop_card(row, events)
            st.markdown("</div>", unsafe_allow_html=True)


def tree_health_class(status):
    s = safe_str(status).lower()
    if "bueno" in s:
        return "ok"
    if "atención" in s or "atencion" in s:
        return "warn"
    if "estrés" in s or "estres" in s:
        return "bad"
    return "neutral"


def arboles_view(arboles, events):
    st.markdown("<div class='filter-panel'><div class='filter-title'>Filtros</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    fincas = ["Todas"] + sorted([x for x in arboles["Finca_Nombre"].dropna().unique().tolist() if x]) if not arboles.empty else ["Todas"]
    f_finca = c1.selectbox("Finca", fincas, key="arbol_finca")
    estados = ["Todos"] + sorted([x for x in arboles["Estado_Fenologico"].dropna().unique().tolist() if x]) if not arboles.empty else ["Todos"]
    f_estado = c2.selectbox("Estado fenológico", estados, key="arbol_estado")
    st.markdown("</div>", unsafe_allow_html=True)
    view = arboles.copy()
    if f_finca != "Todas":
        view = view[view["Finca_Nombre"].eq(f_finca)]
    if f_estado != "Todos":
        view = view[view["Estado_Fenologico"].eq(f_estado)]
    for finca in sorted(view["Finca_Nombre"].dropna().unique()):
        st.markdown(f"<div class='section-title'>🌳 {finca}</div>", unsafe_allow_html=True)
        finca_trees = view[view["Finca_Nombre"].eq(finca)]
        cols = st.columns(3)
        for i, (_, row) in enumerate(finca_trees.iterrows()):
            with cols[i % 3]:
                arbol_id = safe_str(row.get("Arbol_ID"))
                last_abono = latest_event_for(events, "Abono tierra", arbol_id=arbol_id, completed=True)
                last_control = latest_event_for(events, "Control fitosanitario", arbol_id=arbol_id, completed=True)
                next_ev = next_event_for(events, arbol_id=arbol_id)
                health_cls = tree_health_class(row.get("Estado_Sanitario"))
                html = f"""
                <div class='tree-box'>
                  <div><span class='tree-icon'>{row.get('Icono','🌳')}</span><span class='tree-name'>{row.get('Arbol_Nombre','')}</span></div>
                  <div class='info-line'>Estado fenológico: <span class='badge blue'>{row.get('Estado_Fenologico','')}</span></div>
                  <div class='info-line'>Sanidad: <span class='badge {health_cls}'>{row.get('Estado_Sanitario','')}</span></div>
                  <div class='info-line'>Trasplante: {fmt_date(row.get('Fecha_Trasplante'))}</div>
                  <div class='info-line'>Último abono tierra: {last_abono.get('Insumo_Nombre','Sin registro') if last_abono is not None else 'Sin registro'} · {fmt_date(last_abono.get('Fecha_Realizada')) if last_abono is not None else ''}</div>
                  <div class='info-line'>Último control: {last_control.get('Insumo_Nombre','Sin registro') if last_control is not None else 'Sin registro'} · {fmt_date(last_control.get('Fecha_Realizada')) if last_control is not None else ''}</div>
                  <div class='info-line'>Próximo evento: {next_ev.get('Tipo_Evento','Sin pendiente') if next_ev is not None else 'Sin pendiente'} {('· ' + fmt_date(next_ev.get('Fecha_Programada'))) if next_ev is not None else ''}</div>
                  <div class='history-box'><b>Historial {TODAY.year}</b><br>{history_summary(events, arbol_id=arbol_id)}</div>
                  {control_indicator(events, arbol_id=arbol_id)}
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)


def week_of_year_from_jan1(d):
    if pd.isna(d):
        return None
    jan1 = date(d.year, 1, 1)
    return ((d.date() - jan1).days // 7) + 1


def calendario_view(df, events):
    st.markdown("<div class='filter-panel'><div class='filter-title'>Filtros calendario</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    months = sorted(df.dropna(subset=["Cosecha_Min"])["Cosecha_Min"].dt.strftime("%Y-%m").unique().tolist())
    if not months:
        months = [TODAY.strftime("%Y-%m")]
    default_month = TODAY.strftime("%Y-%m") if TODAY.strftime("%Y-%m") in months else months[0]
    month = c1.selectbox("Mes", months, index=months.index(default_month), key="cal_mes")
    finca = c2.selectbox("Finca", ["Todas"] + sorted(df["Finca"].dropna().unique().tolist()), key="cal_finca")
    cama = c3.selectbox("Cama", ["Todas"] + sorted(df["Unidad"].dropna().unique().tolist()), key="cal_cama")
    st.markdown("</div>", unsafe_allow_html=True)

    view = df[(~df["Es_Disponible"]) & (df["Cosecha_Min"].dt.strftime("%Y-%m") == month)].copy()
    if finca != "Todas":
        view = view[view["Finca"].eq(finca)]
    if cama != "Todas":
        view = view[view["Unidad"].eq(cama)]
    if view.empty:
        st.info("No hay cosechas mínimas para este filtro.")
        return
    view["Semana"] = view["Cosecha_Min"].apply(week_of_year_from_jan1)
    weeks = sorted(view["Semana"].dropna().unique().tolist())
    cols = st.columns(4)
    for i, wk in enumerate(weeks):
        with cols[i % 4]:
            wk_df = view[view["Semana"].eq(wk)].sort_values("Cosecha_Min")
            st.markdown("<div class='week-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='week-title'>Semana {int(wk)}</div>", unsafe_allow_html=True)
            for _, r in wk_df.iterrows():
                overdue = bool(r.get("Cosecha_Max_Vencida"))
                cls = "cal-overdue" if overdue else ""
                meta = CROP_META.get(r.get("Cultivo"), {"icon":"🌱"})
                st.markdown(
                    f"<div class='cal-item {cls}'><b>{meta['icon']} {r['Cultivo']}</b><br>{r['Finca']} · {r['Unidad']}<br>Cosecha mín: {fmt_date(r['Cosecha_Min'])}<br>Cosecha máx: {fmt_date(r['Cosecha_Max'])}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)


def eventos_view(events, insumos):
    if events.empty:
        st.info("No hay eventos agrícolas registrados.")
        return
    pending = events[~events["Estado"].eq("Completado")].dropna(subset=["Fecha_Programada"]).copy()
    pending_30 = pending[pending["Fecha_Programada"].dt.date <= TODAY + timedelta(days=30)]
    if not pending_30.empty:
        needs = pending_30.groupby(["Insumo_Nombre", "Tipo_Evento"]).size().reset_index(name="n")
        pills = " ".join([f"<span class='badge purple'>{r['Insumo_Nombre'] or 'Sin insumo'} · {int(r['n'])}</span>" for _, r in needs.iterrows()])
        st.markdown(f"<div class='event-box'><b>Insumos a alistar próximos 30 días</b><br>{pills}</div>", unsafe_allow_html=True)
    for tipo in ["Control fitosanitario", "Abono tierra", "Abono foliar", "Poda"]:
        subset = events[events["Tipo_Evento"].eq(tipo)].copy()
        if subset.empty:
            continue
        st.markdown(f"<div class='event-box'><div class='event-type-title'>{EVENT_ICON.get(tipo,'📌')} {tipo}</div>", unsafe_allow_html=True)
        subset = subset.sort_values(["Estado", "Fecha_Efectiva"], ascending=[True, False])
        for _, r in subset.iterrows():
            target = r.get("Arbol_Nombre") or r.get("Cultivo_Nombre") or r.get("Cama_ID") or "Sin objetivo"
            date_txt = fmt_date(r.get("Fecha_Realizada")) if r.get("Estado") == "Completado" else fmt_date(r.get("Fecha_Programada"))
            st.markdown(
                f"<div class='event-row'><b>{target}</b> · {r.get('Insumo_Nombre','Sin insumo')}<br>{status_badge(r.get('Estado'))} <span class='info-line'>{date_txt}</span><br><span class='info-line'>Momento: {r.get('Momento_Aplicacion','')} · Frecuencia: {r.get('Frecuencia_Dias','')} días</span></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def insumos_view(insumos):
    st.markdown("<div class='filter-panel'><div class='filter-title'>Filtros insumos</div>", unsafe_allow_html=True)
    tipos = ["Todos"] + sorted([x for x in insumos.get("Tipo", pd.Series(dtype=str)).dropna().unique().tolist() if x])
    f_tipo = st.selectbox("Tipo", tipos, key="ins_tipo")
    st.markdown("</div>", unsafe_allow_html=True)
    view = insumos if f_tipo == "Todos" else insumos[insumos["Tipo"].eq(f_tipo)]
    for _, r in view.iterrows():
        st.markdown(
            f"<div class='event-row'><b>{r.get('Nombre','')}</b> · {r.get('Tipo','')}<br><span class='badge {'ok' if r.get('Disponible')=='Sí' else 'bad'}'>Disponible: {r.get('Disponible','')}</span><span class='badge {'bad' if r.get('Compra_Requerida')=='Sí' else 'ok'}'>Compra: {r.get('Compra_Requerida','')}</span><br><span class='info-line'>{r.get('Uso_Principal','')}</span><br><span class='info-line'>Cantidad: {r.get('Cantidad_Guia','')} {r.get('Unidad_Medida','')} · Momento: {r.get('Momento_Aplicacion','')} · Frecuencia: {r.get('Frecuencia_Dias','')} días</span><br><span class='info-line'>Notas: {r.get('Restricciones/Notas','')}</span></div>",
            unsafe_allow_html=True,
        )


df, camas, arboles, eventos, insumos = load_data()

st.markdown("<div class='main-title'>Finca OS Dev</div>", unsafe_allow_html=True)

if not FILE_PATH.exists():
    st.error("No se encontró FincaOS_Data.xlsx en el repositorio.")
    st.stop()

tab_camas, tab_arboles, tab_cal, tab_eventos, tab_insumos = st.tabs(["🛏️ Camas", "🌳 Árboles", "📅 Calendario", "🧪 Eventos", "🧴 Insumos"])
with tab_camas:
    camas_view(df, camas, eventos)
with tab_arboles:
    arboles_view(arboles, eventos)
with tab_cal:
    calendario_view(df, eventos)
with tab_eventos:
    eventos_view(eventos, insumos)
with tab_insumos:
    insumos_view(insumos)
