import numpy as np

class BioreactorScaleUp:
    def __init__(self, v1, v2, d_t1, d_i1, n1):
        """
        Inicializa la clase para el escalado de biorreactores.
        
        Parámetros:
        v1: Volumen del biorreactor piloto/escala menor (L)
        v2: Volumen del biorreactor industrial/escala mayor (L)
        d_t1: Diámetro del tanque menor (m)
        d_i1: Diámetro del impulsor menor (m)
        n1: Velocidad de agitación en escala menor (rpm)
        """
        self.V1 = v1
        self.V2 = v2
        self.Dt1 = d_t1
        self.Di1 = d_i1
        self.N1 = n1 / 60.0  # Convertir a rps
        
        # Similitud geométrica
        self.scale_factor = (self.V2 / self.V1) ** (1/3)
        self.Dt2 = self.Dt1 * self.scale_factor
        self.Di2 = self.Di1 * self.scale_factor

    def constant_power_volume(self):
        """
        Escalado manteniendo la Potencia por unidad de Volumen constante (P/V).
        Ideal para mantener un nivel similar de turbulencia y mezcla.
        Retorna la velocidad de agitación (rpm) para la escala mayor.
        """
        # (N1^3 * Di1^2) = (N2^3 * Di2^2) -> simplificación para régimen turbulento (Np constante)
        N2 = self.N1 * (self.scale_factor ** (-2/3))
        return N2 * 60.0 # a rpm

    def constant_tip_speed(self):
        """
        Escalado manteniendo la velocidad de punta del impulsor constante (v_tip).
        Crucial para células sensibles al estrés de corte (cizallamiento).
        Retorna la velocidad de agitación (rpm) para la escala mayor.
        """
        # N1 * Di1 = N2 * Di2
        N2 = self.N1 * (self.Di1 / self.Di2)
        return N2 * 60.0 # a rpm

    def constant_kla(self):
        """
        Escalado asumiendo un k_L a constante.
        k_L a depende de (P/V)^alpha y de la velocidad superficial del gas (Vs)^beta.
        Esta es una estimación simplificada donde k_L a está muy ligado a P/V.
        Usualmente resulta en parámetros similares a P/V constante.
        """
        return self.constant_power_volume()

    def generate_report(self):
        report = f"--- Reporte de Escalado ({self.V1}L -> {self.V2}L) ---\n"
        report += f"Factor de escala geométrico: {self.scale_factor:.2f}\n"
        report += f"Diámetro del tanque (escala mayor): {self.Dt2:.3f} m\n"
        report += f"Diámetro del impulsor (escala mayor): {self.Di2:.3f} m\n"
        report += f"Velocidad de agitación (P/V constante): {self.constant_power_volume():.1f} rpm\n"
        report += f"Velocidad de agitación (v_tip constante): {self.constant_tip_speed():.1f} rpm\n"
        return report

if __name__ == "__main__":
    # Ejemplo: 20L a 200L
    # Parámetros asumidos para 20L: Diámetro tanque 0.3m, Diámetro impulsor 0.1m, 300 rpm
    scaler = BioreactorScaleUp(20, 200, 0.3, 0.1, 300)
    print(scaler.generate_report())
