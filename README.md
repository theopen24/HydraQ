from pathlib import Path
from datetime import date, datetime, timedelta
import calendar
from textwrap import dedent

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finca OS Dev", layout="wide", page_icon="🌱")

SPREADSHEET_ID = "1ixV756fBEQPzMck3kNuG24X2JJkgnauXE5IXAIAGwR8"
BASE_DIR = Path(__file__).parent
LOGO_FILE = BASE_DIR / "hydraq_logo.png"
ASSETS_DIR = BASE_DIR / "assets"

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


MONTHS_EN = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

LANG_LABELS = {"Español": "es", "English": "en"}

UI_TEXT = {
    "es": {
        "app_title": "Finca OS Dev",
        "filters": "Filtros",
        "language": "Idioma",
        "data_source": "Datos: Google Sheets",
        "farm": "Finca",
        "bed": "Cama",
        "crop": "Cultivo",
        "visual_status": "Estado visual",
        "show_detail_table": "Mostrar tabla detalle",
        "dashboard": "Dashboard",
        "beds": "Camas",
        "trees": "Árboles",
        "events": "Eventos",
        "calendar": "Calendario",
        "account": "Cuenta",
        "date_none": "Sin fecha",
        "date_base_none": "Sin fecha base",
        "transplant": "Trasplante",
        "planting": "Siembra",
        "status": "Estado",
        "quantity": "Cantidad",
        "harvest_min": "Cosecha min",
        "harvest_max": "Cosecha max",
        "harvest_today": "hoy",
        "in_days": "en {days} días",
        "days_ago": "hace {days} días",
        "active_visible": "activos visibles",
        "by_filters": "según filtros",
        "harvest": "Cosecha",
        "available_harvests_short": "Cosechas disp.",
        "no_available_harvest": "No hay cosechas disponibles",
        "min_in_past": "mínima en el pasado",
        "spaces": "Espacios",
        "available_plural": "disponibles",
        "errors": "Errores",
        "missing_data": "datos faltantes",
        "registered": "registrados",
        "events_15d": "Eventos 15d",
        "pending_next": "pendientes próximos",
        "rain_weather": "🌧️ Lluvias y clima",
        "pending_real_rain": "Pendiente integrar lluvia real.",
        "intended_use": "Uso previsto",
        "weather_use": "mover foliares, riego y controles según pronóstico.",
        "overdue": "Vencidos",
        "events_not_done": "eventos sin completar.",
        "no_alerts": "Sin alertas",
        "no_events_15": "No hay eventos próximos en 15 días.",
        "special_events": "⚠️ Eventos especiales",
        "quick_notes": "📝 Notas rápidas",
        "quick_notes_help": "Captura temporal para ideas, observaciones o mensajes que luego GPT puede convertir en cambios de datos.",
        "new_note": "Nueva nota",
        "note_placeholder": "Ejemplo: En Frailes vi hojas con manchas en pepino. Programar control fitosanitario con Mistral.",
        "download_note": "Descargar nota",
        "available_space": "Espacio disponible",
        "no_active_crops": "Sin cultivos activos",
        "max_overdue": "Cosecha máxima vencida",
        "harvest_available": "Cosecha disponible",
        "upcoming_harvest": "Próxima cosecha",
        "future_harvest": "Cosecha futura",
        "month": "Mes",
        "only_next_15": "Solo próximos 15 días",
        "week": "Semana",
        "no_upcoming_15": "No hay cosechas próximas en los próximos 15 días para los filtros seleccionados.",
        "no_min_month": "No hay cultivos con cosecha mínima en el mes seleccionado.",
        "event_type": "Tipo de evento",
        "all_f": "Todas",
        "all_m": "Todos",
        "no_events_filters": "No hay eventos agrícolas para los filtros seleccionados.",
        "input": "Insumo",
        "date": "Fecha",
        "no_input": "Sin insumo",
        "input_catalog": "Catálogo de insumos",
        "no_inputs": "Sin insumos registrados.",
        "purchase_required": "Compra requerida",
        "available_stock": "Disponible",
        "guide_qty": "Cantidad guía",
        "timing": "Momento",
        "frequency": "Frecuencia",
        "no_rule": "Sin regla",
        "according_criteria": "Según criterio",
        "according_state": "Según estado",
        "account_profile": "Perfil y configuración general de FincaOS",
        "user": "Usuario",
        "name": "Nombre",
        "email": "Correo",
        "not_configured": "no configurado",
        "access_permissions": "Permisos de acceso",
        "access_future": "Módulo reservado para administrar accesos. No desarrollado en esta versión.",
        "future_work": "Trabajo futuro",
        "version": "Versión",
        "developer_version": "Developer Version",
        "date_label": "Fecha",
        "developed_with": "Desarrollado con",
        "plugins": "🔌 PlugIns",
        "plugins_text": "Espacio reservado para integraciones futuras: clima, lluvia, GPT Actions y Google Sheets.",
        "detail_title": "Detalle de datos",
        "health_status": "Estado sanitario",
        "phenology": "Estado fenológico",
        "last_control": "Último control",
        "next_abono_no_history": "Próximo abono: sin historial para calcular frecuencia.",
        "next_abono_no_soil": "Próximo abono: sin abonada de tierra registrada.",
        "last_abono": "Último abono",
        "next_abono_suggested": "Próximo abono sugerido",
        "guide_quantity": "Cantidad guía",
        "history_year": "Historial año",
        "crops": "Cultivos sembrados",
        "different_species": "{n} especies diferentes",
        "climate": "Clima",
        "progress": "Avance",
        "weekly": "Semanal",
        "monthly": "Mensual",
        "period": "Periodo",
        "both": "Ambas",
        "rain_7_days": "Lluvia 7 días",
        "sun_hours": "Horas de sol",
        "rainy_days": "Días lluviosos",
        "avg_temp": "Temperatura media",
        "current_week": "Semana actual",
        "monthly_summary": "Resumen mensual",
        "weekly_recommendation": "Recomendación semanal",
        "photo_progress": "Progreso fotográfico",
        "photo_progress_help": "Documenta el crecimiento mes a mes. Sube nuevas fotos y compáralas.",
        "upload_new_photo": "Subir nueva foto",
        "last_gpt_events": "Últimos eventos GPT",
        "last_gpt_events_help": "Últimas 10 entradas registradas por el flujo GPT / Apps Script.",
        "no_gpt_log": "No hay entradas recientes del log GPT.",
        "sample_data": "Datos demostrativos",
        "future_integration": "Integración real pendiente",
        "camera_note": "Recomendación: tomar fotos desde el mismo ángulo, misma cama y mismo periodo mensual."
    },
    "en": {
        "app_title": "Finca OS Dev",
        "filters": "Filters",
        "language": "Language",
        "data_source": "Data: Google Sheets",
        "farm": "Farm",
        "bed": "Bed",
        "crop": "Crop",
        "visual_status": "Visual status",
        "show_detail_table": "Show detail table",
        "dashboard": "Dashboard",
        "beds": "Beds",
        "trees": "Trees",
        "events": "Events",
        "calendar": "Calendar",
        "account": "Account",
        "date_none": "No date",
        "date_base_none": "No base date",
        "transplant": "Transplant",
        "planting": "Planting",
        "status": "Status",
        "quantity": "Quantity",
        "harvest_min": "Harvest min",
        "harvest_max": "Harvest max",
        "harvest_today": "today",
        "in_days": "in {days} days",
        "days_ago": "{days} days ago",
        "active_visible": "visible active",
        "by_filters": "by filters",
        "harvest": "Harvest",
        "available_harvests_short": "Harvests avail.",
        "no_available_harvest": "No harvests available",
        "min_in_past": "minimum date in the past",
        "spaces": "Spaces",
        "available_plural": "available",
        "errors": "Errors",
        "missing_data": "missing data",
        "registered": "registered",
        "events_15d": "Events 15d",
        "pending_next": "upcoming pending",
        "rain_weather": "🌧️ Rain and weather",
        "pending_real_rain": "Real rainfall integration pending.",
        "intended_use": "Planned use",
        "weather_use": "move foliar sprays, irrigation and controls based on forecast.",
        "overdue": "Overdue",
        "events_not_done": "events not completed.",
        "no_alerts": "No alerts",
        "no_events_15": "No upcoming events in 15 days.",
        "special_events": "⚠️ Special events",
        "quick_notes": "📝 Quick notes",
        "quick_notes_help": "Temporary capture for ideas, observations or messages that GPT can later convert into data changes.",
        "new_note": "New note",
        "note_placeholder": "Example: In Frailes I saw spotted leaves on cucumber. Schedule phytosanitary control with Mistral.",
        "download_note": "Download note",
        "available_space": "Available space",
        "no_active_crops": "No active crops",
        "max_overdue": "Maximum harvest overdue",
        "harvest_available": "Harvest available",
        "upcoming_harvest": "Upcoming harvest",
        "future_harvest": "Future harvest",
        "month": "Month",
        "only_next_15": "Only next 15 days",
        "week": "Week",
        "no_upcoming_15": "No upcoming harvests in the next 15 days for the selected filters.",
        "no_min_month": "No crops with minimum harvest date in the selected month.",
        "event_type": "Event type",
        "all_f": "All",
        "all_m": "All",
        "no_events_filters": "No agricultural events for the selected filters.",
        "input": "Input",
        "date": "Date",
        "no_input": "No input",
        "input_catalog": "Input catalog",
        "no_inputs": "No inputs recorded.",
        "purchase_required": "Purchase required",
        "available_stock": "Available",
        "guide_qty": "Guide quantity",
        "timing": "Timing",
        "frequency": "Frequency",
        "no_rule": "No rule",
        "according_criteria": "By criteria",
        "according_state": "By stage",
        "account_profile": "Profile and general FincaOS settings",
        "user": "User",
        "name": "Name",
        "email": "Email",
        "not_configured": "not configured",
        "access_permissions": "Access permissions",
        "access_future": "Reserved module for access management. Not developed in this version.",
        "future_work": "Future work",
        "version": "Version",
        "developer_version": "Developer Version",
        "date_label": "Date",
        "developed_with": "Developed with",
        "plugins": "🔌 Plugins",
        "plugins_text": "Reserved space for future integrations: weather, rainfall, GPT Actions and Google Sheets.",
        "detail_title": "Data detail",
        "health_status": "Health status",
        "phenology": "Phenological stage",
        "last_control": "Last control",
        "next_abono_no_history": "Next soil fertilization: no history to calculate frequency.",
        "next_abono_no_soil": "Next soil fertilization: no soil fertilization recorded.",
        "last_abono": "Last fertilization",
        "next_abono_suggested": "Suggested next fertilization",
        "guide_quantity": "Guide quantity",
        "history_year": "Year history",
        "crops": "Planted crops",
        "different_species": "{n} different species",
        "climate": "Climate",
        "progress": "Progress",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "period": "Period",
        "both": "Both",
        "rain_7_days": "7-day rain",
        "sun_hours": "Sun hours",
        "rainy_days": "Rainy days",
        "avg_temp": "Average temperature",
        "current_week": "Current week",
        "monthly_summary": "Monthly summary",
        "weekly_recommendation": "Weekly recommendation",
        "photo_progress": "Photo progress",
        "photo_progress_help": "Document growth month by month. Upload and compare new photos.",
        "upload_new_photo": "Upload new photo",
        "last_gpt_events": "Latest GPT events",
        "last_gpt_events_help": "Latest 10 entries recorded through the GPT / Apps Script flow.",
        "no_gpt_log": "No recent GPT log entries.",
        "sample_data": "Demo data",
        "future_integration": "Real integration pending",
        "camera_note": "Recommendation: take photos from the same angle, same bed and same monthly period."
    }
}

