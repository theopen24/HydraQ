from pathlib import Path
from datetime import date, datetime, timedelta
import calendar
import html
import re
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
    "Vainica": {"icon": "🌱", "class": "basil"},
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
        "event_status": "Estado del evento",
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
        "camera_note": "Recomendación: tomar fotos desde el mismo ángulo, misma cama y mismo periodo mensual.",
        "rain_reference": "Referencia climática",
        "rain_reference_text": "Lluvia semanal: baja < 10 mm, media 10–40 mm, alta > 40 mm. Poco sol: menos de 21 h por semana o menos de 3 h promedio por día.",
        "bed_photo_pending": "Foto pendiente",
        "same_frame": "Encuadre estándar",
        "bed_visual_reference": "Referencia visual reducida",
        "history": "Historial",
        "no_history": "Sin historial registrado",
        "app_reboot_note": "Si no actualiza, usar Manage app → Reboot app."
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
        "event_status": "Event status",
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
        "camera_note": "Recommendation: take photos from the same angle, same bed and same monthly period.",
        "rain_reference": "Climate reference",
        "rain_reference_text": "Weekly rain: low < 10 mm, medium 10–40 mm, high > 40 mm. Low sun: less than 21 h per week or less than 3 h average per day.",
        "bed_photo_pending": "Photo pending",
        "same_frame": "Standard frame",
        "bed_visual_reference": "Reduced visual reference",
        "history": "History",
        "no_history": "No history recorded",
        "app_reboot_note": "If it does not update, use Manage app → Reboot app."
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
.harvest-qty {font-weight:950; color:#14532d;}
.harvest-summary {background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:14px;margin:10px 0 16px;}
.harvest-summary-title {font-size:16px;font-weight:900;color:#0f3d25;margin-bottom:8px;}
.harvest-chip {display:inline-block;background:#ecfdf5;color:#166534;border:1px solid #bbf7d0;border-radius:999px;padding:6px 10px;margin:4px;font-size:12px;font-weight:800;}
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

.bed-thumb-wrap {display:flex; align-items:center; gap:10px; margin:4px 0 10px 0;}
.bed-thumb {width:20%; max-width:145px; min-width:92px; height:78px; object-fit:cover; border-radius:12px; border:1px solid rgba(255,255,255,.58); box-shadow:0 4px 12px rgba(0,0,0,.18);}
.bed-thumb-placeholder {width:20%; max-width:145px; min-width:92px; height:78px; border-radius:12px; border:1px dashed rgba(255,255,255,.58); display:flex; align-items:center; justify-content:center; color:#d1fae5; font-size:24px; background:rgba(255,255,255,.08);}
.bed-thumb-text {font-size:12px; color:#d1fae5; font-weight:800;}
.history-table {width:100%; border-collapse:collapse; margin-top:8px; font-size:11px; overflow:hidden; border-radius:10px;}
.history-table th {background:#ecfdf5; color:#166534; text-align:left; padding:5px 6px; font-weight:950;}
.history-table td {border-top:1px solid #d1fae5; padding:5px 6px; color:#334155; font-weight:750; vertical-align:top;}
.history-table .datecol {white-space:nowrap; color:#0f3d25; font-weight:950;}
.progress-grid {display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:14px;}
.progress-card {background:rgba(255,255,255,.95); border:1px solid rgba(255,255,255,.72); border-radius:16px; padding:10px; box-shadow:0 6px 16px rgba(0,0,0,.14); color:#0f172a;}
.progress-frame {width:100%; aspect-ratio:4 / 3; border-radius:12px; overflow:hidden; background:#e5e7eb; border:1px solid #dbe7de; display:flex; align-items:center; justify-content:center; color:#64748b; font-weight:950;}
.progress-frame img {width:100%; height:100%; object-fit:cover; display:block;}
.progress-title {font-size:14px; font-weight:950; color:#0f3d25; margin-top:8px;}
.progress-meta {font-size:12px; color:#64748b; font-weight:750;}
.weather-reference {background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:10px 12px; color:#7c2d12; font-weight:800; margin:8px 0 12px 0;}


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


def build_cultivos_view(siembras, fincas, unidades, cultivos):
    """Construye la vista operativa desde CultivosSembrados.

    Regla V27:
    - CultivosSembrados es la fuente de verdad.
    - VistaCultivos queda como vista auxiliar/compatibilidad, no como origen principal.
    - Esto permite que los cambios hechos por GPT/Apps Script se reflejen en la app.
    """
    base = siembras.copy()
    if base.empty:
        return pd.DataFrame(columns=[
            "Siembra_ID", "Finca", "Finca_ID", "Unidad", "Unidad_ID", "Estado_Unidad",
            "Cultivo", "Cultivo_ID", "Cantidad", "Estado_Actual", "Fecha_Siembra",
            "Fecha_Trasplante", "Fecha_Base", "Cosecha_Min", "Cosecha_Max",
            "Alerta_Datos", "Mes_Cosecha", "Evento_Agricola"
        ])

    view = base.merge(fincas, on="Finca_ID", how="left")
    view = view.merge(unidades, on=["Unidad_ID", "Finca_ID"], how="left", suffixes=("", "_Unidad"))
    view = view.merge(cultivos, on="Cultivo_ID", how="left")

    if "Finca" not in view.columns:
        view["Finca"] = view.get("Finca_Nombre", "")
    if "Unidad" not in view.columns:
        view["Unidad"] = view.get("Unidad_Nombre", "")
    if "Cultivo" not in view.columns:
        view["Cultivo"] = view.get("Cultivo_Nombre", "")
    if "Estado_Unidad" not in view.columns:
        view["Estado_Unidad"] = view.get("Estado", "Activa")
    if "Alerta_Datos" not in view.columns:
        view["Alerta_Datos"] = view.get("Estado_Ficha", "")

    if "Mes_Cosecha" not in view.columns:
        cm = pd.to_datetime(view.get("Cosecha_Min"), errors="coerce")
        view["Mes_Cosecha"] = cm.dt.strftime("%Y-%m").fillna("Sin fecha")

    for col in ["Evento_Agricola", "Notas"]:
        if col not in view.columns:
            view[col] = ""

    preferred = [
        "Siembra_ID", "Finca", "Finca_ID", "Unidad", "Unidad_ID", "Estado_Unidad",
        "Cultivo", "Cultivo_ID", "Cantidad", "Estado_Actual", "Fecha_Siembra",
        "Fecha_Trasplante", "Fecha_Base", "Cosecha_Min", "Cosecha_Max",
        "Alerta_Datos", "Mes_Cosecha", "Evento_Agricola"
    ]
    for col in preferred:
        if col not in view.columns:
            view[col] = ""
    return view[preferred]


@st.cache_data(ttl=120, show_spinner="Cargando datos desde Google Sheets...")
def load_data():
    fincas = _read_sheet("Fincas")
    unidades = _read_sheet("Unidades")
    cultivos = _read_sheet("CatalogoCultivos")
    siembras = _read_sheet("CultivosSembrados")

    # V27: la app deja de depender de VistaCultivos como fuente principal.
    # VistaCultivos puede existir, pero la visualización se arma desde CultivosSembrados.
    df = build_cultivos_view(siembras, fincas, unidades, cultivos)

    arboles = _read_sheet("Arboles", ["Arbol_ID","Finca","Arbol","Icono","Estado_Fenologico","Trasplante","Estado_Sanitario","Evento_Agricola"])
    if arboles.empty:
        arboles = pd.DataFrame(TREE_DATA)

    eventos = _read_sheet(
        "EventosAgricolas",
        ["ID_Evento","Tipo_Evento","ID_Insumo","Nombre_Insumo","Target_Tipo","Target_ID",
         "Target_Label","Finca","Unidad","Cultivo","Arbol","Fecha_Programada",
         "Fecha_Realizada","Estado","Notas",
         "Cantidad","Unidad_Medida","Cantidad_Normalizada","Unidad_Normalizada",
         "Tipo_Cosecha","Destino","Afecta_Inventario","Notas_Cosecha"]
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
    text_cols = ["Tipo_Evento", "Nombre_Insumo", "Target_Tipo", "Target_ID", "Target_Label", "Finca", "Unidad", "Cultivo", "Arbol", "Estado", "Notas", "Unidad_Medida", "Unidad_Normalizada", "Tipo_Cosecha", "Destino", "Afecta_Inventario", "Notas_Cosecha"]
    for col in text_cols:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("").astype(str)
    for col in ["Cantidad", "Cantidad_Normalizada"]:
        if col not in out.columns:
            out[col] = pd.NA
        out[col] = pd.to_numeric(out[col], errors="coerce")
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
    # Soporte flexible para GitHub: funciona si las fotos están en /assets
    # o si fueron subidas directamente a la raíz del repo.
    candidates = [
        ASSETS_DIR / name,
        BASE_DIR / name,
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


def img_data_uri(name):
    import base64, mimetypes
    path = asset_path(name)
    if not path:
        return None
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    data = Path(path).read_bytes()
    return f"data:{mime};base64," + base64.b64encode(data).decode("utf-8")


def bed_photo_for(unit_name):
    """Foto local de referencia para cada cama.
    Junio 2026 reemplaza las fotos de muestra anteriores.
    """
    import re
    u = str(unit_name or "").lower()
    photo_map = {
        "1": (None, "Pendiente"),
        "2": ("cama_2_junio.jpeg", "Junio 2026"),
        "3": ("cama_3_junio.jpeg", "Junio 2026"),
        "4": ("cama_4_junio.jpeg", "Junio 2026"),
        "5": ("cama_5_junio.jpeg", "Junio 2026"),
        "6": ("cama_6_junio.jpeg", "Junio 2026"),
        "7": ("cama_7_junio.jpeg", "Junio 2026"),
    }
    match = re.search(r"(\d+)", u)
    bed_num = match.group(1) if match else None
    img, caption = photo_map.get(bed_num, (None, "Referencia visual pendiente"))
    return asset_path(img) if img else None, caption

def normalized_tree_icon(row):
    name = str(row.get("Arbol", "")).lower()
    icon = str(row.get("Icono", "") or "🌳")
    if "limón mandarina" in name or "limon mandarina" in name:
        return "🍋"
    if "🍋" in icon and "🍊" in icon:
        return "🍋"
    return icon


def event_effective_date(row):
    """Fecha principal del evento.
    - Cosecha siempre usa Fecha_Realizada porque es registro histórico/productivo.
    - Completado usa Fecha_Realizada.
    - Programado / No empezado usa Fecha_Programada.
    """
    tipo = str(row.get("Tipo_Evento", "")).strip().lower()
    estado = str(row.get("Estado", "")).strip().lower()
    realizada = row.get("Fecha_Realizada")
    programada = row.get("Fecha_Programada")

    if "cosecha" in tipo:
        return realizada if pd.notna(realizada) else programada
    if "complet" in estado:
        return realizada if pd.notna(realizada) else programada
    return programada if pd.notna(programada) else realizada

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

def history_table_html(events, target_id, limit=5):
    subset = completed_events_for_target(events, target_id)
    if subset.empty:
        return f'<div class="history-line"><b>{t("history")}:</b> {t("no_history")}</div>'
    subset = subset.sort_values("_date", ascending=True).tail(limit)
    rows = []
    for _, r in subset.iterrows():
        fecha = pd.to_datetime(r.get("_date")).strftime("%d/%m/%Y") if pd.notna(r.get("_date")) else ""
        evento = tv(r.get("Tipo_Evento", ""))
        insumo = r.get("Nombre_Insumo", "") or t("no_input")
        rows.append(f'<tr><td class="datecol">{fecha}</td><td>{evento}</td><td>{insumo}</td></tr>')
    return f'<table class="history-table"><thead><tr><th>{t("date")}</th><th>{t("event_type")}</th><th>{t("input")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'


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
    c1, c2, c3 = st.columns([1, 1, 1.6])
    with c1:
        st.radio(t("period"), [t("weekly"), t("monthly")], index=0, horizontal=True, key="weather_period")
    with c2:
        finca = st.radio(t("farm"), ["Frailes", "Moravia"], index=0, horizontal=True, key="weather_farm")
    with c3:
        st.selectbox(t("week"), ["12 – 18 mayo 2025", "19 – 25 mayo 2025", "26 mayo – 1 junio 2025"], key="weather_week")

    html_block(f'<div class="weather-reference"><b>{t("rain_reference")}:</b> {t("rain_reference_text")}</div>')

    mock = {
        "Moravia": {"rain": 28.4, "sun": 32.1, "days": 3, "temp": 24.3},
        "Frailes": {"rain": 68.7, "sun": 18.6, "days": 5, "temp": 22.1},
    }
    cols = st.columns(4)
    metrics = [
        ("🌧️", t("rain_7_days"), "rain", "mm"),
        ("☀️", t("sun_hours"), "sun", "h"),
        ("☔", t("rainy_days"), "days", ""),
        ("🌡️", t("avg_temp"), "temp", "°C"),
    ]
    for col, (icon, label, key, suffix) in zip(cols, metrics):
        with col:
            value = mock[finca][key]
            html_block(f'<div class="weather-card"><div class="weather-title">{icon} {label}</div><div class="weather-value">{value}{suffix}</div><div class="weather-note">{finca}</div></div>')

    days_by_farm = {
        "Frailes": [("LUN 12", "🌧️", "14.8 mm", "1.7 h", "lluvia alta"), ("MAR 13", "🌧️", "8.4 mm", "2.1 h", "lluvia media"), ("MIÉ 14", "🌧️", "18.2 mm", "1.2 h", "lluvia alta"), ("JUE 15", "🌧️", "11.6 mm", "1.6 h", "lluvia alta"), ("VIE 16", "🌦️", "7.5 mm", "2.8 h", "lluvia media"), ("SÁB 17", "🌤️", "2.2 mm", "4.5 h", "parcial"), ("DOM 18", "🌧️", "6.0 mm", "4.7 h", "lluvia media")],
        "Moravia": [("LUN 12", "🌧️", "6.8 mm", "2.1 h", "lluvia media"), ("MAR 13", "🌤️", "1.2 mm", "6.3 h", "nublado parcial"), ("MIÉ 14", "🌤️", "0.0 mm", "5.8 h", "soleado"), ("JUE 15", "🌧️", "12.6 mm", "1.4 h", "lluvia alta"), ("VIE 16", "🌧️", "6.3 mm", "2.0 h", "lluvia media"), ("SÁB 17", "☀️", "0.0 mm", "8.2 h", "soleado"), ("DOM 18", "🌤️", "1.5 mm", "6.3 h", "nublado parcial")],
    }

    st.markdown(f"### {t('current_week')} · {finca}")
    dcols = st.columns(7)
    for c, d in zip(dcols, days_by_farm[finca]):
        with c:
            html_block(f'<div class="weather-day"><b>{d[0]}</b><div class="weather-icon">{d[1]}</div><div>{d[2]}</div><div>{d[3]}</div><small>{d[4]}</small></div>')

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(f"### {t('monthly_summary')}")
        chart_data = pd.DataFrame({"Moravia": [24, 13, 37, 18, 28], "Frailes": [54, 31, 82, 45, 69]}, index=["14-20 abr", "21-27 abr", "28 abr-4 may", "5-11 may", "12-18 may"])
        st.bar_chart(chart_data[[finca]])
    with right:
        st.markdown(f"### {t('weekly_recommendation')}")
        if finca == "Frailes":
            recos = ["Postergar abono foliar por lluvia acumulada alta.", "Vigilar hongos por varios días húmedos.", "Revisar drenaje y evitar riego adicional."]
        else:
            recos = ["Ventana favorable para control fitosanitario si hay 24h sin lluvia.", "Revisar riego solo si baja la humedad del sustrato.", "Buen periodo para observación sanitaria."]
        for r in recos:
            html_block(f'<div class="reco-card">{r}</div>')
    html_block(f'<div class="dash-panel"><div class="dash-line"><b>{t("sample_data")}.</b> {t("future_integration")}.</div></div>')


def render_progress_view():
    st.markdown(f'<div class="section-title">📷 {t("progress")}</div>', unsafe_allow_html=True)
    html_block(f'<div class="dash-panel"><div class="dash-panel-title">{t("photo_progress")}</div><div class="dash-line">{t("photo_progress_help")}</div><div class="dash-line"><span class="dash-pill pill-blue">Tip</span> {t("camera_note")}</div></div>')

    # Vista tipo calendario: meses como filas, camas como columnas.
    beds = [f"Cama {i}" for i in range(1, 8)]
    months = ["Junio 2026"]
    photo_map = {
        ("Junio 2026", "Cama 1"): None,
        ("Junio 2026", "Cama 2"): "cama_2_junio.jpeg",
        ("Junio 2026", "Cama 3"): "cama_3_junio.jpeg",
        ("Junio 2026", "Cama 4"): "cama_4_junio.jpeg",
        ("Junio 2026", "Cama 5"): "cama_5_junio.jpeg",
        ("Junio 2026", "Cama 6"): "cama_6_junio.jpeg",
        ("Junio 2026", "Cama 7"): "cama_7_junio.jpeg",
    }

    st.markdown("### 📅 Avance mensual por cama")
    header_cols = st.columns([0.85] + [1]*len(beds))
    header_cols[0].markdown("**Mes**")
    for col, bed in zip(header_cols[1:], beds):
        col.markdown(f"**{bed}**")

    for month in months:
        row_cols = st.columns([0.85] + [1]*len(beds))
        row_cols[0].markdown(f"**{month}**")
        for col, bed in zip(row_cols[1:], beds):
            img = photo_map.get((month, bed))
            if img and asset_path(img):
                with col:
                    st.image(asset_path(img), caption="Foto registrada", use_container_width=True)
                    with st.expander("🔎 Ampliar", expanded=False):
                        st.image(asset_path(img), caption=f"{bed} · {month}", use_container_width=True)
            else:
                col.markdown('<div style="background:#ffffff;border-radius:14px;padding:18px;text-align:center;color:#64748b;font-weight:800;">📷<br>Pendiente</div>', unsafe_allow_html=True)

    st.markdown("### Carga de nuevas fotos")
    uploaded = st.file_uploader(t("upload_new_photo"), type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded:
        st.write(f"{len(uploaded)} archivo(s) cargado(s) para vista previa. Persistencia real pendiente de integrar con Drive.")
        cols = st.columns(3)
        for col, file in zip(cols, uploaded[:3]):
            with col:
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
            with st.expander("🔎 Ver foto grande", expanded=False):
                st.image(str(photo_path), caption=f"{unidad} · {photo_caption}", use_container_width=True)
        else:
            st.markdown(f'<div class="bed-thumb-wrap"><div class="bed-thumb-placeholder">📷</div><div class="bed-thumb-text">{t("bed_photo_pending")}</div></div>', unsafe_allow_html=True)
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

def month_calendar_weeks(year, month):
    # Weeks are always Monday to Sunday. The first week shown for a month
    # starts on the Monday that contains day 1 of that month.
    first = date(year, month, 1)
    last = date(year, month, calendar.monthrange(year, month)[1])
    start = first - timedelta(days=first.weekday())
    end = last + timedelta(days=(6 - last.weekday()))
    weeks = []
    cur = start
    while cur <= end:
        weeks.append((cur, cur + timedelta(days=6)))
        cur += timedelta(days=7)
    return weeks


def week_number_for_month(year, month, week_start):
    first_week_start = date(year, month, 1) - timedelta(days=date(year, month, 1).weekday())
    return ((week_start - first_week_start).days // 7) + 1


def week_start_for_date(d):
    return d - timedelta(days=d.weekday())

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

    weeks = month_calendar_weeks(selected_year, selected_month)
    if not calendar_df.empty:
        calendar_df["Week_Start"] = calendar_df["Cosecha_Date"].apply(week_start_for_date)

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


    any_events = False
    for start in range(0, len(weeks), 4):
        cols = st.columns(4)
        for col, (week_start, week_end) in zip(cols, weeks[start:start + 4]):
            with col:
                if calendar_df.empty:
                    events = calendar_df
                else:
                    events = calendar_df[calendar_df["Week_Start"] == week_start].sort_values(["Cosecha_Min", "Finca", "Unidad", "Cultivo"])
                if not events.empty:
                    any_events = True
                events_html = "".join(build_event_html(row) for _, row in events.iterrows())
                if not events_html:
                    events_html = f'<div class="no-events">{t("no_available_harvest")}</div>'
                week_num = week_number_for_month(selected_year, selected_month, week_start)
                html_block(
                    f'<div class="week-card"><div class="week-title">{t("week")} {int(week_num)}</div>'
                    f'<div class="week-range">{week_start.strftime("%d %b %Y")} – {week_end.strftime("%d %b %Y")}</div>'
                    f'{events_html}</div>'
                )

    if not any_events:
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
    target_id = row.get("Arbol_ID")
    control = latest_control_status(events, target_id)
    hist = completed_events_for_target(events, target_id).copy()
    if hist.empty:
        hist_html = f'<div class="tree-line">{t("no_history")}</div>'
    else:
        hist["_date"] = hist.apply(event_effective_date, axis=1)
        hist = hist.sort_values("_date", ascending=False).head(5)
        rows = []
        for _, ev in hist.iterrows():
            rows.append(
                "<tr>"
                f"<td>{fmt_date(ev.get('_date')) if pd.notna(ev.get('_date')) else t('date_none')}</td>"
                f"<td>{clean_text_for_html(ev.get('Tipo_Evento', ''))}</td>"
                f"<td>{clean_text_for_html(ev.get('Nombre_Insumo', ''))}</td>"
                f"<td>{clean_text_for_html(ev.get('Estado', ''))}</td>"
                "</tr>"
            )
        hist_html = '<table class="tree-history-table"><thead><tr><th>Fecha</th><th>Evento</th><th>Insumo</th><th>Estado</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'

    control_txt = "Sin control registrado"
    if control:
        control_txt = f"{fmt_date(control.get('date')) if control.get('date') is not None and pd.notna(control.get('date')) else t('date_none')} · {clean_text_for_html(control.get('insumo', ''))}"

    next_abono = next_soil_abono_html(events, insumos, target_id, row.get("Estado_Fenologico", ""))

    st.markdown(f"""
    <div class="tree-card tree-card-wide">
        <div class="tree-name">{normalized_tree_icon(row)} {clean_text_for_html(row.get('Arbol', ''))}</div>
        <div class="tree-3blocks">
            <div class="tree-block">
                <div class="tree-block-title">1. Identificación</div>
                <div class="tree-line"><b>Finca:</b> {clean_text_for_html(row.get('Finca', ''))}</div>
                <div class="tree-line"><b>Trasplante:</b> {clean_text_for_html(row.get('Trasplante', ''))}</div>
                <div class="tree-line"><b>{t('phenology')}:</b> <span class="tree-pill {phen_class(row.get('Estado_Fenologico', ''))}">{tv(row.get('Estado_Fenologico', ''))}</span></div>
            </div>
            <div class="tree-block">
                <div class="tree-block-title">2. Estado y próxima acción</div>
                <div class="tree-line"><b>{t('health_status')}:</b> <span class="tree-pill {health_class(row.get('Estado_Sanitario', ''))}">● {tv(row.get('Estado_Sanitario', ''))}</span></div>
                <div class="tree-line"><b>{t('last_control')}:</b> {control_txt}</div>
                <div class="tree-line">{next_abono}</div>
            </div>
            <div class="tree-block">
                <div class="tree-block-title">3. Historial de eventos</div>
                {hist_html}
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
        for _, row in group.iterrows():
            render_tree_card(row, events, insumos)

def fmt_number(value):
    if value is None or pd.isna(value):
        return ""
    try:
        num = float(value)
    except Exception:
        txt = str(value).strip()
        return "" if txt.lower() in ["", "nan", "none"] else txt
    if abs(num - int(num)) < 0.000001:
        return str(int(num))
    return f"{num:.2f}".rstrip("0").rstrip(".")


def clean_text_for_html(value):
    txt = str(value or "").strip()
    if not txt or txt.lower() == "nan":
        return ""
    # Evita que HTML accidental guardado en Sheets se muestre como código en tarjetas.
    txt = re.sub(r"<[^>]+>", "", txt)
    return html.escape(txt)


def harvest_quantity_html(row):
    cantidad = row.get("Cantidad")
    unidad = clean_text_for_html(row.get("Unidad_Medida", ""))
    normal = row.get("Cantidad_Normalizada")
    unidad_norm = clean_text_for_html(row.get("Unidad_Normalizada", ""))
    destino = clean_text_for_html(row.get("Destino", ""))
    notas_cosecha = clean_text_for_html(row.get("Notas_Cosecha", ""))

    pieces = []
    c = fmt_number(cantidad)
    if c:
        pieces.append(f'<b>Cantidad:</b> <span class="harvest-qty">{c} {unidad}</span>')
    n = fmt_number(normal)
    if n and unidad_norm:
        pieces.append(f'<b>Normalizado:</b> {n} {unidad_norm}')
    if destino:
        pieces.append(f'<b>Destino:</b> {destino}')
    if notas_cosecha:
        pieces.append(notas_cosecha)
    if not pieces:
        return ""
    return '<div class="ag-event-meta">' + '<br>'.join(pieces) + '</div>'


def prepare_harvest_data(events):
    if events is None or events.empty or "Tipo_Evento" not in events.columns:
        return pd.DataFrame()
    cosechas = events[events["Tipo_Evento"].astype(str).str.lower().str.contains("cosecha", na=False)].copy()
    if cosechas.empty:
        return cosechas
    cosechas["_date"] = cosechas.apply(event_effective_date, axis=1)
    cosechas["Fecha"] = pd.to_datetime(cosechas["_date"], errors="coerce")
    cosechas["Mes"] = cosechas["Fecha"].dt.strftime("%Y-%m").fillna("Sin fecha")
    cosechas["Temporada"] = cosechas["Fecha"].dt.to_period("Q").astype(str).replace("NaT", "Sin fecha")
    target_fallback = cosechas["Target_Label"].replace("", pd.NA) if "Target_Label" in cosechas.columns else pd.Series(pd.NA, index=cosechas.index)
    cosechas["Cultivo_Base"] = cosechas["Cultivo"].replace("", pd.NA).fillna(target_fallback).fillna("Sin cultivo")
    return cosechas


def render_cosechas_report(events):
    st.markdown('<div class="section-title">📦 Resumen de Cosechas</div>', unsafe_allow_html=True)
    cosechas = prepare_harvest_data(events)
    if cosechas.empty:
        st.info("Todavía no hay eventos de cosecha registrados.")
        return

    valid = cosechas[cosechas["Cantidad_Normalizada"].notna() & (cosechas["Unidad_Normalizada"].astype(str).str.strip() != "")].copy()
    if valid.empty:
        st.info("Hay cosechas registradas, pero todavía no tienen cantidad normalizada para reportes.")
        st.dataframe(cosechas, use_container_width=True, hide_index=True)
        return

    kg_total = valid[valid["Unidad_Normalizada"].str.lower().eq("kg")]["Cantidad_Normalizada"].sum()
    unit_total = valid[valid["Unidad_Normalizada"].str.lower().str.contains("unidad", na=False)]["Cantidad_Normalizada"].sum()
    especies = valid["Cultivo_Base"].nunique()
    product = (
        valid.groupby("Cultivo_Base")["Cantidad_Normalizada"].sum().sort_values(ascending=False)
    )
    top_product = product.index[0] if not product.empty else "Sin datos"

    dashboard_metric_cards([
        ("Total kg", f"{fmt_number(kg_total)} kg", "gramos y kilos normalizados"),
        ("Total unidades", fmt_number(unit_total), "matas/frutos/unidades"),
        ("Especies", especies, "cultivos o árboles cosechados"),
        ("Más cosechado", top_product, "por cantidad normalizada"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Por finca")
        by_farm = valid.groupby(["Finca", "Unidad_Normalizada"], dropna=False)["Cantidad_Normalizada"].sum().reset_index()
        for unit in by_farm["Unidad_Normalizada"].dropna().unique():
            chart = by_farm[by_farm["Unidad_Normalizada"] == unit].set_index("Finca")[["Cantidad_Normalizada"]]
            st.caption(f"Unidad: {unit}")
            st.bar_chart(chart)
    with c2:
        st.markdown("### Por especie")
        by_crop = valid.groupby(["Cultivo_Base", "Unidad_Normalizada"], dropna=False)["Cantidad_Normalizada"].sum().reset_index()
        for unit in by_crop["Unidad_Normalizada"].dropna().unique():
            chart = by_crop[by_crop["Unidad_Normalizada"] == unit].sort_values("Cantidad_Normalizada", ascending=False).head(12).set_index("Cultivo_Base")[["Cantidad_Normalizada"]]
            st.caption(f"Unidad: {unit}")
            st.bar_chart(chart)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("### Por mes")
        by_month = valid.groupby(["Mes", "Unidad_Normalizada"], dropna=False)["Cantidad_Normalizada"].sum().reset_index()
        for unit in by_month["Unidad_Normalizada"].dropna().unique():
            chart = by_month[by_month["Unidad_Normalizada"] == unit].set_index("Mes")[["Cantidad_Normalizada"]]
            st.caption(f"Unidad: {unit}")
            st.line_chart(chart)
    with c4:
        st.markdown("### Por temporada")
        by_season = valid.groupby(["Temporada", "Unidad_Normalizada"], dropna=False)["Cantidad_Normalizada"].sum().reset_index()
        for unit in by_season["Unidad_Normalizada"].dropna().unique():
            chart = by_season[by_season["Unidad_Normalizada"] == unit].set_index("Temporada")[["Cantidad_Normalizada"]]
            st.caption(f"Unidad: {unit}")
            st.bar_chart(chart)

    st.markdown("### Detalle de cosechas")
    cols = [c for c in ["Fecha", "Finca", "Unidad", "Cultivo_Base", "Cantidad", "Unidad_Medida", "Cantidad_Normalizada", "Unidad_Normalizada", "Destino", "Notas_Cosecha"] if c in valid.columns]
    table = valid[cols].copy().sort_values("Fecha", ascending=False)
    if "Fecha" in table.columns:
        table["Fecha"] = pd.to_datetime(table["Fecha"], errors="coerce").dt.strftime("%d/%m/%Y")
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_eventos_view(events, insumos=None):
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
        return

    filtered_events = filtered_events.copy()
    filtered_events["_date"] = filtered_events.apply(event_effective_date, axis=1)
    filtered_events = filtered_events.sort_values("_date", ascending=False, na_position="last")

    st.markdown("### Tabla de eventos")
    page_size = 50
    max_page = max(0, (len(filtered_events) - 1) // page_size)
    page_key = "events_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    st.session_state[page_key] = min(st.session_state[page_key], max_page)
    b1, b2, b3 = st.columns([1, 1, 4])
    with b1:
        if st.button("◀ Previous", disabled=st.session_state[page_key] == 0):
            st.session_state[page_key] -= 1
    with b2:
        if st.button("Next ▶", disabled=st.session_state[page_key] >= max_page):
            st.session_state[page_key] += 1
    b3.caption(f"Página {st.session_state[page_key]+1} de {max_page+1} · {len(filtered_events)} eventos")

    start = st.session_state[page_key] * page_size
    page = filtered_events.iloc[start:start+page_size].copy()
    display_cols = [c for c in ["ID_Evento", "Tipo_Evento", "Finca", "Target_Tipo", "Target_Label", "Cultivo", "Nombre_Insumo", "Estado", "Fecha_Programada", "Fecha_Realizada", "Cantidad", "Unidad_Medida", "Cantidad_Normalizada", "Unidad_Normalizada", "Notas"] if c in page.columns]
    table = page[display_cols].copy()
    for col in ["Fecha_Programada", "Fecha_Realizada"]:
        if col in table.columns:
            table[col] = pd.to_datetime(table[col], errors="coerce").dt.strftime("%d/%m/%Y").fillna("")
    st.dataframe(table, use_container_width=True, hide_index=True, height=540)

    with st.expander("Tarjetas visuales por tipo de evento", expanded=False):
        for tipo, group in filtered_events.groupby("Tipo_Evento", sort=False):
            st.markdown(f'<div class="event-section-title">{tv(tipo)}</div>', unsafe_allow_html=True)
            records = list(group.iterrows())
            for start in range(0, len(records), 3):
                cols = st.columns(3)
                for col, (_, row) in zip(cols, records[start:start+3]):
                    with col:
                        effective = row.get("_date")
                        cls = event_status_class(row.get("Estado"), effective)
                        fecha_label = "Cosecha" if "cosecha" in str(row.get("Tipo_Evento", "")).lower() else t("date")
                        fecha_txt = fmt_date(effective) if pd.notna(effective) else t("date_none")
                        insumo = clean_text_for_html(row.get("Nombre_Insumo")) or t("no_input")
                        target = clean_text_for_html(row.get("Target_Label")) or clean_text_for_html(row.get("Target_ID"))
                        qty_html = harvest_quantity_html(row) if "cosecha" in str(row.get("Tipo_Evento", "")).lower() else ""
                        html_card = f"""
                        <div class="ag-event-card">
                            <div class="ag-event-top">
                                <div>
                                    <div class="ag-event-title">{target}</div>
                                    <div class="ag-event-meta">{clean_text_for_html(row.get("Finca", ""))} · {clean_text_for_html(row.get("Target_Tipo", ""))}</div>
                                </div>
                                <span class="ag-event-pill {cls}">{tv(row.get("Estado", ""))}</span>
                            </div>
                            <div class="ag-event-meta"><b>{t("input")}:</b> {insumo}</div>
                            <div class="ag-event-meta"><b>{fecha_label}:</b> {fecha_txt}</div>
                            {qty_html}
                            <div class="ag-event-meta">{clean_text_for_html(row.get("Notas", ""))}</div>
                        </div>
                        """
                        st.markdown(html_card, unsafe_allow_html=True)


def render_insumos_view(insumos):
    st.markdown(f'<div class="section-title">🧴 {t("input_catalog")}</div>', unsafe_allow_html=True)
    if insumos is None or insumos.empty:
        st.write(t("no_inputs"))
        return
    tipo_options = [t("all_m")] + sorted([x for x in insumos["Tipo"].dropna().unique() if x]) if "Tipo" in insumos.columns else [t("all_m")]
    tipo_sel = st.selectbox("Tipo", tipo_options, key="insumo_tipo")
    view = insumos.copy()
    if tipo_sel != t("all_m") and "Tipo" in view.columns:
        view = view[view["Tipo"] == tipo_sel]
    for tipo, group in view.groupby("Tipo", sort=False):
        st.markdown(f"### {tipo}")
        records = list(group.iterrows())
        for start in range(0, len(records), 3):
            cols = st.columns(3)
            for col, (_, row) in zip(cols, records[start:start+3]):
                with col:
                    compra = t("purchase_required") if str(row.get("Compra_Requerida", "")).lower().startswith("s") else t("available_stock")
                    html_card = f"""
                    <div class="insumo-card">
                        <div class="insumo-name">{clean_text_for_html(row.get("Nombre", ""))}</div>
                        <div class="insumo-meta">{clean_text_for_html(row.get("Uso_Principal", ""))}</div>
                        <div class="insumo-meta"><b>{t("guide_qty")}:</b> {clean_text_for_html(row.get("Cantidad_Guia", t("according_criteria")))}</div>
                        <div class="insumo-meta"><b>{t("timing")}:</b> {clean_text_for_html(row.get("Momento_Aplicacion", t("according_state")))}</div>
                        <div class="insumo-meta"><b>{t("frequency")}:</b> {clean_text_for_html(row.get("Frecuencia_Dias", "")) if str(row.get("Frecuencia_Dias", "")).strip() else t("no_rule")} días</div>
                        <div class="insumo-meta"><b>{compra}</b></div>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)
    with st.expander("Ver tabla completa", expanded=False):
        st.dataframe(view, use_container_width=True, hide_index=True)

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
          <div style="font-size:15px;color:#1f2937;"><b>{t("developer_version")}:</b> 27.0</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("date_label")}:</b> 2026-06-29</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("developed_with")}:</b> ChatGPT, Google Sheets, GitHub, Apps Script and Streamlit</div>
        </div>
        <div style="background:#ffffff;border:1px solid #d7e4dc;border-radius:16px;padding:16px;">
          <div style="font-size:18px;font-weight:800;color:#133d2e;margin-bottom:8px;">{t("plugins")}</div>
          <div style="font-size:14px;color:#374151;">{t("plugins_text")}</div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("""
<style>
.tree-card-wide {margin-bottom:18px;}
.tree-3blocks {display:grid; grid-template-columns: 1fr 1fr 1.55fr; gap:12px; margin-top:10px;}
.tree-block {background:#f8fafc; border:1px solid #d7e4dc; border-radius:14px; padding:12px;}
.tree-block-title {font-size:13px; font-weight:950; color:#0f3d25; margin-bottom:8px; text-transform:uppercase; letter-spacing:.2px;}
.tree-history-table {width:100%; border-collapse:collapse; font-size:11px; color:#334155;}
.tree-history-table th {background:#ecfdf5; color:#14532d; text-align:left; padding:5px; border-bottom:1px solid #bbf7d0;}
.tree-history-table td {padding:5px; border-bottom:1px solid #e5e7eb; vertical-align:top;}
@media (max-width: 1000px) {.tree-3blocks {grid-template-columns: 1fr;}}
</style>
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

tab_dashboard, tab_camas, tab_arboles, tab_eventos, tab_resumen_cosechas, tab_insumos, tab_calendario, tab_clima, tab_avance, tab_cuenta = st.tabs([f"📊 {t('dashboard')}", f"🛏️ {t('beds')}", f"🌳 {t('trees')}", f"🧪 {t('events')}", "📦 Resumen de Cosechas", "🧴 Insumos", f"📅 {t('calendar')}", f"☁️ {t('climate')}", f"📷 {t('progress')}", f"👤 {t('account')}"] )

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

with tab_resumen_cosechas:
    render_cosechas_report(eventos)

with tab_insumos:
    render_insumos_view(insumos)

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
