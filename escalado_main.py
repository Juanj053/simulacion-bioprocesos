from src.core.scale_up import BioreactorScaleUp
from src.models.kinetics import FermentationKinetics
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np

def run_scale_up_analysis():
    print("Iniciando análisis de escalado de Biorreactor (20L a 200L)...\n")
    
    # 1. Análisis Geométrico y Dinámico
    # Asumimos parámetros de un tanque agitado estándar (relación H/D = 2, Di/Dt = 0.33)
    escala_menor_vol = 20
    escala_mayor_vol = 200
    
    # Estimación de diámetro para tanque cilíndrico de 20L
    # V = pi * (Dt/2)^2 * H -> H = 2Dt -> V = pi/2 * Dt^3 -> Dt = (2V/pi)^(1/3)
    v_m3 = escala_menor_vol / 1000
    dt_20 = (2 * v_m3 / np.pi) ** (1/3)
    di_20 = dt_20 / 3.0
    rpm_20 = 400 # rpm base
    
    scaler = BioreactorScaleUp(escala_menor_vol, escala_mayor_vol, dt_20, di_20, rpm_20)
    print(scaler.generate_report())
    
    # 2. Simulación Cinética
    kinetics = FermentationKinetics(mu_max=0.35, Ks=3.0, Yxs=0.15, Yps=0.45, kd=0.015)
    
    # Condiciones iniciales
    y0 = [0.1, 150.0, 0.0] # [Biomasa g/L, Sustrato g/L, Producto g/L]
    t = np.linspace(0, 360, 500) # 15 días (360 horas)
    
    sol = odeint(kinetics.get_derivatives, y0, t)
    
    # Graficar
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(t/24, sol[:, 0], 'g-', label='Biomasa (X)')
    plt.plot(t/24, sol[:, 2], 'r-', label='Producto (P)')
    plt.xlabel('Tiempo (Días)')
    plt.ylabel('Concentración (g/L)')
    plt.title('Cinética de Fermentación')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(t/24, sol[:, 1], 'b-', label='Sustrato (S)')
    plt.xlabel('Tiempo (Días)')
    plt.ylabel('Concentración (g/L)')
    plt.title('Consumo de Sustrato')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('escalado_cinetica.png')
    print("Gráfica de cinética guardada como 'escalado_cinetica.png'.")

if __name__ == "__main__":
    run_scale_up_analysis()