VALUE_TEXT = {
    "en": {
        "Activa": "Active",
        "No activa": "Not active",
        "Dato faltante": "Missing data",
        "Disponible": "Available",
        "Corte": "Cutting stage",
        "Completado": "Completed",
        "Programado": "Scheduled",
        "Pendiente": "Pending",
        "Realizado": "Completed",
        "Control fitosanitario": "Pest control",
        "Abono tierra": "Soil fertilization",
        "Abono foliar": "Foliar feeding",
        "Poda": "Pruning",
        "Cosecha": "Harvest",
        "Siembra": "Planting",
        "Trasplante": "Transplant",
        "Riego": "Irrigation",
        "Mantenimiento de riego": "Irrigation maintenance",
        "Enmienda": "Soil amendment",
        "Amarre": "Tying",
        "Arqueo de ramas": "Branch bending",
        "Estrés hídrico": "Water stress",
        "Sin estado": "No status",
        "Floración": "Flowering",
        "Cuajado": "Fruit set",
        "Llenado": "Fruit filling",
        "Vegetativo": "Vegetative",
        "Sano": "Healthy",
        "Observación": "Observation"
    },
    "es": {}
}

if "lang" not in st.session_state:
    st.session_state["lang"] = "es"


def lang_code():
    return st.session_state.get("lang", "es")


