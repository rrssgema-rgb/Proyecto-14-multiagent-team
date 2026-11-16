# Proyecto 14 – Ejercicio 1

## Equipo multiagente de atención al cliente de seguros

### 1. Objetivo

Desarrollar un equipo de dos agentes de inteligencia artificial especializados en seguros de automóvil, capaces de colaborar para responder consultas de asegurados utilizando documentación real de una póliza.

El ejercicio reproduce un flujo de trabajo en el que un agente investiga la documentación y otro redacta la respuesta final.

### 2. Framework utilizado

Se ha utilizado **LangGraph** para coordinar los dos agentes mediante un grafo de ejecución secuencial.

Se ha elegido este framework porque permite definir los nodos, las conexiones y el estado compartido entre agentes, controlando cómo se transfiere la información durante el proceso.

### 3. Arquitectura del equipo

El equipo está formado por dos agentes:

**Agente 1 – Investigador de seguros**
- Analiza las seis páginas de una póliza de automóvil anonimizada.
- Identifica información relacionada con la cobertura de lunas y parabrisas.
- Recoge los hallazgos documentales y los organiza por página.
- Transfiere la investigación al segundo agente.

**Agente 2 – Redactor de seguros**
- Recibe la investigación del primer agente.
- Interpreta la información recuperada.
- Redacta una respuesta clara y comprensible para el asegurado.
- Diferencia la información confirmada de aquella que no se ha podido verificar.

### 4. Flujo de ejecución

El flujo se implementa mediante LangGraph:

1. Inicio del proceso.
2. Ejecución del agente investigador.
3. Transferencia de la investigación mediante el estado compartido.
4. Ejecución del agente redactor.
5. Generación de la respuesta final.

### 5. Caso práctico

**Consulta del asegurado:**

¿Qué cubre mi seguro si se rompe el parabrisas del vehículo?

**Documentación utilizada:**

Seis páginas anonimizadas de una póliza de automóvil.

**Modelos utilizados:**
- Qwen2.5VL 3B: análisis visual de las páginas de la póliza.
- Llama 3.1 8B: elaboración de la respuesta al asegurado.

### 6. Estructura del proyecto

```text
multiagent-team/
│
├── agente_seguros_langgraph.py
├── requirements.txt
├── README.md
│
├── data/
│   └── poliza_anonimizada/
│       ├── poliza_anonimizada_pag1.png
│       ├── poliza_anonimizada_pag2.png
│       ├── poliza_anonimizada_pag3.png
│       ├── poliza_anonimizada_pag4.png
│       ├── poliza_anonimizada_pag5.png
│       └── poliza_anonimizada_pag6.png
│
├── evidencias/
│
└── salidas/
    └── ejercicio1_seguros.txt
```

### 7. Instalación y ejecución

Requisitos previos:
- Python.
- Ollama.
- Los modelos Qwen2.5VL 3B y Llama 3.1 8B.

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

Descarga de los modelos, si todavía no están instalados:

```bash
ollama pull qwen2.5vl:3b
ollama pull llama3.1:8b
```

Ejecución:

```bash
python agente_seguros_langgraph.py
```

### 8. Resultado

La ejecución genera una respuesta final al asegurado y guarda el resultado en:

`salidas/ejercicio1_seguros.txt`

Las capturas de pantalla de la ejecución se encuentran en la carpeta `evidencias/`.

### 9. Conclusión

El ejercicio demuestra la colaboración entre dos agentes especializados mediante LangGraph. El investigador se encarga de recuperar información documental y el redactor utiliza esos resultados para elaborar una respuesta orientada a la atención al cliente de seguros.