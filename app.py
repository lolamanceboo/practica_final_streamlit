import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px #Para gráficas interactivas 

#Carga de los datasets
url_parte_1 = "https://github.com/lolamanceboo/practica_final_streamlit/releases/download/v1.0/parte_1.csv"
url_parte_2 = "https://github.com/lolamanceboo/practica_final_streamlit/releases/download/v1.0/parte_2.csv"

df1 = pd.read_csv(url_parte_1)
df2 = pd.read_csv(url_parte_2)

#Concatenación vertical de ambos datasets 
df = pd.concat([df1, df2], axis=0) 

#Reiniciar el índice tras la concatenación
df.reset_index(drop=True, inplace=True)

#Conversión de la columna fecha a formato datetime
df["date"] = pd.to_datetime(df["date"])


#Organizar la información en pestañas interactivas
p1, p2, p3, p4 = st.tabs(["Visualización global", "Tienda", "Estado", "Análisis adicional"])


################################## PESTAÑA 1 ##################################
with p1:

    st.header("VISUALIZACIÓN GLOBAL DE LA SITUACIÓN DE LAS VENTAS")

    #------------------------------------------------------------------------------------

    #APARTADO a. Conteo general con los siguientes datos
    st.write("\n")
    st.subheader("CONTEOS GENERALES")

    #Uso de columnas para organizar KPIs horizontalmente 
    col1, col2, col3, col4 = st.columns(4)

    #KPI 1 (i. Número total de tiendas) 
    col1.metric(label="**Número total de tiendas**", value=df["store_nbr"].nunique())

    #KPI 2 (ii. Número total de productos que se venden) 
    col2.metric(label="**Número total de productos que se venden**", value=df["family"].nunique())

    #KPI 3 (iii. Estados en los que opera la empresa) 
    col3.metric(label="**Estados en los que opera la empresa**", value=df["state"].nunique())

    #KPI 4: (iv. Meses de los que se disponen datos para realizar el informe) 
    col4.metric(label="**Meses de los que se disponen datos para realizar el informe**", value=df["month"].nunique())

    #------------------------------------------------------------------------------------

    #APARTADO b. Análisis en términos medios de los siguientes datos
    st.write("\n")
    st.subheader("ANÁLISIS MEDIO DE VENTAS") 

    #(i. Ranking (top 10) de los productos más vendidos)
    st.write("\n")
    st.markdown("**Top 10 de los productos más vendidos**")

    #Agrupación y suma de ventas por producto
    top10_products = (df.groupby("family")["sales"].sum().sort_values(ascending=False).head(10))

    #Mostrar tabla
    st.dataframe(top10_products)

    #Mostrar gráfico de barras automático
    st.bar_chart(top10_products)

    #(ii. Distribución de las ventas por tiendas)
    st.write("\n")
    st.markdown("**Distribución de las ventas por tienda**")

    ventas_por_tienda = df.groupby("store_nbr")["sales"].sum()

    st.bar_chart(ventas_por_tienda)

    #(iii. Ranking (top 10) de tienes con ventas en productos en promoción)
    st.write("\n")
    st.markdown("**Top 10 de tiendas con ventas en promoción**")

    df_promos = df[df["onpromotion"] > 0]

    top10_tiendas_promos = (df_promos.groupby("store_nbr")["sales"].sum().sort_values(ascending=False).head(10))

    st.bar_chart(top10_tiendas_promos)

    #------------------------------------------------------------------------------------

    #APARTADO c. Análisis de la estacionalidad de las ventas
    st.write("\n")
    st.subheader("ESTACIONALIDAD DE LAS VENTAS")

    #(i. Día de la semana en el que se producen más ventas por término medio)
    ventas_dia_semana = df.groupby("day_of_week")["sales"].mean()

    dia_top = ventas_dia_semana.idxmax()

    st.write("\n")
    st.markdown(f"**Día con mayor media de ventas: {dia_top}**")

    st.bar_chart(ventas_dia_semana)

    #(ii. Volumen de ventas medio por semana del año de todos los años del dataset)
    st.write("\n")
    ventas_semana = df.groupby("week")["sales"].mean()
    st.line_chart(ventas_semana)

    #(iii. Volumen de ventas medio por mes en todos los años del dataset)
    st.write("\n")
    ventas_mes = df.groupby("month")["sales"].mean()
    st.bar_chart(ventas_mes)