def t(key):
    return UI_TEXT.get(lang_code(), UI_TEXT["es"]).get(key, UI_TEXT["es"].get(key, key))


def tv(value):
    if value is None or pd.isna(value):
        return ""
    text = str(value)
    return VALUE_TEXT.get(lang_code(), {}).get(text, text)


def month_name(month_number):
    return (MONTHS_EN if lang_code() == "en" else MONTHS_ES).get(month_number, str(month_number))

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


.photo-card {background:rgba(255,255,255,.95);border:1px solid rgba(255,255,255,.72);border-radius:16px;padding:10px;box-shadow:0 6px 16px rgba(0,0,0,.14);margin-bottom:12px;color:#0f172a;}
.photo-title {font-size:14px;font-weight:950;color:#0f3d25;margin-top:7px;}
.photo-note {font-size:12px;color:#64748b;font-weight:750;margin-top:3px;}
.weather-card {background:rgba(255,255,255,.95);border:1px solid rgba(255,255,255,.72);border-radius:18px;padding:14px;box-shadow:0 6px 18px rgba(0,0,0,.14);margin-bottom:12px;color:#0f172a;}
.weather-title {font-size:15px;font-weight:950;color:#31543d;margin-bottom:4px;}
.weather-value {font-size:26px;font-weight:950;color:#0f3d25;}
.weather-note {font-size:12px;color:#64748b;font-weight:750;}
.weather-day {background:rgba(255,255,255,.94);border:1px solid #dbe7de;border-radius:14px;padding:10px;text-align:center;min-height:130px;color:#0f172a;}
.weather-icon {font-size:30px;margin:3px 0;}
.reco-card {background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;padding:10px 12px;margin-bottom:8px;color:#14532d;font-weight:800;}
.bed-image-caption {font-size:12px;color:#d1fae5;font-weight:800;margin:6px 0 10px 0;}

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


def _sheet_csv_url(sheet_name):
    from urllib.parse import quote
    return (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={quote(sheet_name)}"
    )


def _read_sheet(sheet_name, empty_columns=None):
    try:
        return pd.read_csv(_sheet_csv_url(sheet_name))
    except Exception as exc:
        # En la opción A, la hoja debe estar compartida como: cualquiera con el enlace puede ver.
        # Si una pestaña opcional no existe, devolvemos un DataFrame vacío para no romper la app.
        if empty_columns is not None:
            return pd.DataFrame(columns=empty_columns)
        st.error(
            f"No pude leer la pestaña '{sheet_name}' desde Google Sheets. "
            "Revisá que la hoja esté compartida como 'Cualquier persona con el enlace puede ver' "
            "y que el nombre de la pestaña sea correcto."
        )
        st.caption(str(exc))
        st.stop()


@st.cache_data(ttl=120, show_spinner="Cargando datos desde Google Sheets...")
def load_data():
    fincas = _read_sheet("Fincas")
    unidades = _read_sheet("Unidades")

    # Preferimos VistaCultivos si existe. Si no existe, armamos la vista desde las tablas base.
    try:
        df = _read_sheet("VistaCultivos", [])
        if df.empty:
            raise ValueError("VistaCultivos vacía")
    except Exception:
        cultivos = _read_sheet("CatalogoCultivos")
        siembras = _read_sheet("CultivosSembrados")
        df = siembras.merge(fincas, on="Finca_ID", how="left")
        df = df.merge(unidades, on=["Unidad_ID", "Finca_ID"], how="left")
        df = df.merge(cultivos, on="Cultivo_ID", how="left")

    arboles = _read_sheet("Arboles", ["Arbol_ID","Finca","Arbol","Icono","Estado_Fenologico","Trasplante","Estado_Sanitario","Evento_Agricola"])
    if arboles.empty:
        arboles = pd.DataFrame(TREE_DATA)

    eventos = _read_sheet(
        "EventosAgricolas",
        ["ID_Evento","Tipo_Evento","ID_Insumo","Nombre_Insumo","Target_Tipo","Target_ID",
         "Target_Label","Finca","Unidad","Cultivo","Arbol","Fecha_Programada",
         "Fecha_Realizada","Estado","Notas"]
    )

    insumos = _read_sheet(
        "Insumos",
        ["ID_Insumo","Nombre","Tipo","Disponible","Uso_Principal","Restricciones/Notas","Compra_Requerida"]
    )

    log_gpt = _read_sheet(
        "LogCambiosGPT",
        ["FechaHora", "Accion", "Estado", "ComandoOriginal", "DetalleJSON", "ResultadoJSON"]
    )

    return clean_view(df), clean_units(unidades, fincas), clean_trees(arboles), clean_events(eventos), insumos, clean_gpt_log(log_gpt)


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


def clean_gpt_log(log_df):
    out = log_df.copy()
    for col in ["FechaHora", "Accion", "Estado", "ComandoOriginal", "DetalleJSON", "ResultadoJSON"]:
        if col not in out.columns:
            out[col] = ""
    out["FechaHora"] = pd.to_datetime(out["FechaHora"], errors="coerce", dayfirst=True)
    for col in ["Accion", "Estado", "ComandoOriginal", "DetalleJSON", "ResultadoJSON"]:
        out[col] = out[col].fillna("").astype(str)
    return out


def asset_path(name):
    path = ASSETS_DIR / name
    return str(path) if path.exists() else None


def bed_photo_for(unit_name):
    u = str(unit_name).lower()
    if "6" in u:
        return asset_path("cama_6_y_3.jpeg"), "Cama 6 / referencia actual"
    if "3" in u:
        return asset_path("cama_6_y_3.jpeg"), "Cama 3 / referencia actual"
    if "1" in u or "2" in u:
        return asset_path("vista_este.jpeg"), "Vista de referencia"
    if "4" in u or "5" in u or "7" in u:
        return asset_path("vista_sur.jpeg"), "Vista de referencia"
    return None, "Referencia visual pendiente"


def normalized_tree_icon(row):
    name = str(row.get("Arbol", "")).lower()
    icon = str(row.get("Icono", "") or "🌳")
    if "limón mandarina" in name or "limon mandarina" in name:
        return "🍋"
    if "🍋" in icon and "🍊" in icon:
        return "🍋"
    return icon


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
        return f'<div class="control-line">{tv("Control fitosanitario")} <span class="control-pill event-no-empezado">{t("no_alerts")}</span></div>'
    cls = event_status_class(control.get("estado"), control.get("fecha"))
    insumo = control.get("insumo") or t("no_input")
    fecha = fmt_date(control.get("fecha")) if pd.notna(control.get("fecha")) else t("date_none")
    return f'<div class="control-line">{tv("Control fitosanitario")} <span class="control-pill {cls}">{tv(control.get("estado", ""))}</span> · {insumo} · {fecha}</div>'



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
        return f'<div class="history-line">{t("history_year")}: <span class="history-pill">{t("no_alerts")}</span></div>'
    subset["_key"] = subset["Tipo_Evento"].fillna("").apply(tv) + ": " + subset["Nombre_Insumo"].fillna(t("no_input"))
    counts = subset.groupby("_key").size().sort_values(ascending=False)
    pills = "".join([f'<span class="history-pill">{k} x{v}</span>' for k, v in counts.items()])
    return f'<div class="history-line">{t("history_year")}: {pills}</div>'


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
        return f'<div class="next-abono">{t("next_abono_no_history")}</div>'
    subset = completed_events_for_target(events, target_id)
    subset = subset[subset["Tipo_Evento"].astype(str).str.lower() == "abono tierra"] if not subset.empty else subset
    if subset.empty:
        return f'<div class="next-abono">{t("next_abono_no_soil")}</div>'
    subset = subset.sort_values("_date")
    last = subset.iloc[-1]
    meta = insumo_metadata(insumos, last.get("ID_Insumo"), last.get("Nombre_Insumo"))
    freq = pd.to_numeric(meta.get("Frecuencia_Dias", None), errors="coerce")
    insumo = last.get("Nombre_Insumo") or meta.get("Nombre") or "Abono tierra"
    last_date = pd.to_datetime(last.get("_date")).date()
    cantidad = meta.get("Cantidad_Guia", "") or t("according_criteria")
    momento = meta.get("Momento_Aplicacion", "") or t("according_state")
    if pd.isna(freq) or float(freq) <= 0:
        return f'<div class="next-abono">{t("last_abono")}: {insumo} · {fmt_date(last_date)} · {t("guide_quantity")}: {cantidad}</div>'
    next_date = last_date + timedelta(days=int(freq))
    days = (next_date - date.today()).days
    cls = "next-abono overdue" if days <= 0 else "next-abono"
    timing = t("overdue").lower() if days < 0 else t("harvest_today") if days == 0 else t("in_days").format(days=days)
    return f'<div class="{cls}">{t("next_abono_suggested")}: {insumo} · {fmt_date(next_date)} ({timing})<br>{t("guide_quantity")}: {cantidad}<br>{t("timing")}: {momento}</div>'

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
        return t("date_none")
    return pd.to_datetime(value).strftime("%d %b %Y")


def base_date_label(row):
    if pd.notna(row["Fecha_Trasplante"]):
        return f"{t('transplant')}: {fmt_date(row['Fecha_Trasplante'])}"
    if pd.notna(row["Fecha_Siembra"]):
        return f"{t('planting')}: {fmt_date(row['Fecha_Siembra'])}"
    return t("date_base_none")


def days_html(value, prefix):
    if pd.isna(value):
        return f'<div class="info-line">{prefix}: {t("date_none")}</div>'
    days = (pd.to_datetime(value).date() - date.today()).days
    if days > 0:
        return f'<div class="info-line">{prefix}: {t("in_days").format(days=days)}</div>'
    if days == 0:
        return f'<div class="info-line past-harvest"><b>{prefix}: {t("harvest_today")}</b></div>'
    return f'<div class="info-line past-harvest"><b>{prefix}: {t("days_ago").format(days=abs(days))}</b></div>'


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


def render_dashboard_view(filtered, filtered_units, events, trees, log_gpt=None):
    active_crops = filtered[(filtered["Cultivo"] != "Disponible") & (filtered["Estado_Unidad"] != "No activa")].copy()
    available_harvest = active_crops[active_crops["Cosecha_Disponible"]].copy()
    explicit_available = filtered[filtered["Cultivo"] == "Disponible"].copy()
    errors = int((filtered["Visual_Status"] == "Dato faltante").sum())
    total_plants = int(pd.to_numeric(active_crops.get("Cantidad", 0), errors="coerce").fillna(0).sum()) if not active_crops.empty else 0
    species_count = int(active_crops["Cultivo"].nunique()) if not active_crops.empty else 0

    next_harvest_value = t("date_none")
    next_harvest_note = t("no_available_harvest")
    if not available_harvest.empty:
        item = available_harvest.sort_values("Cosecha_Min").iloc[0]
        next_harvest_value = fmt_date(item["Cosecha_Min"])
        next_harvest_note = f"{item['Cultivo']} · {item['Unidad']}"

    next_15_events = pd.DataFrame()
    overdue_events = pd.DataFrame()
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

    active_trees = 0 if trees is None or trees.empty else len(trees)
    cards = [
        (t("crops"), total_plants, t("different_species").format(n=species_count)),
        (t("trees"), active_trees, t("registered")),
        (t("beds"), filtered_units["Unidad"].nunique(), t("by_filters")),
        (t("harvest"), next_harvest_value, next_harvest_note),
        (t("available_harvests_short"), len(available_harvest), t("min_in_past")),
        (t("spaces"), len(explicit_available), t("available_plural")),
        (t("errors"), errors, t("missing_data")),
        (t("events_15d"), len(next_15_events), t("pending_next")),
    ]
    dashboard_metric_cards(cards)

    c1, c2 = st.columns([1,1])
    with c1:
        lines = []
        if len(overdue_events) > 0:
            lines.append(f'<div class="dash-line"><span class="dash-pill pill-red">{t("overdue")}</span> {len(overdue_events)} {t("events_not_done")}</div>')
        if len(next_15_events) > 0:
            sample = next_15_events.sort_values("_date").head(3)
            for _, r in sample.iterrows():
                lines.append(f'<div class="dash-line"><span class="dash-pill pill-yellow">{fmt_date(r["_date"])}</span> {r.get("Tipo_Evento", "Evento")} · {r.get("Target_Label", "")}</div>')
        if not lines:
            lines.append(f'<div class="dash-line"><span class="dash-pill pill-green">{t("no_alerts")}</span> {t("no_events_15")}</div>')
        html_block(f'<div class="dash-panel"><div class="dash-panel-title">{t("special_events")}</div>{"".join(lines)}</div>')
    with c2:
        html_block(f'<div class="dash-panel"><div class="dash-panel-title">{t("quick_notes")}</div><div class="dash-line">{t("quick_notes_help")}</div></div>')
        note = st.text_area(t("new_note"), placeholder=t("note_placeholder"), height=90, key="quick_note")
        if note.strip():
            st.download_button(t("download_note"), data=note.strip(), file_name=f"fincaos_nota_{date.today().isoformat()}.txt", mime="text/plain")

    render_gpt_log_panel(log_gpt)


def render_gpt_log_panel(log_gpt):
    st.markdown(f'<div class="event-section-title">🧾 {t("last_gpt_events")}</div>', unsafe_allow_html=True)
    st.caption(t("last_gpt_events_help"))
    if log_gpt is None or log_gpt.empty:
        html_block(f'<div class="dash-panel"><div class="dash-line">{t("no_gpt_log")}</div></div>')
        return
    view = log_gpt.sort_values("FechaHora", ascending=False).head(10).copy()
    view["Fecha"] = view["FechaHora"].dt.strftime("%d/%m/%Y %H:%M").fillna("")
    view = view[["Fecha", "Accion", "Estado", "ComandoOriginal"]]
    st.dataframe(view, use_container_width=True, hide_index=True)


def render_weather_view():
    st.markdown(f'<div class="section-title">☁️ {t("climate")}</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1.4])
    with c1:
        st.radio(t("period"), [t("weekly"), t("monthly")], horizontal=True)
    with c2:
        finca = st.radio(t("farm"), ["Moravia", "Frailes", t("both")], horizontal=True)
    with c3:
        st.selectbox(t("week"), ["12 – 18 mayo 2025", "19 – 25 mayo 2025", "26 mayo – 1 junio 2025"], key="weather_week")

    mock = {"Moravia": {"rain": 28.4, "sun": 32.1, "days": 3, "temp": 24.3}, "Frailes": {"rain": 68.7, "sun": 18.6, "days": 5, "temp": 22.1}}
    farms = ["Moravia", "Frailes"] if finca == t("both") else [finca]
    cols = st.columns(4)
    metrics = [("🌧️", t("rain_7_days"), "rain", "mm"), ("☀️", t("sun_hours"), "sun", "h"), ("☔", t("rainy_days"), "days", ""), ("🌡️", t("avg_temp"), "temp", "°C")]
    for col, (icon, label, key, suffix) in zip(cols, metrics):
        with col:
            details = " · ".join([f"{f}: {mock[f][key]}{suffix}" for f in farms])
            html_block(f'<div class="weather-card"><div class="weather-title">{icon} {label}</div><div class="weather-value">{mock[farms[0]][key]}{suffix}</div><div class="weather-note">{details}</div></div>')

    left, mid, right = st.columns([1.2,1.1,1])
    days = [("LUN 12", "🌧️", "6.8 mm", "2.1 h", "lluvia media"), ("MAR 13", "🌤️", "1.2 mm", "6.3 h", "nublado parcial"), ("MIÉ 14", "🌤️", "0.0 mm", "5.8 h", "soleado"), ("JUE 15", "🌧️", "12.6 mm", "1.4 h", "lluvia alta"), ("VIE 16", "🌧️", "6.3 mm", "2.0 h", "lluvia media"), ("SÁB 17", "☀️", "0.0 mm", "8.2 h", "soleado"), ("DOM 18", "🌤️", "1.5 mm", "6.3 h", "nublado parcial")]
    with left:
        st.markdown(f"### {t('current_week')}")
        dcols = st.columns(7)
        for c, d in zip(dcols, days):
            with c:
                html_block(f'<div class="weather-day"><b>{d[0]}</b><div class="weather-icon">{d[1]}</div><div>{d[2]}</div><div>{d[3]}</div><small>{d[4]}</small></div>')
    with mid:
        st.markdown(f"### {t('monthly_summary')}")
        chart_data = pd.DataFrame({"Moravia": [24, 13, 37, 18, 28], "Frailes": [54, 31, 82, 45, 69]}, index=["14-20 abr", "21-27 abr", "28 abr-4 may", "5-11 may", "12-18 may"])
        st.bar_chart(chart_data)
    with right:
        st.markdown(f"### {t('weekly_recommendation')}")
        recos = ["Frailes: postergar abono foliar por lluvia acumulada alta.", "Moravia: ventana favorable para control fitosanitario.", "Revisar riego si la lluvia semanal es baja.", "Vigilar hongos tras varios días húmedos."]
        for r in recos:
            html_block(f'<div class="reco-card">{r}</div>')
    html_block(f'<div class="dash-panel"><div class="dash-line"><b>{t("sample_data")}.</b> {t("future_integration")}.</div></div>')


def render_progress_view():
    st.markdown(f'<div class="section-title">📷 {t("progress")}</div>', unsafe_allow_html=True)
    html_block(f'<div class="dash-panel"><div class="dash-panel-title">{t("photo_progress")}</div><div class="dash-line">{t("photo_progress_help")}</div><div class="dash-line"><span class="dash-pill pill-blue">Tip</span>{t("camera_note")}</div></div>')
    records = [("Frailes · Vista general", "Mayo 2025", "vista_sur.jpeg"), ("Frailes · Cama 6", "Junio 2025", "cama_6_y_3.jpeg"), ("Frailes · Vista este", "Junio 2025", "vista_este.jpeg")]
    cols = st.columns(3)
    for col, (title, month, img) in zip(cols, records):
        with col:
            path = asset_path(img)
            if path:
                st.image(path, use_container_width=True)
            html_block(f'<div class="photo-card"><div class="photo-title">{title}</div><div class="photo-note">{month}</div></div>')
    uploaded = st.file_uploader(t("upload_new_photo"), type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded:
        st.write(f"{len(uploaded)} archivo(s) cargado(s) para vista previa. Persistencia real pendiente de integrar.")
        for file in uploaded[:3]:
            st.image(file, caption=file.name, use_container_width=True)

def crop_card(row, idx, events=None):
    crop = row["Cultivo"]
    meta = CROP_META.get(crop, {"icon": "🌱", "class": "lettuce"})

    control_html = control_status_html(latest_control_status(events, row.get("Siembra_ID")))

    if is_available_placeholder(row):
        st.markdown(
            f"""
            <div class="crop-card available-card">
                <div class="icon-circle {meta['class']}">{meta['icon']}</div>
                <div class="crop-name">{tv("Disponible")}</div>
                <div class="qty">{t("available_space")}</div>
                <div class="info-line">{t("status")}: <b>{tv("Disponible")}</b></div>
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
            <div class="info-line">{t("status")}: <b>{tv(display_state(row))}</b></div>
            <div class="info-line">{base_date_label(row)}</div>
            {days_html(row['Cosecha_Min'], t("harvest_min"))}
            {days_html(row['Cosecha_Max'], t("harvest_max"))}
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
                <span class="badge {badge_class}">{tv(status)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        photo_path, photo_caption = bed_photo_for(unidad)
        if photo_path:
            st.image(photo_path, use_container_width=True)
            st.markdown(f'<div class="bed-image-caption">📷 {photo_caption}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bed-image-caption">📷 {photo_caption}</div>', unsafe_allow_html=True)
        if str(unit_row.get("Estado_Unidad", "")).lower().startswith("no activa"):
            st.markdown(f'<div class="empty-card">{tv("No activa")}</div>', unsafe_allow_html=True)
            return
        if crops_df is None or crops_df.empty:
            st.markdown(f'<div class="empty-card">{t("no_active_crops")}</div>', unsafe_allow_html=True)
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
        return t("date_none"), "future"
    min_date = pd.to_datetime(row["Cosecha_Min"]).date()
    max_date = pd.to_datetime(row["Cosecha_Max"]).date() if pd.notna(row["Cosecha_Max"]) else None
    days = (min_date - date.today()).days
    if max_date is not None and max_date < date.today():
        return t("max_overdue"), "overdue"
    if days <= 0:
        return t("harvest_available"), "available"
    if days <= 15:
        return t("upcoming_harvest"), "soon"
    return t("future_harvest"), "future"


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
                    <div class="event-meta">{t("harvest_max")}: {fmt_date(row['Cosecha_Max'])}</div>
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
        month_options.append((f"{month_name(m)} {y}", y, m))

    labels = [x[0] for x in month_options]
    default_label = f"{month_name(today.month)} {today.year}"

    c1, c2, c3, c4 = st.columns([1.15, 1.15, 1.35, 1.25])
    with c1:
        selected_label = st.selectbox(t("month"), labels, index=labels.index(default_label) if default_label in labels else 0, key="cal_mes")
    _, selected_year, selected_month = next(x for x in month_options if x[0] == selected_label)

    calendar_base = all_df.copy()
    calendar_base = calendar_base[
        (calendar_base["Cultivo"] != "Disponible")
        & (calendar_base["Estado_Unidad"] != "No activa")
        & calendar_base["Cosecha_Min"].notna()
    ].copy()
    calendar_base["Cosecha_Date"] = calendar_base["Cosecha_Min"].dt.date

    with c2:
        fincas = [t("all_f")] + [f for f in ["Moravia", "Frailes"] if f in set(calendar_base["Finca"].dropna().unique())]
        fincas += [f for f in sorted(calendar_base["Finca"].dropna().unique()) if f not in fincas]
        cal_finca = st.selectbox(t("farm"), fincas, key="cal_finca")
    if cal_finca != t("all_f"):
        calendar_base = calendar_base[calendar_base["Finca"] == cal_finca]

    with c3:
        camas = [t("all_f")] + sorted(calendar_base["Unidad"].dropna().unique())
        cal_cama = st.selectbox(t("bed"), camas, key="cal_cama")
    if cal_cama != t("all_f"):
        calendar_base = calendar_base[calendar_base["Unidad"] == cal_cama]

    with c4:
        only_soon = st.checkbox(t("only_next_15"), value=False, key="cal_only_soon")

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
            f'<div class="event-meta">{t("harvest_max")}: {fmt_date(row["Cosecha_Max"])}</div>'
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
                    events_html = f'<div class="no-events">{t("no_available_harvest")}</div>'
                html_block(
                    f'<div class="week-card"><div class="week-title">{t("week")} {int(week_num)}</div>'
                    f'<div class="week-range">{week_start.strftime("%d %b")} – {week_end.strftime("%d %b")}</div>'
                    f'{events_html}</div>'
                )

    if len(week_nums) == 0:
        msg = t("no_upcoming_15") if only_soon else t("no_min_month")
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
            <div class="tree-icon">{normalized_tree_icon(row)}</div>
            <div style="width:100%;">
                <div class="tree-name">{row['Arbol']}</div>
                <div class="tree-line">{t("phenology")} <span class="tree-pill {phen_class(row['Estado_Fenologico'])}">{tv(row['Estado_Fenologico'])}</span></div>
                <div class="tree-line">Trasplante <b>{row['Trasplante']}</b></div>
                <div class="tree-line">{t("health_status")} <span class="tree-pill {health_class(row['Estado_Sanitario'])}">● {tv(row['Estado_Sanitario'])}</span></div>
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
        finca_sel = st.selectbox(t("farm"), [t("all_f")] + [f for f in ["Moravia","Frailes"] if f in trees["Finca"].unique()], key="tree_finca")
    with c2:
        health_sel = st.selectbox(t("health_status"), [t("all_m")] + sorted(trees["Estado_Sanitario"].unique()), key="tree_health", format_func=tv)
    if finca_sel != t("all_f"):
        trees = trees[trees["Finca"] == finca_sel]
    if health_sel != t("all_m"):
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
        tipo_options = [t("all_m")] + sorted([x for x in events["Tipo_Evento"].dropna().unique() if x])
        tipo_sel = st.selectbox(t("event_type"), tipo_options, key="evt_tipo", format_func=tv)
    with c2:
        finca_options = [t("all_f")] + sorted([x for x in events["Finca"].dropna().unique() if x])
        finca_sel = st.selectbox(t("farm"), finca_options, key="evt_finca")
    with c3:
        estado_options = [t("all_m")] + sorted([x for x in events["Estado"].dropna().unique() if x])
        estado_sel = st.selectbox(t("event_status"), estado_options, key="evt_estado", format_func=tv)

    filtered_events = events.copy()
    if tipo_sel != t("all_m"):
        filtered_events = filtered_events[filtered_events["Tipo_Evento"] == tipo_sel]
    if finca_sel != t("all_f"):
        filtered_events = filtered_events[filtered_events["Finca"] == finca_sel]
    if estado_sel != t("all_m"):
        filtered_events = filtered_events[filtered_events["Estado"] == estado_sel]

    if filtered_events.empty:
        st.markdown(f'<div class="calendar-toolbar"><div class="calendar-note">{t("no_events_filters")}</div></div>', unsafe_allow_html=True)
    else:
        for tipo, group in filtered_events.groupby("Tipo_Evento", sort=False):
            st.markdown(f'<div class="event-section-title">{tv(tipo)}</div>', unsafe_allow_html=True)
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
                        fecha_txt = fmt_date(effective) if pd.notna(effective) else t("date_none")
                        insumo = row.get("Nombre_Insumo") or t("no_input")
                        target = row.get("Target_Label") or row.get("Target_ID")
                        html = f"""
                        <div class="ag-event-card">
                            <div class="ag-event-top">
                                <div>
                                    <div class="ag-event-title">{target}</div>
                                    <div class="ag-event-meta">{row.get("Finca", "")} · {row.get("Target_Tipo", "")}</div>
                                </div>
                                <span class="ag-event-pill {cls}">{tv(row.get("Estado", ""))}</span>
                            </div>
                            <div class="ag-event-meta"><b>{t("input")}:</b> {insumo}</div>
                            <div class="ag-event-meta"><b>{t("date")}:</b> {fecha_txt}</div>
                            <div class="ag-event-meta">{row.get("Notas", "")}</div>
                        </div>
                        """
                        st.markdown(html, unsafe_allow_html=True)

    with st.expander(t("input_catalog")):
        if insumos is None or insumos.empty:
            st.write(t("no_inputs"))
        else:
            for tipo, group in insumos.groupby("Tipo", sort=False):
                st.markdown(f"**{tipo}**")
                records = list(group.iterrows())
                for start in range(0, len(records), 3):
                    cols = st.columns(3)
                    for col, (_, row) in zip(cols, records[start:start+3]):
                        with col:
                            compra = t("purchase_required") if str(row.get("Compra_Requerida", "")).lower().startswith("s") else t("available_stock")
                            html = f"""
                            <div class="insumo-card">
                                <div class="insumo-name">{row.get("Nombre", "")}</div>
                                <div class="insumo-meta">{row.get("Uso_Principal", "")}</div>
                                <div class="insumo-meta"><b>{t("guide_qty")}:</b> {row.get("Cantidad_Guia", t("according_criteria"))}</div>
                                <div class="insumo-meta"><b>{t("timing")}:</b> {row.get("Momento_Aplicacion", t("according_state"))}</div>
                                <div class="insumo-meta"><b>{t("frequency")}:</b> {row.get("Frecuencia_Dias", "") if str(row.get("Frecuencia_Dias", "")).strip() else t("no_rule")} días</div>
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
    st.markdown(f"""
        </div>
        <div>
          <div style="font-size:26px;font-weight:800;line-height:1.1;">{t("account")}</div>
          <div style="opacity:.88;font-size:14px;margin-top:4px;">{t("account_profile")}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.15, 1])
    with c1:
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;margin-bottom:14px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">{t("user")}</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("name")}:</b> Pablo Castro</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("email")}:</b> {t("not_configured")}</div>
        </div>
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">{t("access_permissions")}</div>
          <div style="font-size:14px;color:#374151;">{t("access_future")}</div>
          <div style="display:inline-block;margin-top:10px;padding:6px 10px;border-radius:999px;background:#e5e7eb;color:#374151;font-size:12px;font-weight:700;">{t("future_work")}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;margin-bottom:14px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">{t("version")}</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("developer_version")}:</b> 22.0</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("date_label")}:</b> 2026-06-11</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("developed_with")}:</b> ChatGPT, Google Sheets, GitHub, Apps Script and Streamlit</div>
        </div>
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">{t("plugins")}</div>
          <div style="font-size:14px;color:#374151;">{t("plugins_text")}</div>
        </div>
        """, unsafe_allow_html=True)

df, units, trees, eventos, insumos, log_gpt = load_data()

with st.sidebar:
    lang_label = st.selectbox(
        t("language"),
        list(LANG_LABELS.keys()),
        index=list(LANG_LABELS.values()).index(st.session_state.get("lang", "es")),
        key="lang_selector",
    )
    st.session_state["lang"] = LANG_LABELS[lang_label]

st.markdown(f'<div class="app-title">{t("app_title")}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header(t("filters"))
    st.caption(t("data_source"))
    finca_options = [f for f in ["Moravia", "Frailes"] if f in set(units["Finca"].dropna().unique())] + [f for f in sorted(units["Finca"].dropna().unique()) if f not in ["Moravia", "Frailes"]]
    finca_filter = st.multiselect(t("farm"), finca_options, default=finca_options)
    unidad_options = sorted(units[units["Finca"].isin(finca_filter)]["Unidad"].dropna().unique()) if finca_filter else sorted(units["Unidad"].dropna().unique())
    unidad_filter = st.multiselect(t("bed"), unidad_options)
    cultivo_filter = st.multiselect(t("crop"), sorted(df["Cultivo"].dropna().unique()))
    estado_options = sorted(set(list(df["Visual_Status"].dropna().unique()) + ["No activa"]))
    estado_filter = st.multiselect(t("visual_status"), estado_options, format_func=tv)
    show_detail_table = st.checkbox(t("show_detail_table"), value=False)

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

tab_dashboard, tab_camas, tab_arboles, tab_eventos, tab_calendario, tab_clima, tab_avance, tab_cuenta = st.tabs([f"📊 {t('dashboard')}", f"🛏️ {t('beds')}", f"🌳 {t('trees')}", f"🧪 {t('events')}", f"📅 {t('calendar')}", f"☁️ {t('climate')}", f"📷 {t('progress')}", f"👤 {t('account')}"] )

with tab_dashboard:
    render_dashboard_view(filtered, filtered_units, eventos, trees, log_gpt)

with tab_camas:
    finca_order = ["Frailes", "Moravia"] + [f for f in filtered_units["Finca"].dropna().unique() if f not in ["Frailes", "Moravia"]]
    for finca in finca_order:
        unit_group = filtered_units[filtered_units["Finca"] == finca]
        if unit_group.empty:
            continue
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

with tab_clima:
    render_weather_view()

with tab_avance:
    render_progress_view()

with tab_cuenta:
    render_account_view()

if show_detail_table:
    st.divider()
    st.subheader(t("detail_title"))
    show_cols = [
        "Finca", "Unidad", "Cultivo", "Cantidad", "Estado_Actual",
        "Fecha_Siembra", "Fecha_Trasplante", "Cosecha_Min", "Cosecha_Max", "Visual_Status"
    ]
    table = filtered[show_cols].copy().sort_values(["Finca", "Unidad", "Cultivo"])
    st.dataframe(table, use_container_width=True, hide_index=True)
