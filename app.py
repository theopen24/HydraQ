from pathlib import Path
from datetime import date, datetime, timedelta
import calendar
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


UI_TEXT['es'].update({
    'general_info':'Información general',
    'registered_events':'Eventos registrados',
    'future_actions_notes':'Acciones futuras y notas',
    'pending_actions':'Acciones programadas',
    'no_pending_actions':'Sin acciones futuras programadas',
    'notes':'Notas',
    'no_notes':'Sin notas',
    'current_event':'Evento agrícola',
    'tree_history_help':'Historial cronológico más reciente',
    'future_section_help':'Próximas acciones sugeridas y observaciones',
    'doses':'Dosis',
    'field_dose_reference':'Referencia de dosis en campo',
    'liquid_foliar_controls':'Controles fitosanitarios y abonos foliares',
    'yaramila_tree_reference':'YaraMila Hydrocomplex por árbol',
    'dose_per_liter':'Dosis por litro',
    'dose_per_20l':'Dosis por bomba 20 L',
    'source_note':'Nota / fuente',
    'reference_only':'Referencia operativa; validar etiqueta del producto antes de aplicar.',
    'event_history':'Historial de Eventos',
    'whats_next':'Qué hay y qué viene',
    'whats_next_title':'Qué hay y qué viene / Próximas acciones',
    'whats_next_help':'Esta vista muestra solo eventos futuros desplegados en las próximas 4 semanas a partir de hoy. Para historia de eventos, usar Historial de Eventos o la base de datos.',
    'event_type_filter':'Tipo de evento',
    'showing_last_events':'Mostrando las últimas 50 entradas de {total} eventos registrados. Los eventos futuros se resaltan en verde. Para análisis histórico completo usar la base de datos.',
    'input_section':'Insumos',
    'input_section_help':'Catálogo operativo de insumos, dosis por litro y notas de uso en campo.',
    'no_future_events_4w':'No hay eventos futuros programados para las próximas 4 semanas según los filtros actuales.',
    'objective':'Objetivo',
    'notes_col':'Notas',
    'all_option':'Todos',
    'event_kind_harvest':'🥬 Cosecha',
    'event_kind_fito':'🛡️ Fitosanitario',
    'event_kind_abono':'🧪 Abono / foliar',
    'event_kind_poda':'✂️ Poda / manejo',
    'event_kind_riego':'💧 Riego',
    'event_kind_otro':'📌 Otro',
})
UI_TEXT['en'].update({
    'general_info':'General information',
    'registered_events':'Registered events',
    'future_actions_notes':'Future actions and notes',
    'pending_actions':'Scheduled actions',
    'no_pending_actions':'No upcoming actions scheduled',
    'notes':'Notes',
    'no_notes':'No notes',
    'current_event':'Agricultural event',
    'tree_history_help':'Most recent chronological history',
    'future_section_help':'Suggested next actions and observations',
    'doses':'Doses',
    'field_dose_reference':'Field dose reference',
    'liquid_foliar_controls':'Phytosanitary controls and foliar fertilizers',
    'yaramila_tree_reference':'YaraMila Hydrocomplex by tree',
    'dose_per_liter':'Dose per liter',
    'dose_per_20l':'Dose per 20 L sprayer',
    'source_note':'Note / source',
    'reference_only':'Operational reference; validate product label before applying.',
    'event_history':'Event History',
    'whats_next':'What is next',
    'whats_next_title':'What is next / Upcoming actions',
    'whats_next_help':'This view only shows future events scheduled over the next 4 weeks from today. For event history, use Event History or the database.',
    'event_type_filter':'Event type',
    'showing_last_events':'Showing the latest 50 entries out of {total} registered events. Future events are highlighted in green. For full historical analysis, use the database.',
    'input_section':'Inputs',
    'input_section_help':'Operational input catalog, dose per liter and field-use notes.',
    'no_future_events_4w':'There are no future events scheduled for the next 4 weeks with the current filters.',
    'objective':'Target',
    'notes_col':'Notes',
    'all_option':'All',
    'event_kind_harvest':'🥬 Harvest',
    'event_kind_fito':'🛡️ Pest control',
    'event_kind_abono':'🧪 Fertilization / foliar',
    'event_kind_poda':'✂️ Pruning / management',
    'event_kind_riego':'💧 Irrigation',
    'event_kind_otro':'📌 Other',
})

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

