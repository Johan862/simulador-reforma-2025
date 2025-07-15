import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Simulador Costos por Reforma Laboral", layout="centered")
st.title("📊 Simulador de Costos Laborales por Reforma (2025–2027)")

st.markdown("""
Este simulador proyecta los **costos laborales mensuales** de una planta 24/7 desde **enero de 2025 hasta diciembre de 2027**, considerando la reducción progresiva de las horas laborales mensuales por la reforma laboral en Colombia.

🧮 Fórmulas basadas en:
- Salario mensual ingresado
- Horas semanales por tipo de hora (supuestas constantes)
- Cálculo automático de valor hora según el periodo

""")

with st.form("formulario"):
    salario_mensual = st.number_input("💰 Salario mensual base ($)", value=1300000.0, step=50000.0)
    empleados = st.number_input("👥 Número de empleados", value=6, step=1)

    st.markdown("### ⏱️ Horas semanales por tipo de hora")
    h_ordinarias = st.number_input("Horas ordinarias", value=44.0)
    h_extra_diurna = st.number_input("Horas extra diurnas", value=0.0)
    h_nocturnas = st.number_input("Horas nocturnas", value=16.0)
    h_extra_nocturna = st.number_input("Horas extra nocturnas", value=0.0)
    h_dominical = st.number_input("Horas dominical/festiva", value=12.0)
    h_extra_dominical = st.number_input("Horas extra dominical/festiva", value=0.0)

    submitted = st.form_submit_button("Simular")

if submitted:
    fechas = pd.date_range(start="2025-01-01", end="2027-12-31", freq="MS")

    proyeccion = []

    for fecha in fechas:
        anio = fecha.year
        mes = fecha.month
        dia = fecha.day
        fecha_ref = datetime(anio, mes, 15)

        # Determinar horas base mensuales según la fecha
        if fecha < datetime(2025, 7, 16):
            horas_base = 230
        elif fecha < datetime(2026, 7, 1):
            horas_base = 220
        else:
            horas_base = 210

        valor_hora = salario_mensual / horas_base

        # Calcular horas mensuales (4.33 semanas por mes)
        factor_mes = 4.33
        hm_ordinarias = h_ordinarias * factor_mes
        hm_extra_diurna = h_extra_diurna * factor_mes
        hm_nocturnas = h_nocturnas * factor_mes
        hm_extra_nocturna = h_extra_nocturna * factor_mes
        hm_dominical = h_dominical * factor_mes
        hm_extra_dominical = h_extra_dominical * factor_mes

        # Calcular costos por tipo de hora
        costos = {
            "Ordinarias": hm_ordinarias * valor_hora * empleados,
            "Extra Diurna": hm_extra_diurna * valor_hora * 1.25 * empleados,
            "Nocturna": hm_nocturnas * valor_hora * 1.35 * empleados,
            "Extra Nocturna": hm_extra_nocturna * valor_hora * 1.75 * empleados,
            "Dominical/Festiva": hm_dominical * valor_hora * 2.00 * empleados,
            "Extra Dominical": hm_extra_dominical * valor_hora * 2.50 * empleados,
        }

        total_mes = sum(costos.values())

        proyeccion.append({
            "Mes": fecha.strftime("%Y-%m"),
            "Horas base": horas_base,
            "Valor hora": round(valor_hora, 2),
            "Costo Ordinarias": round(costos["Ordinarias"], 0),
            "Costo Extra Diurna": round(costos["Extra Diurna"], 0),
            "Costo Nocturna": round(costos["Nocturna"], 0),
            "Costo Extra Nocturna": round(costos["Extra Nocturna"], 0),
            "Costo Dominical": round(costos["Dominical/Festiva"], 0),
            "Costo Extra Dominical": round(costos["Extra Dominical"], 0),
            "Costo Total Mes": round(total_mes, 0)
        })

    df = pd.DataFrame(proyeccion)

    st.subheader("📅 Proyección Mensual de Costos (2025–2027)")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Evolución del Costo Total Mensual")
    st.line_chart(df.set_index("Mes")["Costo Total Mes"])

    st.success("✅ Simulación completada correctamente")
