import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

def ajustar_fin_de_semana(fecha):
    """Ajusta la fecha si cae en fin de semana, moviendo al viernes anterior"""
    dia_semana = fecha.weekday()
    if dia_semana == 5:  # Sábado
        fecha = fecha - timedelta(days=1)
    elif dia_semana == 6:  # Domingo
        fecha = fecha - timedelta(days=2)
    return fecha

def calcular_fechas_pago(fecha_inicio, fecha_fin):
    """Calcula todas las fechas de pago quincenales en el periodo"""
    fechas_pago = []
    
    fecha_actual = fecha_inicio.replace(day=1)
    
    while fecha_actual <= fecha_fin:
        year = fecha_actual.year
        month = fecha_actual.month
        
        # Pago del día 15
        fecha_15 = datetime(year, month, 15)
        if fecha_inicio <= fecha_15 <= fecha_fin:
            fecha_15_ajustada = ajustar_fin_de_semana(fecha_15)
            fechas_pago.append(fecha_15_ajustada)
        
        # Pago de fin de mes (último día del mes)
        ultimo_dia = calendar.monthrange(year, month)[1]
        fecha_fin_mes = datetime(year, month, ultimo_dia)
        if fecha_inicio <= fecha_fin_mes <= fecha_fin:
            fecha_fin_mes_ajustada = ajustar_fin_de_semana(fecha_fin_mes)
            fechas_pago.append(fecha_fin_mes_ajustada)
        
        # Siguiente mes
        if month == 12:
            fecha_actual = datetime(year + 1, 1, 1)
        else:
            fecha_actual = datetime(year, month + 1, 1)
    
    return sorted(list(set(fechas_pago)))

