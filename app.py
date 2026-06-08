from pathlib import Path
from datetime import date, datetime
import calendar

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finca OS Dev", layout="wide", page_icon="🌱")

DATA_FILE = "FincaOS_Data.xlsx"
BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / DATA_FILE
if not FILE_PATH.exists():
    st.error(f"No se encontró el archivo de datos requerido: {DATA_FILE}")
    st.stop()

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
    "Cebollino": {"icon": "🌾", "class": "chives"},
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
.week-card {
    background: rgba(255,255,255,0.94);
    border: 2px solid rgba(255,255,255,0.84);
    border-radius: 18px;
    padding: 14px;
    min-height: 320px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.13);
}
.week-title {font-size:18px; font-weight:950; color:#0f3d25; margin-bottom:2px;}
.week-range {font-size:12px; color:#64748b; font-weight:800; margin-bottom:12px;}
.event-card {
    border-radius: 14px;
    padding: 10px 10px;
    margin-bottom: 10px;
    border: 1px solid #e5e7eb;
    background:#ffffff;
}
.event-card.ready {background:#e7f8df; border:2px solid #86c96f;}
.event-card.soon {background:#fffbeb; border:2px solid #fbbf24;}
.event-card.future {background:#f8fafc; border:1px solid #cbd5e1;}
.event-row {display:flex; gap:9px; align-items:flex-start;}
.event-icon {font-size:26px; width:34px; text-align:center;}
.event-crop {font-weight:950; color:#0f172a; font-size:14px;}
.event-meta {font-size:12px; color:#475569; margin-top:2px; font-weight:700;}
.event-date {font-size:12px; margin-top:4px; font-weight:950;}
.ready-text {color:#15803d;}
.soon-text {color:#b45309;}
.future-text {color:#2563eb;}
.no-events {color:#94a3b8; font-size:13px; font-weight:800; text-align:center; margin-top:20px;}
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


def crop_card(row, idx):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})

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
        records = list(sort_crops_for_display(crops_df).iterrows())
        for start in range(0, len(records), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, (idx, row) in zip(cols, records[start:start + cols_per_row]):
                with col:
                    crop_card(row, idx)


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
    days = (pd.to_datetime(row["Cosecha_Min"]).date() - date.today()).days
    if days < 0:
        return "Cosecha disponible", "ready"
    if days <= 15:
        return "Próxima cosecha", "soon"
    return "Cosecha futura", "future"


def calendar_event_card(row):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})
    status_label, status_class = event_status(row)
    date_class = "ready-text" if status_class == "ready" else "soon-text" if status_class == "soon" else "future-text"
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


def render_calendar_view(filtered_df):
    today = date.today()
    month_options = []
    for offset in range(-2, 7):
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
    selected_label = st.selectbox("Mes del calendario", labels, index=labels.index(default_label) if default_label in labels else 0)
    _, selected_year, selected_month = next(x for x in month_options if x[0] == selected_label)

    calendar_df = filtered_df.copy()
    calendar_df = calendar_df[
        (calendar_df["Cultivo"] != "Disponible")
        & (calendar_df["Estado_Unidad"] != "No activa")
        & calendar_df["Cosecha_Min"].notna()
    ].copy()
    calendar_df["Cosecha_Date"] = calendar_df["Cosecha_Min"].dt.date
    calendar_df["Month_Match"] = calendar_df["Cosecha_Date"].apply(lambda d: d.year == selected_year and d.month == selected_month)
    month_df = calendar_df[calendar_df["Month_Match"]].copy()
    month_df["Week_Num"] = month_df["Cosecha_Date"].apply(app_week_number)

    available_count = int((calendar_df["Cosecha_Date"] < today).sum())
    soon_count = int(((calendar_df["Cosecha_Date"] >= today) & (calendar_df["Cosecha_Date"] <= today + pd.Timedelta(days=15))).sum())
    month_count = len(month_df)
    future_count = int((calendar_df["Cosecha_Date"] > today + pd.Timedelta(days=15)).sum())

    st.markdown(
        f"""
        <div class="calendar-toolbar">
            <div class="calendar-title">Calendario · {selected_label}</div>
            <div class="calendar-note">Las semanas usan secuencia anual: la semana del 1 de enero es Semana 1.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Disponibles", available_count, "cosecha mínima pasada")
    with c2:
        metric_card("Próximas 15 días", soon_count, "desde hoy")
    with c3:
        metric_card("En el mes", month_count, selected_label)
    with c4:
        metric_card("Futuras", future_count, "más de 15 días")

    week_nums = month_week_numbers(selected_year, selected_month)
    for start in range(0, len(week_nums), 3):
        cols = st.columns(3)
        for col, week_num in zip(cols, week_nums[start:start + 3]):
            with col:
                week_start, week_end = week_range_for_number(selected_year, week_num)
                events = month_df[month_df["Week_Num"] == week_num].sort_values(["Cosecha_Min", "Finca", "Unidad", "Cultivo"])
                st.markdown(
                    f"""
                    <div class="week-card">
                        <div class="week-title">Semana {week_num}</div>
                        <div class="week-range">{week_start.strftime('%d %b')} – {week_end.strftime('%d %b')}</div>
                    """,
                    unsafe_allow_html=True,
                )
                if events.empty:
                    st.markdown('<div class="no-events">Sin cosechas</div>', unsafe_allow_html=True)
                else:
                    for _, row in events.iterrows():
                        calendar_event_card(row)
                st.markdown("</div>", unsafe_allow_html=True)


df, units = load_data()

st.markdown('<div class="app-title">Finca OS Dev</div>', unsafe_allow_html=True)

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
available_harvest = active_crops[active_crops["Cosecha_Disponible"]].copy()
explicit_available = filtered[filtered["Cultivo"] == "Disponible"]

harvest_date = "Sin disponible"
harvest_note = ""
if not available_harvest.empty:
    item = available_harvest.sort_values("Cosecha_Min").iloc[0]
    harvest_date = fmt_date(item["Cosecha_Min"])
    harvest_note = f"{item['Cultivo']} · {item['Unidad']}"

m1, m2, m3, m4, m5, m6 = st.columns(6)
with m1:
    metric_card("Cultivos activos", len(active_crops), "sin contar espacios disponibles")
with m2:
    metric_card("Camas visibles", filtered_units["Unidad"].nunique(), "según filtros")
with m3:
    metric_card("Cosecha Disponible", harvest_date, harvest_note)
with m4:
    metric_card("Cosechas disponibles", len(available_harvest), "cosecha mínima en el pasado")
with m5:
    metric_card("Espacios disponibles", len(explicit_available), "oportunidad de siembra")
with m6:
    metric_card("Errores de datos", int((filtered["Visual_Status"] == "Dato faltante").sum()), "falta información")

tab_camas, tab_calendario = st.tabs(["🌱 Camas", "📅 Calendario"])

with tab_camas:
    for finca, unit_group in filtered_units.groupby("Finca", sort=False):
        st.markdown(f'<div class="section-title">📍 {finca}</div>', unsafe_allow_html=True)
        unit_records = list(unit_group.sort_values("Unidad").iterrows())
        for start in range(0, len(unit_records), 2):
            cols = st.columns(2)
            for col, (_, unit_row) in zip(cols, unit_records[start:start + 2]):
                with col:
                    crops = filtered[filtered["Unidad"] == unit_row["Unidad"]]
                    bed_panel(unit_row, crops)

with tab_calendario:
    render_calendar_view(filtered)

if show_detail_table:
    st.divider()
    st.subheader("Detalle de datos")
    show_cols = [
        "Finca", "Unidad", "Cultivo", "Cantidad", "Estado_Actual",
        "Fecha_Siembra", "Fecha_Trasplante", "Cosecha_Min", "Cosecha_Max", "Visual_Status"
    ]
    table = filtered[show_cols].copy().sort_values(["Finca", "Unidad", "Cultivo"])
    st.dataframe(table, use_container_width=True, hide_index=True)
