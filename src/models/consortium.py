class BioproductSimulator:
    def __init__(self, feedstock, consortium):
        """
        Simulador de composición final de bioproductos basado en el consorcio microbiano.
        
        feedstock: dict con la composición inicial en g/L (azúcares, celulosa, nitrógeno, minerales)
        consortium: lista de strings con los microorganismos inoculados
        """
        self.feedstock = feedstock.copy()
        self.consortium = consortium
        
    def run_fermentation(self, days=15):
        """
        Calcula la composición final estimada (g/L) asumiendo factores de conversión empíricos 
        para un tiempo de residencia determinado.
        """
        output = {
            'azucares_residuales': self.feedstock.get('azucares_simples', 0),
            'celulosa_residual': self.feedstock.get('celulosa', 0),
            'etanol': 0.0,
            'acido_lactico': 0.0,
            'aminoacidos_libres': 0.0,
            'esteres_aromaticos': 0.0,
            'biomasa_total': 0.1,  # Inóculo inicial
            'ph_estimado': 6.5
        }
        
        # 1. Acción de Bacillus (Hidrólisis de complejos)
        if 'Bacillus' in self.consortium:
            # Degrada celulosa a azúcares simples
            celulosa_degradada = output['celulosa_residual'] * 0.4  # 40% de eficiencia
            output['celulosa_residual'] -= celulosa_degradada
            output['azucares_residuales'] += celulosa_degradada
            
            # Degrada proteínas a aminoácidos libres
            output['aminoacidos_libres'] += self.feedstock.get('nitrogeno_organico', 0) * 0.6

        # 2. Acción de Levaduras (Saccharomyces)
        if 'Levadura' in self.consortium:
            azucares_consumidos = output['azucares_residuales'] * 0.7
            output['azucares_residuales'] -= azucares_consumidos
            
            # Rendimiento típico de Gay-Lussac ~0.51 g etanol / g glucosa
            output['etanol'] += azucares_consumidos * 0.45 
            output['esteres_aromaticos'] += azucares_consumidos * 0.02
            output['biomasa_total'] += azucares_consumidos * 0.05

        # 3. Acción de Bacterias Ácido Lácticas (Lactobacillus)
        if 'Lactobacillus' in self.consortium:
            # Compiten por azúcares
            azucares_consumidos_lab = output['azucares_residuales'] * 0.8
            output['azucares_residuales'] -= azucares_consumidos_lab
            
            # Rendimiento de ácido láctico
            output['acido_lactico'] += azucares_consumidos_lab * 0.85
            output['biomasa_total'] += azucares_consumidos_lab * 0.05
            
            # Caída de pH empírica en base al ácido láctico (aprox)
            if output['acido_lactico'] > 10:
                output['ph_estimado'] = 3.8
            elif output['acido_lactico'] > 0:
                output['ph_estimado'] = 4.5

        return output

    def generate_report(self):
        final_comp = self.run_fermentation()
        
        report = "=== REPORTE DE COMPOSICIÓN DE BIOPRODUCTO ===\n"
        report += f"Materia Prima Inicial: {self.feedstock}\n"
        report += f"Consorcio Inoculado: {', '.join(self.consortium)}\n"
        report += "-"*45 + "\n"
        report += "[Composición Final Estimada]\n"
        for key, value in final_comp.items():
            unidad = "pH" if key == "ph_estimado" else "g/L"
            report += f"{key.replace('_', ' ').title():<25}: {value:.2f} {unidad}\n"
            
        return report
