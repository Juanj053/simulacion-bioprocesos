import numpy as np

class BioreactorScaleUp:
    def __init__(self, v1, v2, d_t1, d_i1, n1, vvm=1.0):
        """
        Inicializa la clase para el escalado de biorreactores.
        
        Parámetros:
        v1: Volumen del biorreactor piloto/escala menor (L)
        v2: Volumen del biorreactor industrial/escala mayor (L)
        d_t1: Diámetro del tanque menor (m)
        d_i1: Diámetro del impulsor menor (m)
        n1: Velocidad de agitación en escala menor (rpm)
        vvm: Volumen de aire por volumen de líquido por minuto (min^-1)
        """
        self.V1 = v1
        self.V2 = v2
        self.Dt1 = d_t1
        self.Di1 = d_i1
        self.N1 = n1 / 60.0  # rps
        self.vvm = vvm
        
        # Similitud geométrica
        self.scale_factor = (self.V2 / self.V1) ** (1/3)
        self.Dt2 = self.Dt1 * self.scale_factor
        self.Di2 = self.Di1 * self.scale_factor
        
        # Propiedades del fluido y del impulsor (Asumiendo turbina Rushton y agua)
        self.Np = 5.0      # Número de potencia
        self.rho = 1000.0  # Densidad (kg/m^3)

    def calculate_power_volume(self, N_rps, Di, V_liters):
        """Calcula la Potencia por unidad de Volumen (W/m^3)"""
        V_m3 = V_liters / 1000.0
        P = self.Np * self.rho * (N_rps ** 3) * (Di ** 5)
        return P / V_m3

    def calculate_kla(self, p_v, vs):
        """
        Calcula k_L a (1/s) basado en la correlación empírica de Van't Riet:
        k_L a = 0.026 * (P/V)^0.4 * (vs)^0.5
        """
        return 0.026 * (p_v ** 0.4) * (vs ** 0.5)

    def get_superficial_velocity(self, V_liters, Dt):
        """Calcula la velocidad superficial del gas vs (m/s)"""
        V_m3 = V_liters / 1000.0
        Q_gas = V_m3 * self.vvm / 60.0 # m^3/s
        Area = np.pi * ((Dt / 2.0) ** 2)
        return Q_gas / Area

    def calculate_mixing_time(self, Dt, Di, N_rps):
        """
        Calcula el tiempo de mezcla tm (s) usando la correlación empírica:
        N * tm = 1.5 * (Dt/Di)^2
        """
        # Para un régimen completamente turbulento
        return (1.5 * (Dt / Di) ** 2) / N_rps

    def calculate_cooling_area_ratio(self, Dt):
        """
        Calcula la relación Área de Enfriamiento / Volumen (A/V) en m^-1.
        Asume un tanque cilíndrico donde la altura del líquido H = 2*Dt
        """
        # A = pi * Dt * H = 2 * pi * Dt^2
        # V = pi/4 * Dt^2 * H = pi/2 * Dt^3
        # A/V = 4 / Dt
        return 4.0 / Dt

    def constant_power_volume(self):
        """Retorna la velocidad de agitación (rpm) para la escala mayor manteniendo P/V"""
        N2 = self.N1 * (self.scale_factor ** (-2/3))
        return N2 * 60.0

    def constant_tip_speed(self):
        """Retorna la velocidad de agitación (rpm) para la escala mayor manteniendo v_tip"""
        N2 = self.N1 * (self.Di1 / self.Di2)
        return N2 * 60.0

    def generate_report(self):
        N2_pv = self.constant_power_volume() / 60.0
        N2_tip = self.constant_tip_speed() / 60.0
        
        # Variables escala 1
        pv1 = self.calculate_power_volume(self.N1, self.Di1, self.V1)
        vs1 = self.get_superficial_velocity(self.V1, self.Dt1)
        kla1 = self.calculate_kla(pv1, vs1)
        tm1 = self.calculate_mixing_time(self.Dt1, self.Di1, self.N1)
        av1 = self.calculate_cooling_area_ratio(self.Dt1)
        
        # Variables escala 2 (Manteniendo P/V)
        pv2_pv = self.calculate_power_volume(N2_pv, self.Di2, self.V2)
        vs2 = self.get_superficial_velocity(self.V2, self.Dt2)
        kla2_pv = self.calculate_kla(pv2_pv, vs2)
        tm2_pv = self.calculate_mixing_time(self.Dt2, self.Di2, N2_pv)
        av2 = self.calculate_cooling_area_ratio(self.Dt2)
        
        # Variables escala 2 (Manteniendo v_tip)
        pv2_tip = self.calculate_power_volume(N2_tip, self.Di2, self.V2)
        kla2_tip = self.calculate_kla(pv2_tip, vs2)
        tm2_tip = self.calculate_mixing_time(self.Dt2, self.Di2, N2_tip)

        report = f"--- Reporte Avanzado de Escalado ({self.V1}L -> {self.V2}L) ---\n"
        report += f"Factor geométrico: {self.scale_factor:.2f} | Aireación: {self.vvm} VVM\n"
        report += f"Área de enfriamiento vs Volumen (A/V) cae de {av1:.1f} m^-1 a {av2:.1f} m^-1\n"
        report += f"-> Nota: El biorreactor industrial tendrá una capacidad de enfriamiento mucho menor por cada litro.\n"
        
        report += f"\n[Escala Piloto - {self.V1}L]\n"
        report += f"Agitación: {self.N1*60:.0f} rpm | P/V: {pv1:.1f} W/m^3 | k_La: {kla1*3600:.1f} h^-1 | Tiempo Mezcla: {tm1:.1f} s\n"
        
        report += f"\n[Escala Industrial - {self.V2}L : Criterio P/V Constante]\n"
        report += f"Agitación: {N2_pv*60:.0f} rpm | P/V: {pv2_pv:.1f} W/m^3 | k_La: {kla2_pv*3600:.1f} h^-1 | Tiempo Mezcla: {tm2_pv:.1f} s\n"
        report += f"-> Impacto: k_La aumenta por mayor vs. El tiempo de mezcla (t_m) empeora al ser un tanque mayor.\n"
        
        report += f"\n[Escala Industrial - {self.V2}L : Criterio v_tip Constante]\n"
        report += f"Agitación: {N2_tip*60:.0f} rpm | P/V: {pv2_tip:.1f} W/m^3 | k_La: {kla2_tip*3600:.1f} h^-1 | Tiempo Mezcla: {tm2_tip:.1f} s\n"
        report += f"-> Impacto: Fuerte caída en P/V. El tiempo de mezcla se vuelve críticamente lento.\n"
        
        return report

if __name__ == "__main__":
    # Ejemplo: 20L a 200L
    # Parámetros asumidos para 20L: Diámetro tanque 0.3m, Diámetro impulsor 0.1m, 300 rpm
    scaler = BioreactorScaleUp(20, 200, 0.3, 0.1, 300)
    print(scaler.generate_report())
