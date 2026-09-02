# Simulación de Bioprocesos 

Este proyecto contiene un entorno de simulación para modelar el proceso de fermentación de residuos agroindustriales, basado en los datos recopilados en la bitácora de diseño de biorreactores.

## Contenido

* `simulacion.py`: Script principal de Python que utiliza `scipy.integrate.odeint` para resolver las ecuaciones diferenciales del modelo cinético de Monod. Simula el crecimiento de biomasa, consumo de sustrato (grados Brix) y producción (alcohol/ésteres) a lo largo del tiempo.
* `requirements.txt`: Dependencias del entorno de simulación (`numpy`, `scipy`, `matplotlib`, `pandas`).
* `biorxiv_results.json`: Resultados de la búsqueda de literatura relacionada con biorreactores y escalado, obtenida de bioRxiv.

## Uso

1. Crear un entorno virtual de Python y activarlo:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la simulación:
   ```bash
   python simulacion.py
   ```

Esto generará un gráfico `simulacion_batch_20L.png` que muestra la curva de fermentación.

## Objetivos del Modelo

- Predecir el comportamiento del biorreactor en la fase de 20L y proyectar el escalado a digestores de 200L.
- Evaluar el impacto de variables clave identificadas durante el proceso, como la concentración de azúcares y el rendimiento del inóculo.
