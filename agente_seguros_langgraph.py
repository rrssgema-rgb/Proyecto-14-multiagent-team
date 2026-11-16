
from typing import TypedDict
from pathlib import Path
import base64
import time

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).parent
CARPETA_DATOS = BASE_DIR / "data" / "poliza_anonimizada"
CARPETA_SALIDAS = BASE_DIR / "salidas"

CARPETA_SALIDAS.mkdir(exist_ok=True)

MODELO_VISION = "qwen2.5vl:3b"
MODELO_REDACCION = "llama3.1:8b"

CONSULTA = (
    "¿Qué cubre mi seguro si se rompe el parabrisas del vehículo?"
)

investigador_llm = ChatOllama(
    model=MODELO_VISION,
    temperature=0
)

redactor_llm = ChatOllama(
    model=MODELO_REDACCION,
    temperature=0.2
)


# ============================================================
# ESTADO COMPARTIDO
# ============================================================

class EstadoEquipo(TypedDict):
    consulta: str
    investigacion: str
    respuesta: str


# ============================================================
# AGENTE 1: INVESTIGADOR DE SEGUROS
# ============================================================


def investigador(estado: EstadoEquipo):

    print("\n" + "=" * 55)
    print("AGENTE 1: INVESTIGADOR DE SEGUROS")
    print("=" * 55)

    # Localizar las seis páginas anonimizadas de la póliza
    imagenes = sorted(
        CARPETA_DATOS.glob("poliza_anonimizada_pag*.png")
    )

    if not imagenes:
        raise FileNotFoundError(
            f"No se encuentran imágenes en {CARPETA_DATOS}"
        )

    investigaciones = []

    # Analizar cada página por separado para evitar superar
    # el límite de contexto del modelo
    for imagen in imagenes:

        numero_pagina = imagen.stem[-1]

        print(
            f"Investigador: analizando página {numero_pagina}"
        )

        imagen_base64 = base64.b64encode(
            imagen.read_bytes()
        ).decode("utf-8")

        prompt = f"""
Analiza esta página de una póliza de automóvil.

Consulta del cliente:
{estado['consulta']}

Busca y transcribe literalmente cualquier información relacionada con:
- Lunas, cristales y parabrisas.
- Reposición o reparación de lunas.
- Condiciones y límites de esa cobertura.
- Exclusiones relacionadas con los cristales.

Es imprescindible revisar todas las páginas.
Indica siempre el número de página y las palabras
exactas que aparecen en el documento.

Si encuentras información como "Lunas: Su reposición",
debes recogerla literalmente.

No concluyas que una cobertura no existe sin haber
comprobado todas las páginas.
No inventes condiciones que no aparezcan en la póliza.
Indica el número de página {numero_pagina}.
No inventes información ni reproduzcas datos personales.
Si la página no contiene información relevante, indícalo.
"""

        mensaje = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{imagen_base64}"
                    }
                }
            ]
        )

        # Una llamada independiente al modelo por cada página
        resultado = investigador_llm.invoke([mensaje])

        investigaciones.append(
            f"PÁGINA {numero_pagina}:\n{resultado.content}"
        )

    investigacion = "\n\n".join(investigaciones)

    print("Investigador: análisis documental terminado.")
    print("Investigador: entregando resultados al redactor.")

    return {
        "investigacion": investigacion
    }


# ============================================================
# AGENTE 2: REDACTOR DE SEGUROS
# ============================================================


def redactor(estado: EstadoEquipo):

    print("\n" + "=" * 55)
    print("AGENTE 2: REDACTOR DE SEGUROS")
    print("=" * 55)

    print("Redactor: información recibida del investigador.")
    print("Redactor: preparando respuesta al asegurado.")

    prompt = f"""
Eres un asistente de atención al cliente especializado
en seguros de automóvil.

CONSULTA DEL ASEGURADO:
{estado['consulta']}

INVESTIGACIÓN DOCUMENTAL REALIZADA POR EL AGENTE 1:
{estado['investigacion']}

Tu tarea es responder a la consulta utilizando los
resultados de la investigación documental.

INSTRUCCIONES OBLIGATORIAS:

1. Lee todos los resultados de las páginas analizadas.

2. Identifica cualquier referencia a lunas, cristales
   o parabrisas.

3. Si aparece el texto "Lunas: Su reposición",
   debes mencionarlo expresamente e indicar la página
   donde aparece.

4. Explica únicamente lo que permite afirmar el texto
   de la póliza.

5. No confundas la reposición con una cobertura
   ilimitada ni inventes condiciones.

6. Indica claramente qué condiciones, límites o
   exclusiones no se han podido confirmar.

7. Si falta información para responder completamente,
   recomienda consultar las condiciones generales
   o a la aseguradora.

8. No afirmes que una cobertura no existe si aparece
   mencionada en la documentación.

9. Utiliza exclusivamente la información facilitada
   por el investigador. No inventes información.

10. No incluyas datos personales del asegurado.

Redacta una respuesta profesional, clara y breve,
dirigida directamente al asegurado.

Incluye las páginas que respaldan la respuesta.
"""

    resultado = redactor_llm.invoke(prompt)

    respuesta = resultado.content

    print("Redactor: respuesta terminada.")

    return {
        "respuesta": respuesta
    }


# ============================================================
# CONSTRUCCIÓN DEL GRAFO LANGGRAPH
# ============================================================

grafo = StateGraph(EstadoEquipo)

grafo.add_node("investigador", investigador)
grafo.add_node("redactor", redactor)

grafo.add_edge(START, "investigador")
grafo.add_edge("investigador", "redactor")
grafo.add_edge("redactor", END)

equipo = grafo.compile()


# ============================================================
# EJECUCIÓN DEL EQUIPO
# ============================================================

if __name__ == "__main__":

    inicio = time.time()

    print("\n" + "=" * 55)
    print("PROYECTO 14 - EJERCICIO 1")
    print("EQUIPO MULTIAGENTE DE SEGUROS")
    print("=" * 55)

    print(f"\nConsulta: {CONSULTA}")

    resultado = equipo.invoke({
        "consulta": CONSULTA,
        "investigacion": "",
        "respuesta": ""
    })

    duracion = time.time() - inicio

    print("\n" + "=" * 55)
    print("RESPUESTA FINAL AL ASEGURADO")
    print("=" * 55)

    print(resultado["respuesta"])

    # Guardar resultado final
    archivo = CARPETA_SALIDAS / "ejercicio1_seguros.txt"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("PROYECTO 14 - EJERCICIO 1\n")
        f.write("EQUIPO DE DOS AGENTES DE SEGUROS\n\n")
        f.write(f"Consulta: {CONSULTA}\n\n")
        f.write("RESPUESTA FINAL\n")
        f.write(resultado["respuesta"])
        f.write(f"\n\nTiempo de ejecución: {duracion:.2f} segundos\n")

    print("\n" + "=" * 55)
    print("EJECUCIÓN FINALIZADA")
    print("=" * 55)
    print(f"Tiempo: {duracion:.2f} segundos")
    print(f"Resultado guardado en: {archivo}")