################################## PESTAÑA 2 ##################################
with p2:

    st.header("INFORMACIÓN POR TIENDA")

    #Widget selectbox para seleccionar tienda (entrada del usuario)
    lista_tiendas = sorted(df["store_nbr"].unique())
    tienda = st.selectbox("Selecciona una tienda:", lista_tiendas)

    #Filtrado del DataFrame según la tienda elegida
    df_tienda = df[df["store_nbr"] == tienda]

    #------------------------------------------------------------------------------------

    #APARTADO a. Número total de ventas por año (ordenador de más antiguo a más reciente)
    st.write("\n")
    st.subheader("VENTAS TOTALES POR AÑO")

    ventas_anuales = (df_tienda.groupby("year")["sales"].sum().sort_index())

    st.bar_chart(ventas_anuales)

    #------------------------------------------------------------------------------------

    #APARTADO b. Número total de productos vendidos
    st.write("\n")
    st.subheader("NÚMERO TOTAL DE PRODUCTOS VENDIDOS")

    total_productos = df_tienda["sales"].sum()

    st.metric(label="Productos vendidos", value=f"{total_productos:.0f}")

    #------------------------------------------------------------------------------------

    #APARTADO c. Número total de productos vendidos que estaban en promoción
    st.write("\n")
    st.subheader("PRODUCTOS VENDIDOS EN PROMOCIÓN")

    productos_promocion = df_tienda[df_tienda["onpromotion"] > 0]["sales"].sum()

    st.metric(label="Productos vendidos en promoción", value=f"{productos_promocion:.0f}")


################################## PESTAÑA 3 ##################################
with p3:

    st.header("INFORMACIÓN POR ESTADO")

    #Seleccionar un estado
    lista_estados = sorted(df["state"].unique())
    estado = st.selectbox("Selecciona un estado:", lista_estados)

    #Filtrado por estado
    df_estado = df[df["state"] == estado]

    #------------------------------------------------------------------------------------

    #APARTADO a. Número total de transacciones por año
    st.write("\n")
    st.subheader("TRANSACCIONES TOTALES POR AÑO")

    transacciones_anuales = (df_estado.groupby("year")["transactions"].sum().sort_index()) 

    st.bar_chart(transacciones_anuales)

    #------------------------------------------------------------------------------------

    #APARTADO b. Ranking de tiendas con más ventas
    st.write("\n")
    st.subheader("RANKING DE TIENDAS CON MÁS VENTAS")

    ranking_tiendas = (df_estado.groupby("store_nbr")["sales"].sum().sort_values(ascending=False))

    st.dataframe(ranking_tiendas)
    st.bar_chart(ranking_tiendas.head(10))

    #------------------------------------------------------------------------------------

    #APARTADO c. Producto más vendido en la tienda
    st.write("\n")
    st.subheader("PRODUCTO MÁS VENDIDO EN LA TIENDA")

    ventas_producto = df_estado.groupby("family")["sales"].sum()

    producto_top = ventas_producto.idxmax()
    ventas_top = ventas_producto.max()

    st.metric(label="Producto más vendido", value=producto_top, delta=f"Ventas totales: {ventas_top:.0f}")


