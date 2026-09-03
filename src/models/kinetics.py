import numpy as np

class FermentationKinetics:
    def __init__(self, mu_max: float = 0.3, Ks: float = 2.5, Yxs: float = 0.1, Yps: float = 0.4, kd: float = 0.01):
        """
        Modelo de cinética de fermentación.
        mu_max: Tasa máxima de crecimiento específico (1/h)
        Ks: Constante de semisaturación de Monod (g/L)
        Yxs: Rendimiento biomasa/sustrato (g X / g S)
        Yps: Rendimiento producto/sustrato (g P / g S)
        kd: Tasa de muerte celular (1/h)
        """
        if mu_max < 0 or Ks <= 0 or Yxs <= 0 or Yps < 0 or kd < 0:
            raise ValueError("Parámetros cinéticos inválidos.")
            
        self.mu_max = float(mu_max)
        self.Ks = float(Ks)
        self.Yxs = float(Yxs)
        self.Yps = float(Yps)
        self.kd = float(kd)

    def get_derivatives(self, y, t):
        """
        Ecuaciones diferenciales para modelo batch.
        y = [X, S, P]
        """
        X, S, P = y
        
        # Ecuación de Monod
        mu = self.mu_max * (S / (self.Ks + S))
        
        # Cambio en biomasa (Crecimiento - Muerte)
        dXdt = (mu - self.kd) * X
        
        # Consumo de sustrato (Asociado al crecimiento de biomasa)
        if S > 0:
            dSdt = -(1/self.Yxs) * mu * X
        else:
            dSdt = 0
            
        # Formación de producto (Ecuación tipo Luedeking-Piret, aquí simplificada a asociado al crecimiento)
        dPdt = self.Yps * (1/self.Yxs) * mu * X
        
        return [dXdt, dSdt, dPdt]