.bed-thumb-wrap {display:flex; align-items:center; gap:10px; margin:4px 0 10px 0;}
.bed-thumb {width:20%; max-width:145px; min-width:92px; height:78px; object-fit:cover; border-radius:12px; border:1px solid rgba(255,255,255,.58); box-shadow:0 4px 12px rgba(0,0,0,.18);}
.bed-thumb-placeholder {width:20%; max-width:145px; min-width:92px; height:78px; border-radius:12px; border:1px dashed rgba(255,255,255,.58); display:flex; align-items:center; justify-content:center; color:#d1fae5; font-size:24px; background:rgba(255,255,255,.08);}
.bed-thumb-text {font-size:12px; color:#d1fae5; font-weight:800;}
.history-table {width:100%; border-collapse:collapse; margin-top:8px; font-size:11px; overflow:hidden; border-radius:10px;}
.history-table th {background:#ecfdf5; color:#166534; text-align:left; padding:5px 6px; font-weight:950;}
.history-table td {border-top:1px solid #d1fae5; padding:5px 6px; color:#334155; font-weight:750; vertical-align:top;}
.history-table .datecol {white-space:nowrap; color:#0f3d25; font-weight:950;}
.tree-header {display:flex; align-items:center; gap:14px; margin-bottom:10px;}
.tree-body {display:flex; flex-direction:column; gap:10px;}
.tree-section {background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:10px 12px;}
.tree-section.general-info {background:#f8fafc; border-left:5px solid #86efac;}
.tree-section.registered-events {background:#f0fdf4; border-left:5px solid #22c55e;}
.tree-section.future-actions {background:#eff6ff; border-left:5px solid #3b82f6;}
.tree-section + .tree-section {margin-top:2px;}
.tree-subtitle {font-size:12px; font-weight:950; color:#0f3d25; text-transform:uppercase; letter-spacing:.4px; margin-bottom:6px;}
.tree-subnote {font-size:11px; color:#64748b; font-weight:750; margin:-2px 0 6px 0;}
.pending-table {width:100%; border-collapse:collapse; margin-top:6px; font-size:11px;}
.pending-table th {background:#eff6ff; color:#1d4ed8; text-align:left; padding:5px 6px; font-weight:950;}
.pending-table td {border-top:1px solid #dbeafe; padding:5px 6px; color:#334155; font-weight:750; vertical-align:top;}
.pending-note {font-size:12px; color:#334155; font-weight:750; margin-top:6px;}
.notes-box {margin-top:8px; background:#fff7ed; border:1px solid #fed7aa; border-radius:10px; padding:8px 10px; color:#7c2d12; font-size:12px; font-weight:750;}
.progress-grid {display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:14px;}
.progress-card {background:rgba(255,255,255,.95); border:1px solid rgba(255,255,255,.72); border-radius:16px; padding:10px; box-shadow:0 6px 16px rgba(0,0,0,.14); color:#0f172a;}
.progress-frame {width:100%; aspect-ratio:4 / 3; border-radius:12px; overflow:hidden; background:#e5e7eb; border:1px solid #dbe7de; display:flex; align-items:center; justify-content:center; color:#64748b; font-weight:950;}
.progress-frame img {width:100%; height:100%; object-fit:cover; display:block;}
.progress-title {font-size:14px; font-weight:950; color:#0f3d25; margin-top:8px;}
.progress-meta {font-size:12px; color:#64748b; font-weight:750;}
.weather-reference {background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:10px 12px; color:#7c2d12; font-weight:800; margin:8px 0 12px 0;}



.bed-thumb-link {display:inline-block; width:20%; max-width:145px; min-width:92px;}
.bed-thumb-link .bed-thumb {width:100%; max-width:145px; min-width:92px;}
.img-modal {position:fixed; inset:0; background:rgba(0,0,0,.86); display:none; align-items:center; justify-content:center; z-index:999999; padding:24px;}
.img-modal:target {display:flex;}
.img-modal img {max-width:92vw; max-height:86vh; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.45);}
.img-modal .close {position:absolute; top:18px; right:24px; color:white; text-decoration:none; font-size:38px; font-weight:950; line-height:1;}
.img-modal-caption {position:absolute; bottom:18px; color:white; background:rgba(0,0,0,.42); padding:8px 12px; border-radius:999px; font-size:13px; font-weight:800;}
.dose-section-title {font-size:24px; font-weight:950; color:#ffffff; margin:20px 0 12px 0;}
.dose-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:12px; margin-bottom:18px;}
.dose-card {background:rgba(255,255,255,.96); border:1px solid rgba(255,255,255,.7); border-radius:16px; padding:13px 14px; color:#0f172a; box-shadow:0 6px 16px rgba(0,0,0,.14);}
.dose-name {font-size:16px; font-weight:950; color:#0f3d25; margin-bottom:5px;}
.dose-chip {display:inline-block; padding:4px 9px; border-radius:999px; background:#ecfdf5; color:#166534; font-size:12px; font-weight:900; margin:2px 4px 5px 0;}
.dose-line {font-size:13px; color:#334155; font-weight:750; margin-top:4px;}
.dose-note {font-size:12px; color:#64748b; font-weight:700; margin-top:6px;}
.dose-warning {background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:10px 12px; color:#7c2d12; font-size:13px; font-weight:800; margin-bottom:14px;}


/* V30 calendar and event improvements */
.calendar-help {background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:10px 12px; color:#7c2d12; font-size:13px; font-weight:850; margin:10px 0 14px 0;}
.cal-event {border-radius:12px; padding:9px 10px; margin:8px 0; border-left:5px solid #94a3b8; background:#ffffff; box-shadow:0 4px 10px rgba(0,0,0,.08);}
.cal-event.harvest {border-left-color:#16a34a; background:#f0fdf4;}
.cal-event.fito {border-left-color:#dc2626; background:#fef2f2;}
.cal-event.abono {border-left-color:#ca8a04; background:#fffbeb;}
.cal-event.poda {border-left-color:#7c3aed; background:#f5f3ff;}
.cal-event.riego {border-left-color:#0284c7; background:#f0f9ff;}
.cal-event.otro {border-left-color:#64748b; background:#f8fafc;}
.cal-event-type {font-size:10px; font-weight:950; text-transform:uppercase; letter-spacing:.35px; color:#334155;}
.cal-event-title {font-size:13px; font-weight:950; color:#0f172a; margin-top:2px;}
.cal-event-meta {font-size:11px; font-weight:750; color:#475569; margin-top:3px;}
.calendar-legend {display:flex; gap:8px; flex-wrap:wrap; margin:4px 0 12px 0;}
.legend-pill {display:inline-flex; align-items:center; gap:5px; padding:5px 9px; border-radius:999px; background:#ffffff; border:1px solid #dbe6df; font-size:11px; font-weight:850; color:#0f3d25;}
.legend-dot {width:10px; height:10px; border-radius:999px; display:inline-block;}
.event-table {width:100%; border-collapse:collapse; background:#ffffff; border-radius:14px; overflow:hidden; font-size:12px;}
.event-table th {background:#0f3d25; color:#ffffff; text-align:left; padding:8px 9px; font-weight:950;}
.event-table td {border-top:1px solid #e2e8f0; padding:7px 9px; color:#1f2937; font-weight:750; vertical-align:top;}
.event-summary-note {background:#eff6ff; border:1px solid #bfdbfe; color:#1d4ed8; border-radius:14px; padding:10px 12px; font-size:13px; font-weight:850; margin:8px 0 14px 0;}
.insumo-icon {font-size:28px; width:42px; height:42px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:#ecfdf5; margin-bottom:8px;}
.progress-matrix {width:100%; border-collapse:separate; border-spacing:0; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 6px 16px rgba(0,0,0,.14); font-size:12px;}
.progress-matrix th {background:#0f3d25; color:#ffffff; padding:9px 10px; text-align:center; font-weight:950;}
.progress-matrix td {border-top:1px solid #e2e8f0; border-right:1px solid #e2e8f0; padding:8px; text-align:center; color:#334155; font-weight:800; min-width:95px;}
.progress-matrix .bed-cell {text-align:left; background:#f8fafc; color:#0f3d25; font-weight:950;}
.progress-mini-img {width:88px; height:58px; object-fit:cover; border-radius:10px; display:block; margin:0 auto 4px auto;}
.progress-pending {border:1px dashed #cbd5e1; border-radius:10px; padding:12px 6px; color:#64748b; background:#f8fafc;}


/* V31 refinements */
.event-table.compact {font-size:11px; line-height:1.15;}
.event-table.compact th {padding:5px 7px;}
.event-table.compact td {padding:4px 7px;}
.event-table tr.future-row td {background:#ecfdf5; color:#064e3b;}
.event-table tr.future-row td:first-child {border-left:5px solid #22c55e;}
.input-section-title {font-size:24px; font-weight:950; color:#ffffff; margin:18px 0 12px 0;}


.calendar-filter-title {font-size:13px; color:#d1fae5; font-weight:900; margin:8px 0 2px 0;}
div[data-testid="stCheckbox"] label {font-size:12px !important; font-weight:800 !important;}

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
        ["ID_Insumo","Nombre","Tipo","Disponible","Uso_Principal","Restricciones/Notas","Compra_Requerida",
         "Cantidad_Guia","Momento_Aplicacion","Frecuencia_Dias","Dosis_Por_Litro","Unidad_Dosis",
         "Tipo_Dosis","Fuente_Dosis","Notas_Dosis"]
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
    for col in ["Finca", "Arbol", "Icono", "Estado_Fenologico", "Trasplante", "Estado_Sanitario", "Evento_Agricola", "Notas"]:
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
    name = str(row.get("Arbol", "")).lower().strip()

    # Íconos diferenciados por especie. Solo comparten icono cuando claramente son la misma familia/grupo práctico.
    icon_map = [
        (["manzano", "manzana"], "🍎"),
        (["naranja washington", "naranja valencia", "naranja"], "🍊"),
        (["mandarina"], "🍊"),
        (["limón", "limon"], "🍋"),
        (["mango", "manga"], "🥭"),
        (["durazno"], "🍑"),
        (["guanábana", "guanabana"], "🍈"),
        (["anona"], "🟤"),
        (["cas"], "🟡"),
        (["guayabita"], "🟣"),
        (["guayaba"], "🟢"),
        (["níspero", "nispero"], "🟠"),
        (["mamón chino", "mamon chino"], "🔴"),
        (["carambola"], "⭐"),
        (["banano", "plátano", "platano"], "🍌"),
        (["yuplón", "yuplon"], "🟢"),
    ]
    for keys, emoji in icon_map:
        if any(k in name for k in keys):
            return emoji

    icon = str(row.get("Icono", "") or "").strip()
    for candidate in ["🍎", "🍊", "🍋", "🥭", "🍑", "🍈", "🟤", "🟡", "🟣", "🟢", "🟠", "🔴", "⭐", "🍌", "🌳"]:
        if candidate in icon:
            return candidate
    return "🌳"

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



def pending_actions_html(events, target_id, limit=4):
    if events is None or events.empty or not target_id:
        return f'<div class="pending-note">{t("no_pending_actions")}</div>'
    subset = events[events['Target_ID'].astype(str) == str(target_id)].copy()
    if subset.empty:
        return f'<div class="pending-note">{t("no_pending_actions")}</div>'
    subset['_date'] = subset.apply(event_effective_date, axis=1)
    subset = subset[~subset['Estado'].astype(str).str.lower().str.contains('complet', na=False)]
    subset = subset.sort_values('_date', na_position='last').head(limit)
    if subset.empty:
        return f'<div class="pending-note">{t("no_pending_actions")}</div>'
    rows = []
    for _, r in subset.iterrows():
        fecha = fmt_date(r.get('_date')) if pd.notna(r.get('_date')) else t('date_none')
        evento = tv(r.get('Tipo_Evento', ''))
        insumo = r.get('Nombre_Insumo', '') or t('no_input')
        estado = tv(r.get('Estado', ''))
        rows.append(f'<tr><td class="datecol">{fecha}</td><td>{evento}</td><td>{insumo}</td><td>{estado}</td></tr>')
    return f'<table class="pending-table"><thead><tr><th>{t("date")}</th><th>{t("event_type")}</th><th>{t("input")}</th><th>{t("status")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'


def tree_notes_html(row):
    notes = str(row.get('Notas', '') or '').strip()
    current_event = str(row.get('Evento_Agricola', '') or '').strip()
    blocks = []
    if current_event and current_event.lower() != 'nan':
        blocks.append(f'<div class="pending-note"><b>{t("current_event")}:</b> {tv(current_event)}</div>')
    if notes and notes.lower() != 'nan':
        blocks.append(f'<div class="notes-box"><b>{t("notes")}:</b> {notes}</div>')
    if not blocks:
        return f'<div class="pending-note">{t("no_notes")}</div>'
    return ''.join(blocks)


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
    html_block(f'<div class="dash-panel"><div class="dash-panel-title">{t("photo_progress")}</div><div class="dash-line">Matriz de avance visual: camas en filas y meses en columnas, iniciando en junio. Las fotos reales se irán agregando conforme se carguen al flujo de fotos.</div><div class="dash-line"><span class="dash-pill pill-blue">Tip</span>{t("camera_note")}</div></div>')

    beds = [f"Cama {i}" for i in range(1, 8)]
    months = ["Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    june_refs = {
        "Cama 1": "vista_este.jpeg",
        "Cama 3": "cama_6_y_3.jpeg",
        "Cama 6": "cama_6_y_3.jpeg",
        "Cama 7": "vista_sur.jpeg",
    }

    html = ['<table class="progress-matrix"><thead><tr><th>Cama</th>']
    for m in months:
        html.append(f'<th>{m}</th>')
    html.append('</tr></thead><tbody>')

    for bed in beds:
        html.append(f'<tr><td class="bed-cell">{bed}</td>')
        for m in months:
            img = june_refs.get(bed) if m == "Junio" else None
            uri = img_data_uri(img) if img else None
            if uri:
                cell = f'<img class="progress-mini-img" src="{uri}"><div>Referencia</div>'
            else:
                cell = '<div class="progress-pending">📷<br>Pendiente</div>'
            html.append(f'<td>{cell}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    html_block(''.join(html))

    uploaded = st.file_uploader(t("upload_new_photo"), type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded:
        st.write(f"{len(uploaded)} archivo(s) cargado(s) para vista previa. Persistencia real pendiente de integrar.")
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
            import base64, mimetypes
            mime = mimetypes.guess_type(photo_path)[0] or "image/jpeg"
            uri = "data:" + mime + ";base64," + base64.b64encode(Path(photo_path).read_bytes()).decode("utf-8")
            safe_id = re.sub(r'[^a-zA-Z0-9_-]+', '_', str(unidad))
            st.markdown(
                f'''
                <div class="bed-thumb-wrap">
                    <a class="bed-thumb-link" href="#foto_{safe_id}">
                        <img class="bed-thumb" src="{uri}" title="Click para ampliar">
                    </a>
                    <div class="bed-thumb-text">📷 {t("bed_visual_reference")}<br>{photo_caption}<br><span style="font-size:11px;opacity:.8;">Click para ampliar</span></div>
                </div>
                <div id="foto_{safe_id}" class="img-modal">
                    <a href="#" class="close">×</a>
                    <img src="{uri}">
                    <div class="img-modal-caption">{unidad} · {photo_caption}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
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




def calendar_type_label(kind):
    labels = {
        "harvest": t("event_kind_harvest"),
        "fito": t("event_kind_fito"),
        "abono": t("event_kind_abono"),
        "poda": t("event_kind_poda"),
        "riego": t("event_kind_riego"),
        "otro": t("event_kind_otro"),
    }
    return labels.get(kind, kind)

def calendar_event_kind(tipo):
    s = str(tipo).lower()
    if "cosecha" in s:
        return "harvest", "🥬"
    if "fitosanit" in s or "control" in s:
        return "fito", "🛡️"
    if "abono" in s or "foliar" in s or "enmienda" in s:
        return "abono", "🧪"
    if "poda" in s or "amarre" in s or "arqueo" in s:
        return "poda", "✂️"
    if "riego" in s or "hídrico" in s or "hidrico" in s:
        return "riego", "💧"
    return "otro", "📌"


def calendar_event_card(tipo, titulo, fecha, meta="", extra=""):
    kind, icon = calendar_event_kind(tipo)
    fecha_txt = fmt_date(fecha) if pd.notna(fecha) else t("date_none")
    return (
        f'<div class="cal-event {kind}">'
        f'<div class="cal-event-type">{icon} {tv(tipo)}</div>'
        f'<div class="cal-event-title">{titulo}</div>'
        f'<div class="cal-event-meta">{fecha_txt} · {meta}</div>'
        f'<div class="cal-event-meta">{extra}</div>'
        f'</div>'
    )


def insumo_icon(nombre, tipo=""):
    n = str(nombre).lower()
    tpo = str(tipo).lower()
    if "yaramila" in n or "fertiliz" in tpo or "abono" in tpo:
        return "🌱"
    if "pas" in n:
        return "⚗️"
    if "mistral" in n or "barrera" in n or "cobre" in n:
        return "🛡️"
    if "neem" in n:
        return "🌿"
    if "safer" in n or "soap" in n or "jabón" in n or "jabon" in n:
        return "🧼"
    if "boro" in n or "calcio" in n or "metalosate" in n or "evofert" in n or "potasio" in n or "multi" in n:
        return "🧪"
    return "🧴"

def render_calendar_view(all_df, events=None, trees=None):
    today = date.today()
    end_date = today + timedelta(days=27)

    st.markdown(f'<div class="section-title">📅 {t("whats_next_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="calendar-help">{t("whats_next_help")}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.15, 1.15, 1.7])
    crop_options = [t("all_m")] + sorted([x for x in all_df["Cultivo"].dropna().unique() if x and x != "Disponible"])
    with c1:
        cal_cultivo = st.selectbox(t("crop"), crop_options, key="cal_cultivo")
    unit_options = [t("all_f")] + sorted([x for x in all_df["Unidad"].dropna().unique() if x])
    with c2:
        cal_cama = st.selectbox(t("bed"), unit_options, key="cal_cama")
    tree_options = [t("all_m")]
    if trees is not None and not trees.empty and "Arbol" in trees.columns:
        tree_options += sorted([x for x in trees["Arbol"].dropna().unique() if x])
    with c3:
        cal_arbol = st.selectbox(t("trees"), tree_options, key="cal_arbol")

    st.markdown(f'<div class="calendar-filter-title">{t("event_type_filter")}</div>', unsafe_allow_html=True)
    type_options = ["harvest", "fito", "abono", "poda", "riego", "otro"]
    type_cols = st.columns(6)
    selected_types = []
    for col, kind in zip(type_cols, type_options):
        with col:
            if st.checkbox(calendar_type_label(kind), value=True, key=f"cal_type_{kind}"):
                selected_types.append(kind)

    st.markdown(
        '<div class="calendar-legend">'
        f'<span class="legend-pill"><span class="legend-dot" style="background:#16a34a;"></span>{t("event_kind_harvest")}</span>'
        f'<span class="legend-pill"><span class="legend-dot" style="background:#dc2626;"></span>{t("event_kind_fito")}</span>'
        f'<span class="legend-pill"><span class="legend-dot" style="background:#ca8a04;"></span>{t("event_kind_abono")}</span>'
        f'<span class="legend-pill"><span class="legend-dot" style="background:#7c3aed;"></span>{t("event_kind_poda")}</span>'
        f'<span class="legend-pill"><span class="legend-dot" style="background:#0284c7;"></span>{t("event_kind_riego")}</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    rows = []

    # Crop harvests
    crop_df = all_df.copy()
    crop_df = crop_df[
        (crop_df["Cultivo"] != "Disponible")
        & (crop_df["Estado_Unidad"] != "No activa")
        & crop_df["Cosecha_Min"].notna()
    ].copy()
    if not crop_df.empty:
        crop_df["Fecha"] = crop_df["Cosecha_Min"].dt.date
        crop_df = crop_df[(crop_df["Fecha"] >= today) & (crop_df["Fecha"] <= end_date)]
        if cal_cultivo != t("all_m"):
            crop_df = crop_df[crop_df["Cultivo"] == cal_cultivo]
        if cal_cama != t("all_f"):
            crop_df = crop_df[crop_df["Unidad"] == cal_cama]
        if "harvest" in selected_types:
            for _, r in crop_df.iterrows():
                rows.append({
                    "fecha": r["Fecha"],
                    "tipo": "Cosecha",
                    "kind": "harvest",
                    "titulo": str(r.get("Cultivo", "")),
                    "meta": f'{r.get("Finca","")} · {r.get("Unidad","")}',
                    "extra": f'{t("harvest_max")}: {fmt_date(r.get("Cosecha_Max"))}',
                })

    # Programmed future events
    if events is not None and not events.empty:
        ev = events.copy()
        ev["_fecha"] = pd.to_datetime(ev.get("Fecha_Programada"), errors="coerce").dt.date
        ev = ev[ev["_fecha"].notna()].copy()
        ev = ev[(ev["_fecha"] >= today) & (ev["_fecha"] <= end_date)]
        ev = ev[~ev["Estado"].astype(str).str.lower().str.contains("complet", na=False)]

        if cal_cultivo != t("all_m"):
            ev = ev[
                ev.get("Cultivo", "").astype(str).eq(cal_cultivo)
                | ev.get("Target_Label", "").astype(str).str.contains(cal_cultivo, case=False, na=False)
            ]
        if cal_cama != t("all_f"):
            ev = ev[
                ev.get("Unidad", "").astype(str).eq(cal_cama)
                | ev.get("Target_Label", "").astype(str).str.contains(cal_cama, case=False, na=False)
            ]
        if cal_arbol != t("all_m"):
            ev = ev[
                ev.get("Arbol", "").astype(str).eq(cal_arbol)
                | ev.get("Target_Label", "").astype(str).str.contains(cal_arbol, case=False, na=False)
            ]

        for _, r in ev.iterrows():
            tipo_evt = _txt(r.get("Tipo_Evento"), "Otro")
            kind, _ = calendar_event_kind(tipo_evt)
            if kind not in selected_types:
                continue
            target = _txt(r.get("Target_Label"), _txt(r.get("Arbol"), _txt(r.get("Cultivo"), _txt(r.get("Target_ID"), ""))))
            insumo = _txt(r.get("Nombre_Insumo"), _txt(r.get("Insumo"), t("no_input")))
            rows.append({
                "fecha": r["_fecha"],
                "tipo": tipo_evt,
                "kind": kind,
                "titulo": target,
                "meta": f'{_txt(r.get("Finca"), "")} · {tv(_txt(r.get("Target_Tipo"), ""))}',
                "extra": f'{t("input")}: {insumo}',
            })

    events_df = pd.DataFrame(rows)
    if not events_df.empty:
        events_df["week_start"] = events_df["fecha"].apply(week_start_for_date)

    weeks = []
    cur = week_start_for_date(today)
    for _ in range(4):
        weeks.append((cur, cur + timedelta(days=6)))
        cur += timedelta(days=7)

    any_events = False
    cols = st.columns(4)
    for col, (week_start, week_end) in zip(cols, weeks):
        with col:
            if events_df.empty:
                week_events = pd.DataFrame()
            else:
                week_events = events_df[events_df["week_start"] == week_start].sort_values(["fecha", "tipo", "titulo"])
            if not week_events.empty:
                any_events = True
            html = ""
            for _, r in week_events.iterrows():
                html += calendar_event_card(r["tipo"], r["titulo"], r["fecha"], r["meta"], r["extra"])
            if not html:
                html = f'<div class="no-events">{t("no_available_harvest")}</div>'

            iso_year, iso_week, _ = week_start.isocalendar()
            html_block(
                f'<div class="week-card"><div class="week-title">{t("week")} {iso_week:02d}</div>'
                f'<div class="week-range">{week_start.strftime("%d %b %Y")} – {week_end.strftime("%d %b %Y")}</div>'
                f'{html}</div>'
            )

    if not any_events:
        html_block(f'<div class="calendar-toolbar"><div class="calendar-note">{t("no_future_events_4w")}</div></div>')

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
    history_html = history_table_html(events, row.get("Arbol_ID"))
    next_abono_html = next_soil_abono_html(events, insumos, row.get("Arbol_ID"), row.get("Estado_Fenologico", ""))
    pending_html = pending_actions_html(events, row.get("Arbol_ID"))
    notes_html = tree_notes_html(row)
    st.markdown(f"""
    <div class="tree-card">
        <div class="tree-header">
            <div class="tree-icon">{normalized_tree_icon(row)}</div>
            <div style="width:100%;">
                <div class="tree-name">{row['Arbol']}</div>
            </div>
        </div>
        <div class="tree-body">
            <div class="tree-section general-info">
                <div class="tree-subtitle">{t('general_info')}</div>
                <div class="tree-line">{t("phenology")} <span class="tree-pill {phen_class(row['Estado_Fenologico'])}">{tv(row['Estado_Fenologico'])}</span></div>
                <div class="tree-line">Trasplante <b>{row['Trasplante']}</b></div>
                <div class="tree-line">{t("health_status")} <span class="tree-pill {health_class(row['Estado_Sanitario'])}">● {tv(row['Estado_Sanitario'])}</span></div>
                {control_html}
            </div>
            <div class="tree-section registered-events">
                <div class="tree-subtitle">{t('registered_events')}</div>
                <div class="tree-subnote">{t('tree_history_help')}</div>
                {history_html}
            </div>
            <div class="tree-section future-actions">
                <div class="tree-subtitle">{t('future_actions_notes')}</div>
                <div class="tree-subnote">{t('future_section_help')}</div>
                {next_abono_html}
                <div class="pending-note" style="margin-top:8px;"><b>{t('pending_actions')}</b></div>
                {pending_html}
                {notes_html}
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
    st.markdown(f'<div class="section-title">🧾 {t("event_history")}</div>', unsafe_allow_html=True)
    if events is None or events.empty:
        st.markdown(f'<div class="calendar-toolbar"><div class="calendar-note">{t("no_events_filters")}</div></div>', unsafe_allow_html=True)
        return

    today = date.today()
    df_events = events.copy()
    df_events["_date"] = df_events.apply(event_effective_date, axis=1)
    df_events["_date_sort"] = pd.to_datetime(df_events["_date"], errors="coerce")
    df_events["_is_future"] = df_events["_date_sort"].dt.date >= today
    total_events = len(df_events)
    latest = df_events.sort_values("_date_sort", ascending=False, na_position="last").head(50).copy()

    st.markdown(
        f'<div class="event-summary-note">{t("showing_last_events").format(total=total_events)}</div>',
        unsafe_allow_html=True,
    )

    rows = ['<table class="event-table compact"><thead><tr>'
            f'<th>{t("date")}</th><th>{t("event_type")}</th><th>{t("objective")}</th><th>{t("farm")}</th><th>{t("input")}</th><th>{t("event_status")}</th><th>{t("notes_col")}</th>'
            '</tr></thead><tbody>']
    for _, r in latest.iterrows():
        fecha_txt = fmt_date(r.get("_date")) if pd.notna(r.get("_date")) else t("date_none")
        target = _txt(r.get("Target_Label"), _txt(r.get("Arbol"), _txt(r.get("Cultivo"), _txt(r.get("Target_ID"), ""))))
        insumo = _txt(r.get("Nombre_Insumo"), _txt(r.get("Insumo"), t("no_input")))
        row_class = ' class="future-row"' if bool(r.get("_is_future")) else ""
        rows.append(
            f'<tr{row_class}>'
            f'<td>{fecha_txt}</td>'
            f'<td>{tv(r.get("Tipo_Evento", ""))}</td>'
            f'<td>{target}</td>'
            f'<td>{_txt(r.get("Finca"), "")}</td>'
            f'<td>{insumo}</td>'
            f'<td>{tv(r.get("Estado", ""))}</td>'
            f'<td>{_txt(r.get("Notas"), "")}</td>'
            '</tr>'
        )
    rows.append('</tbody></table>')
    st.markdown(''.join(rows), unsafe_allow_html=True)


def render_insumos_view(insumos):
    st.markdown(f'<div class="section-title">🧴 {t("input_section")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="event-summary-note">{t("input_section_help")}</div>', unsafe_allow_html=True)
    if insumos is None or insumos.empty:
        st.write(t("no_inputs"))
        return
    for tipo, group in insumos.groupby("Tipo", sort=False):
        st.markdown(f'<div class="input-section-title">{tipo}</div>', unsafe_allow_html=True)
        records = list(group.iterrows())
        for start in range(0, len(records), 4):
            cols = st.columns(4)
            for col, (_, row) in zip(cols, records[start:start+4]):
                with col:
                    compra = t("purchase_required") if str(row.get("Compra_Requerida", "")).lower().startswith("s") else t("available_stock")
                    icon = insumo_icon(row.get("Nombre", ""), row.get("Tipo", ""))
                    dosis = row.get("Dosis_Por_Litro", t("according_criteria")) if str(row.get("Dosis_Por_Litro", "")).strip() else t("according_criteria")
                    html = f"""
                    <div class="insumo-card">
                        <div class="insumo-icon">{icon}</div>
                        <div class="insumo-name">{row.get("Nombre", "")}</div>
                        <div class="insumo-meta">{row.get("Uso_Principal", "")}</div>
                        <div class="insumo-meta"><b>{t("dose_per_liter")}:</b> {dosis}</div>
                        <div class="insumo-meta"><b>{t("guide_qty")}:</b> {row.get("Cantidad_Guia", t("according_criteria"))}</div>
                        <div class="insumo-meta"><b>{t("timing")}:</b> {row.get("Momento_Aplicacion", t("according_state"))}</div>
                        <div class="insumo-meta"><b>{compra}</b></div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)


def _txt(value, fallback=""):
    if value is None or pd.isna(value):
        return fallback
    text = str(value).strip()
    if text.lower() in ["", "nan", "none"]:
        return fallback
    return text


def render_dosis_view(insumos):
    st.markdown(f'<div class="section-title">🧪 {t("field_dose_reference")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dose-warning">{t("reference_only")} Datos leídos desde la pestaña Insumos. Dosis mostradas solo por 1 litro.</div>', unsafe_allow_html=True)

    if insumos is None or insumos.empty:
        st.write(t("no_inputs"))
        return

    df_ins = insumos.copy()
    for col in ["Dosis_Por_Litro", "Unidad_Dosis", "Tipo_Dosis", "Fuente_Dosis", "Notas_Dosis", "Cantidad_Guia", "Momento_Aplicacion", "Frecuencia_Dias"]:
        if col not in df_ins.columns:
            df_ins[col] = ""

    tipo = df_ins.get("Tipo", "").astype(str).str.lower()
    dosis = df_ins.get("Dosis_Por_Litro", "").astype(str).str.lower()
    liquid_mask = (
        tipo.str.contains("control|foliar|coadyuv", na=False)
        & ~dosis.str.contains("no aplica", na=False)
        & dosis.str.strip().ne("")
        & ~dosis.str.contains("pendiente", na=False)
    )
    liquid_rows = df_ins[liquid_mask].copy()

    st.markdown(f'<div class="dose-section-title">{t("liquid_foliar_controls")}</div>', unsafe_allow_html=True)
    if liquid_rows.empty:
        st.markdown('<div class="dose-warning">No hay dosis por litro cargadas en Insumos.</div>', unsafe_allow_html=True)
    else:
        cards = ['<div class="dose-grid">']
        for _, r in liquid_rows.iterrows():
            dose_l = _txt(r.get("Dosis_Por_Litro"), t("according_criteria"))
            source = _txt(r.get("Fuente_Dosis"), "")
            note = _txt(r.get("Notas_Dosis"), "")
            cards.append(
                '<div class="dose-card">'
                f'<div class="dose-name">{_txt(r.get("Nombre"))}</div>'
                f'<span class="dose-chip">{_txt(r.get("Tipo"))}</span>'
                f'<div class="dose-line"><b>{t("dose_per_liter")}:</b> {dose_l}</div>'
                f'<div class="dose-note"><b>{t("source_note")}:</b> {source}</div>'
                f'<div class="dose-note">{note}</div>'
                '</div>'
            )
        cards.append('</div>')
        st.markdown(''.join(cards), unsafe_allow_html=True)

    st.markdown(f'<div class="dose-section-title">{t("yaramila_tree_reference")}</div>', unsafe_allow_html=True)
    ymask = df_ins.get("Nombre", "").astype(str).str.lower().str.contains("yaramila", na=False)
    y_rows = df_ins[ymask].copy()
    if y_rows.empty:
        st.markdown('<div class="dose-warning">No hay registro de YaraMila en Insumos.</div>', unsafe_allow_html=True)
    else:
        cards = ['<div class="dose-grid">']
        for _, r in y_rows.iterrows():
            cards.append(
                '<div class="dose-card">'
                f'<div class="dose-name">{_txt(r.get("Nombre"))}</div>'
                f'<span class="dose-chip">{_txt(r.get("Tipo_Dosis"), "Por árbol / corona")}</span>'
                f'<div class="dose-line"><b>{t("guide_qty")}:</b> {_txt(r.get("Cantidad_Guia"), t("according_criteria"))}</div>'
                f'<div class="dose-line"><b>{t("frequency")}:</b> {_txt(r.get("Frecuencia_Dias"), t("no_rule"))} días</div>'
                f'<div class="dose-line"><b>{t("timing")}:</b> {_txt(r.get("Momento_Aplicacion"), t("according_state"))}</div>'
                f'<div class="dose-note"><b>{t("source_note")}:</b> {_txt(r.get("Fuente_Dosis"), "Referencia interna FincaOS")}</div>'
                f'<div class="dose-note">{_txt(r.get("Notas_Dosis"), "")}</div>'
                '</div>'
            )
        cards.append('</div>')
        st.markdown(''.join(cards), unsafe_allow_html=True)

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
          <div style="font-size:15px;color:#1f2937;"><b>{t("developer_version")}:</b> 32</div>
          <div style="font-size:15px;color:#1f2937;"><b>{t("date_label")}:</b> 2026-06-12</div>
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

tab_dashboard, tab_camas, tab_arboles, tab_eventos, tab_insumos, tab_dosis, tab_proximas, tab_clima, tab_avance, tab_cuenta = st.tabs([f"📊 {t('dashboard')}", f"🛏️ {t('beds')}", f"🌳 {t('trees')}", f"🧾 {t('event_history')}", f"🧴 {t('input_section')}", f"📏 {t('doses')}", f"📅 {t('whats_next')}", f"☁️ {t('climate')}", f"📷 {t('progress')}", f"👤 {t('account')}"] )

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

with tab_insumos:
    render_insumos_view(insumos)

with tab_dosis:
    render_dosis_view(insumos)

with tab_proximas:
    render_calendar_view(df, eventos, trees)

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