def calcular_semanas(fecha_inicio, fecha_fin):
    """Cuenta semanas basándose en número de lunes en el período"""
    dias_totales = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir el último día
    dias_hasta_lunes = (7 - fecha_inicio.weekday()) % 7
    semanas = 1 + ((dias_totales - dias_hasta_lunes - 1) // 7)
    return semanas

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Pagos Quincenales",
    page_icon="📅",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* Modo claro */
    [data-testid="stAppViewContainer"] .main-title {
        color: #1f2937;
    }
    [data-testid="stAppViewContainer"] .subtitle {
        color: #6b7280;
    }
    /* Modo oscuro */
    [data-theme="dark"] .main-title {
        color: #f9fafb;
    }
    [data-theme="dark"] .subtitle {
        color: #d1d5db;
    }
    .metric-card {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-card .label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .blue-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }
    .green-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .month-box {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 15px;
        background: white;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    [data-theme="dark"] .month-box {
        background: #1f2937;
        border-color: #374151;
    }
    .month-title {
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
        color: #1f2937;
        flex-shrink: 0;
    }
    [data-theme="dark"] .month-title {
        color: #f9fafb;
    }
    .cal-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(7, 1fr);
        gap: 3px;
        flex-grow: 1;
        min-height: 280px;
    }
    .cal-day-header {
        text-align: center;
        font-weight: bold;
        font-size: 0.8rem;
        padding: 5px;
        color: #6b7280;
    }
    [data-theme="dark"] .cal-day-header {
        color: #9ca3af;
    }
    .cal-day {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        font-size: 0.85rem;
        min-height: 35px;
    }
    .day-payment {
        background: #10b981;
        color: white;
        font-weight: bold;
    }
    .day-in-range {
        background: #e0e7ff;
        color: #1f2937;
    }
    .day-out-range {
        background: #f3f4f6;
        color: #9ca3af;
    }
    .legend-container {
        display: flex;
        gap: 20px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .legend-box {
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="main-title">📅 Calculadora de Semanas y Pagos Quincenales</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema de cálculo quincenal con ajuste automático de fines de semana</div>', unsafe_allow_html=True)

# Inputs
col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input(
        "Fecha de Inicio",
        value=datetime(2025, 3, 1),
        format="DD/MM/YYYY"
    )

with col2:
    fecha_fin = st.date_input(
        "Fecha de Fin",
        value=datetime(2026, 2, 28),
        format="DD/MM/YYYY"
    )

# Convertir a datetime
fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
fecha_fin = datetime.combine(fecha_fin, datetime.min.time())

if fecha_inicio < fecha_fin:
    # Calcular
    semanas = calcular_semanas(fecha_inicio, fecha_fin)
    fechas_pago = calcular_fechas_pago(fecha_inicio, fecha_fin)
    num_pagos = len(fechas_pago)
    
    # Mostrar resultados con tarjetas
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card blue-card">
            <h2>⏰ Semanas</h2>
            <div class="value">{semanas}</div>
            <div class="label">semanas en el periodo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card green-card">
            <h2>💰 Pagos</h2>
            <div class="value">{num_pagos}</div>
            <div class="label">pagos quincenales</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calendario
    st.markdown("---")
    st.markdown("### 📆 Calendario de Pagos")
    
    # Leyenda
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item">
            <div class="legend-box" style="background: #10b981;"></div>
            <span>Día de pago</span>
        </div>
        <div class="legend-item">
            <div class="legend-box" style="background: #e0e7ff;"></div>
            <span>Dentro del periodo</span>
        </div>
        <div class="legend-item">
            <div class="legend-box" style="background: #f3f4f6;"></div>
            <span>Fuera del periodo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar meses a mostrar
    meses = []
    fecha_actual = fecha_inicio.replace(day=1)
    
    while fecha_actual <= fecha_fin:
        year = fecha_actual.year
        month = fecha_actual.month
        meses.append((year, month))
        
        if month == 12:
            fecha_actual = datetime(year + 1, 1, 1)
        else:
            fecha_actual = datetime(year, month + 1, 1)
    
    # Convertir fechas de pago a conjunto
    fechas_pago_set = {fecha.date() for fecha in fechas_pago}
    
    # Nombres de meses en español
    meses_esp = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Crear calendarios en columnas
    num_cols = 3
    for i in range(0, len(meses), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(meses):
                year, month = meses[i + j]
                with cols[j]:
                    mes_nombre = meses_esp[month]
                    
                    # Obtener información del mes
                    primer_dia_semana = calendar.monthrange(year, month)[0]
                    dias_en_mes = calendar.monthrange(year, month)[1]
                    primer_dia_semana = (primer_dia_semana + 1) % 7
                    
                    # Construir calendario HTML
                    cal_html = f'<div class="month-box"><div class="month-title">{mes_nombre} {year}</div><div class="cal-grid">'
                    
                    # Headers
                    for dia in ['D', 'L', 'M', 'M', 'J', 'V', 'S']:
                        cal_html += f'<div class="cal-day-header">{dia}</div>'
                    
                    # Días vacíos
                    for _ in range(primer_dia_semana):
                        cal_html += '<div class="cal-day"></div>'
                    
                    # Días del mes
                    for dia in range(1, dias_en_mes + 1):
                        fecha = datetime(year, month, dia).date()
                        es_pago = fecha in fechas_pago_set
                        en_rango = fecha_inicio.date() <= fecha <= fecha_fin.date()
                        
                        clase = 'cal-day'
                        if es_pago:
                            clase += ' day-payment'
                        elif en_rango:
                            clase += ' day-in-range'
                        else:
                            clase += ' day-out-range'
                        
                        cal_html += f'<div class="{clase}">{dia}</div>'
                    
                    cal_html += '</div></div>'
                    st.markdown(cal_html, unsafe_allow_html=True)
    
    # Lista de fechas de pago
    st.markdown("---")
    st.markdown("### 📋 Fechas de Pago Detalladas")
    
    # Traducción de días
    dias_esp = {
        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    # Crear DataFrame
    df_pagos = pd.DataFrame({
        'No.': range(1, len(fechas_pago) + 1),
        'Fecha': [fecha.strftime('%d/%m/%Y') for fecha in fechas_pago],
        'Día': [dias_esp[fecha.strftime('%A')] for fecha in fechas_pago],
        'Mes': [meses_esp[fecha.month] + ' ' + str(fecha.year) for fecha in fechas_pago]
    })
    
    st.dataframe(df_pagos, use_container_width=True, hide_index=True)
    
    # Botón de descarga
    csv = df_pagos.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Descargar fechas de pago (CSV)",
        data=csv,
        file_name=f"fechas_pago_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
else:
    st.error("⚠️ La fecha de inicio debe ser anterior a la fecha de fin")