import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos(ruta_archivo):
    try:
        return pd.read_csv(ruta_archivo)
    except FileNotFoundError:
        st.error("No se encontró el archivo CSV en la ruta especificada.")
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
    return None

def mostrar_interfaz():
    st.title("Herramienta de Análisis de Datos")

    # Subir archivo CSV
    archivo_csv = st.file_uploader("Subir archivo CSV", type=["csv"])

    if archivo_csv is not None:
        datos = cargar_datos(archivo_csv)
        if datos is not None:
            st.write("Vista preliminar de los datos:")
            st.write(datos.head(10))

            columnas_seleccionadas = st.multiselect("Seleccionar columnas para estadísticas:", datos.columns)
            if columnas_seleccionadas:
                columnas_numericas = datos[columnas_seleccionadas].select_dtypes(include=['int64', 'float64'])
                if not columnas_numericas.empty:
                    estadisticas = columnas_numericas.describe().loc[['mean', '50%', 'std']]
                    estadisticas.rename(index={'mean': 'MedArit', '50%': 'Med', 'std': 'DesvEst'}, inplace=True)
                    st.write("Estadísticas descriptivas para las columnas seleccionadas:")
                    st.write(estadisticas)
                else:
                    st.warning("No se seleccionaron columnas numéricas en los datos cargados.")
            else:
                st.warning("No se seleccionaron columnas para calcular estadísticas.")

if __name__ == "__main__":
    mostrar_interfaz()
