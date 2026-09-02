# Simulación de Bioprocesos y Biorreactores

Este proyecto contiene un entorno de simulación en Python para modelar un proceso de fermentación genérico a partir de residuos orgánicos agrícolas, y sirve como **referencia técnica para el escalado de biorreactores (ej. 20L a 200L)**.

## Estructura del Proyecto

* `src/core/scale_up.py`: Módulo para el cálculo de variables críticas de escalado manteniendo similitud geométrica. Incluye:
  * Escalado por **Potencia/Volumen (P/V) constante** (recomendado para mantener turbulencia/transferencia de masa).
  * Escalado por **Velocidad de punta del impulsor ($v_{tip}$) constante** (recomendado para células sensibles a cizallamiento).
  * Ecuaciones para mantener **$k_L a$ (Coeficiente volumétrico de transferencia de oxígeno)** constante.
  * Cálculo de **Tiempo de Mezcla ($t_m$)** mediante número de mezcla adimensional.
  * Estimación de la relación **Área de Enfriamiento / Volumen ($A/V$)**, crucial para anticipar problemas de transferencia de calor en bioprocesos exotérmicos.
* `src/models/kinetics.py`: Módulo con el modelo matemático basado en cinética de Monod y Luedeking-Piret (modificado) para modelar crecimiento de biomasa, consumo de sustrato (grados Brix) y formación de producto.
* `src/models/consortium.py`: Simulador estequiométrico-empírico de consorcios microbianos. Permite estimar la composición final del bioproducto (ej. Etanol, Ácido Láctico, Aminoácidos) en base al perfil de la materia prima (*feedstock*) y los microorganismos inoculados (ej. *Levaduras, Lactobacillus, Bacillus*).
* `escalado_main.py`: Script de ejecución principal que genera el reporte de escalado físico y las curvas cinéticas.
* `herramienta_composicion.py`: Script para ejecutar escenarios comparativos sobre el consorcio biológico y predecir perfiles de bioproductos finales (Biol, fertilizantes, etc.).
* `simulacion.py`: Script original de la curva de fermentación en un solo archivo.

## Teoría de Escalado Implementada

Al escalar de un reactor piloto (20L) a uno industrial (200L), no es posible mantener todas las variables físicas constantes simultáneamente (mezcla, corte, transferencia de calor). Este entorno permite proyectar cuál es la velocidad de agitación (rpm) óptima en la escala mayor dependiendo del criterio elegido:
- Si se mantiene $P/V$ constante, el tiempo de mezcla aumentará, pero la transferencia de gas-líquido ($k_L a$) será similar.
- Si se mantiene $v_{tip}$ constante, se reduce el daño celular, pero la mezcla puede ser deficiente.

## Uso

1. Crear un entorno virtual de Python e instalar las dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ejecutar el análisis de escalado:
   ```bash
   python escalado_main.py
   ```
