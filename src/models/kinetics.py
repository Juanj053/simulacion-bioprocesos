import numpy as np

class FermentationKinetics:
    def __init__(self, mu_max=0.3, Ks=2.5, Yxs=0.1, Yps=0.4, kd=0.01):
        """
        Modelo de cinética de fermentación.
        mu_max: Tasa máxima de crecimiento específico (1/h)
        Ks: Constante de semisaturación de Monod (g/L)
        Yxs: Rendimiento biomasa/sustrato (g X / g S)
        Yps: Rendimiento producto/sustrato (g P / g S)
        kd: Tasa de muerte celular (1/h)
        """
        self.mu_max = mu_max
        self.Ks = Ks
        self.Yxs = Yxs
        self.Yps = Yps
        self.kd = kd

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
