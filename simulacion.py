import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros cinéticos (Estimados para levadura en jugo de piña)
# Ajustables según los datos experimentales de la Bitácora
mu_max = 0.3    # Tasa máxima de crecimiento (1/h)
Ks = 2.5        # Constante de semisaturación (g/L)
Yxs = 0.1       # Rendimiento de biomasa por sustrato (g X / g S)
Yps = 0.4       # Rendimiento de producto (alcohol/ésteres) por sustrato (g P / g S)

# Modelo del biorreactor (Batch)
def modelo_biorreactor(y, t):
    X, S, P = y
    
    # Ecuación de Monod para la tasa de crecimiento específico
    mu = mu_max * S / (Ks + S)
    
    # Ecuaciones diferenciales
    dXdt = mu * X
    dSdt = -(1/Yxs) * mu * X
    dPdt = Yps * (1/Yxs) * mu * X
    
    return [dXdt, dSdt, dPdt]

# Condiciones iniciales (Fase 2 - Biorreactores de 20L)
X0 = 0.1        # Biomasa inicial (inoculo) en g/L
S0 = 150.0      # Sustrato inicial (aprox. 15 Brix o 150 g/L de azúcares)
P0 = 0.0        # Producto inicial en g/L

y0 = [X0, S0, P0]

# Vector de tiempo (15 días de fermentación = 360 horas)
t = np.linspace(0, 360, 500)

# Resolver sistema de EDOs
sol = odeint(modelo_biorreactor, y0, t)
X = sol[:, 0]
S = sol[:, 1]
P = sol[:, 2]

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(t/24, X, label='Biomasa (X) [g/L]', color='green')
plt.plot(t/24, S, label='Sustrato (S) [g/L]', color='blue')
plt.plot(t/24, P, label='Producto (P) [g/L]', color='red')

plt.title('Simulación de Fermentación Batch (Biorreactor 20L)')
plt.xlabel('Tiempo (Días)')
plt.ylabel('Concentración (g/L)')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Guardar figura
plt.savefig('simulacion_batch_20L.png')
print("Simulación completada. Gráfico guardado como 'simulacion_batch_20L.png'.")