################################## PESTAÑA 4 ##################################
with p4:

    st.header("ANÁLISIS COMPLEMENTARIO PARA APOYO A DECISIONES")

    #------------------------------------------------------------------------------------
    
    #BLOQUE 1 – COMPARACIÓN DE VENTAS CON Y SIN PROMOCIÓN
    st.write("\n")
    st.subheader("**Comparación de ventas con y sin promoción**")

    #Cálculo de la venta media cuando hay promoción
    venta_media_promo = df[df["onpromotion"] > 0]["sales"].mean()

    #Cálculo de la venta media cuando no hay promoción
    venta_media_no_promo = df[df["onpromotion"] == 0]["sales"].mean()

    col1, col2 = st.columns(2)

    col1.metric(label="Venta media con promoción", value=f"{venta_media_promo:.2f}")

    col2.metric(label="Venta media sin promoción", value=f"{venta_media_no_promo:.2f}", delta=f"{venta_media_promo - venta_media_no_promo:.2f}")

    st.markdown("""
    **Conclusión:**  

    Los resultados muestran que la venta media es claramente superior cuando los productos
    se encuentran en promoción frente a cuando no lo están.  

    Esto indica que las promociones tienen un impacto positivo directo sobre el volumen
    de ventas, incentivando el consumo por parte de los clientes.  

    De cara al próximo año, se recomienda **mantener e incluso reforzar las campañas
    promocionales**, especialmente en los periodos de mayor demanda, ya que contribuyen
    a mejorar el rendimiento comercial.
    """)

    #------------------------------------------------------------------------------------
    
    #BLOQUE 2 – EFICIENCIA DE VENTAS POR ESTADO
    st.write("\n")
    st.subheader("**Eficiencia de ventas por estado**")

    #Agrupación de ventas y transacciones por estado
    eficiencia_estado = (df.groupby("state")[["sales", "transactions"]].sum().reset_index())

    #Cálculo de ventas por transacción
    eficiencia_estado["ventas_por_transaccion"] = (eficiencia_estado["sales"] / eficiencia_estado["transactions"])

    #Ordenar estados por mayor eficiencia
    eficiencia_estado = eficiencia_estado.sort_values("ventas_por_transaccion", ascending=False)

    st.dataframe(eficiencia_estado)

    fig_eficiencia = px.bar(
        eficiencia_estado,
        x="state",
        y="ventas_por_transaccion",
        title="Ventas por transacción según estado",
        labels={
            "state": "Estado",
            "ventas_por_transaccion": "Ventas por transacción"
        }
    )

    st.plotly_chart(fig_eficiencia)

    st.markdown("""
    **Conclusión:**  

    El análisis de ventas por transacción pone de manifiesto que existen diferencias
    significativas entre estados en cuanto al comportamiento de compra de los clientes.  

    Algunos estados generan un mayor volumen de ventas en cada transacción, lo que refleja
    un mayor gasto medio por cliente.  

    Estos estados presentan un **mayor potencial de rentabilidad**, por lo que conviene
    priorizarlos en futuras acciones comerciales y estrategias de crecimiento.
    """)

    #------------------------------------------------------------------------------------
    
    #BLOQUE 3 – EVOLUCIÓN TEMPORAL DE LAS VENTAS
    st.write("\n")
    st.subheader("**Evolución temporal de las ventas**")

    ventas_diarias = (df.groupby("date")["sales"].sum().reset_index())

    #Cálculo de media móvil de 7 días
    ventas_diarias["media_movil_7d"] = ventas_diarias["sales"].rolling(7).mean()

    fig_tendencia = px.line(
        ventas_diarias,
        x="date",
        y=["sales", "media_movil_7d"],
        labels={"value": "Ventas", "date": "Fecha"},
        title="Evolución diaria de las ventas con media móvil"
    )

    st.plotly_chart(fig_tendencia)

    st.markdown("""
    **Conclusión:**  

    La evolución temporal de las ventas, junto con la media móvil, muestra una tendencia
    general positiva a lo largo del tiempo, a pesar de las fluctuaciones puntuales.  

    Esto sugiere que el negocio mantiene una base sólida y un crecimiento sostenido,
    sin depender únicamente de picos aislados.  

    De cara al futuro, esta tendencia permite planificar con mayor confianza las
    estrategias comerciales y anticipar posibles escenarios de crecimiento.
    """)

    #------------------------------------------------------------------------------------
    
    #BLOQUE 4 – IDENTIFICACIÓN DE ESTADOS PRIORITARIOS
    st.write("\n")
    st.subheader("Identificación de estados prioritarios")

    #Normalización simple para comparar métricas
    eficiencia_estado["ventas_normalizadas"] = (eficiencia_estado["sales"] / eficiencia_estado["sales"].max())

    eficiencia_estado["eficiencia_normalizada"] = (eficiencia_estado["ventas_por_transaccion"] / eficiencia_estado["ventas_por_transaccion"].max())

    #Puntuación combinada
    eficiencia_estado["puntuacion_global"] = (eficiencia_estado["ventas_normalizadas"] + eficiencia_estado["eficiencia_normalizada"])

    #Selección de los 3 estados con mejor puntuación
    top_estados = eficiencia_estado.sort_values("puntuacion_global", ascending=False).head(3)

    st.dataframe(top_estados[[
        "state",
        "sales",
        "ventas_por_transaccion",
        "puntuacion_global"
    ]])

    st.markdown("""
    **Conclusión final:**  

    Al combinar el volumen total de ventas con la eficiencia medida como ventas por
    transacción, se obtiene una visión más completa del rendimiento global de cada estado.  

    Los estados con mayor puntuación destacan tanto por su capacidad de generar ventas
    como por un comportamiento de compra eficiente por parte de los clientes.  

    Estos resultados permiten identificar **estados prioritarios**, en los que resulta
    recomendable concentrar esfuerzos comerciales y estratégicos para maximizar el impacto
    de las decisiones de negocio.
    """)