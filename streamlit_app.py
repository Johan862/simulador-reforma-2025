import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Simulador Costos por Año", layout="centered")
st.title("📅 Simulador de Costos Laborales por Reforma (por Año)")

# Año a simular
anio_seleccionado = st.selectbox("Selecciona el año a simular", [2025, 2026, 2027])

st.markdown("### 👥 Datos de empleados")

num_empleados = st.number_input("Número de empleados", min_value=1, value=2, step=1)
empleados = []

for i in range(num_empleados):
    with st.expander(f"👤 Empleado {i + 1}"):
        nombre = st.text_input(f"Nombre del empleado {i + 1}", value=f"Empleado {i + 1}", key=f"emp_nombre_{i}")
        salario = st.number_input(f"💰 Salario mensual de {nombre}", value=1300000.0, step=50000.0, key=f"emp_sal_{i}")
        auxilio = st.number_input(f"🚍 Auxilio de transporte mensual de {nombre}", value=140606.0, step=1000.0, key=f"emp_aux_{i}")

        horas_por_mes = {}
        for mes in range(1, 13):
            label = f"{anio_seleccionado}-{mes:02d}"
            with st.expander(f"🗓️ {label} - Horas de {nombre}"):
                horas_por_mes[label] = {
                    "ordinarias": st.number_input(f"Horas ordinarias ({label})", value=176.0, key=f"{nombre}_{label}_ord"),
                    "extra_diurna": st.number_input(f"Horas extra diurnas ({label})", value=0.0, key=f"{nombre}_{label}_extd"),
                    "nocturnas": st.number_input(f"Horas nocturnas ({label})", value=16.0, key=f"{nombre}_{label}_n"),
                    "extra_nocturna": st.number_input(f"Horas extra nocturnas ({label})", value=0.0, key=f"{nombre}_{label}_extn"),
                    "dominical": st.number_input(f"Horas dominicales/festivas ({label})", value=12.0, key=f"{nombre}_{label}_df"),
                    "extra_dominical": st.number_input(f"Horas extra dominicales ({label})", value=0.0, key=f"{nombre}_{label}_edf"),
                }

        empleados.append({
            "nombre": nombre,
            "salario": salario,
            "auxilio": auxilio,
            "horas_por_mes": horas_por_mes
        })

if st.button("Simular"):
    resultados = []

    for emp in empleados:
        for mes in range(1, 13):
            label = f"{anio_seleccionado}-{mes:02d}"
            fecha = datetime(anio_seleccionado, mes, 1)

            # Horas base según la fecha
            if fecha < datetime(2025, 7, 16):
                horas_base = 230
            elif fecha < datetime(2026, 7, 1):
                horas_base = 220
            else:
                horas_base = 210

            valor_hora = emp["salario"] / horas_base

            horas = emp["horas_por_mes"][label]

            # Cálculo por tipo
            costos = {
                "ordinarias": horas["ordinarias"] * valor_hora,
                "extra_diurna": horas["extra_diurna"] * valor_hora * 1.25,
                "nocturna": horas["nocturnas"] * valor_hora * 1.35,
                "extra_nocturna": horas["extra_nocturna"] * valor_hora * 1.75,
                "dominical": horas["dominical"] * valor_hora * 2.00,
                "extra_dominical": horas["extra_dominical"] * valor_hora * 2.50,
            }

            subtotal = sum(costos.values())
            parafiscales = subtotal * 1.52
            total_mes = subtotal + parafiscales + emp["auxilio"]

            resultados.append({
                "Empleado": emp["nombre"],
                "Mes": label,
                "Valor hora": round(valor_hora, 2),
                "Horas base": horas_base,
                "Subtotal": round(subtotal, 0),
                "Auxilio": round(emp["auxilio"], 0),
                "Parafiscales (0.52)": round(parafiscales, 0),
                "Total mes": round(total_mes, 0)
            })

    df = pd.DataFrame(resultados)
    st.subheader(f"📊 Resultados simulación {anio_seleccionado}")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Evolución del Costo Total Mensual por Empleado")
    for emp in df["Empleado"].unique():
        df_emp = df[df["Empleado"] == emp]
        st.line_chart(df_emp.set_index("Mes")[["Total mes"]], height=250, use_container_width=True)

    st.success("✅ Simulación finalizada correctamente")

