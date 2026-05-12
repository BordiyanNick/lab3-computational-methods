# Модель: Математичне моделювання біологічного росту бактерій (5 семестр)
# Автор: Бордіян Микола Павлович, група AI-231

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class BacteriaGrowthModel:
    def __init__(self):
        # Кінетичні параметри моделі 
        self.mu_max = 0.5  # Максимальна питома швидкість росту (год^-1)
        self.Ks = 0.01     # Константа напівнасичення (г/л)
        self.Y = 0.4       # Коефіцієнт виходу (ефективність використання субстрату)

    def model_system(self, y, t):
        """
        Система диференціальних рівнянь 
        N: чисельність бактерій
        S: концентрація субстрату
        """
        N, S = y
        
        # Рівняння Моно для швидкості росту 
        mu = self.mu_max * (S / (self.Ks + S))
        
        # dN/dt = mu * N 
        dNdt = mu * N
        
        # dS/dt = -(1/Y) * dN/dt 
        dSdt = -(1 / self.Y) * dNdt
        
        return [dNdt, dSdt]

    def run_simulation(self, N0, S0, t_max):
        """Запуск чисельного інтегрування"""
        t = np.linspace(0, t_max, 1000)
        y0 = [N0, S0]  # Початкові умови
        
        # Розв'язання системи ЗДР за допомогою odeint 
        solution = odeint(self.model_system, y0, t)
        return t, solution[:, 0], solution[:, 1]

    def plot_results(self, t, N, S):
        """Візуалізація N(t) та S(t)"""
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:green'
        ax1.set_xlabel('Час (год)')
        ax1.set_ylabel('Чисельність бактерій (N)', color=color)
        ax1.plot(t, N, color=color, linewidth=2, label='Бактерії (N)')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Концентрація субстрату (S)', color=color)
        ax2.plot(t, S, color=color, linestyle='--', linewidth=2, label='Субстрат (S)')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title('Моделювання біологічного росту бактерій у замкненому середовищі')
        fig.tight_layout()
        plt.grid(True, linestyle=':')
        
        plt.savefig("growth_model.png")
        print("Графік збережено у файл 'growth_model.png'")
        plt.show()

if __name__ == '__main__':
    model = BacteriaGrowthModel()
  
    t, N, S = model.run_simulation(N0=0.1, S0=1.0, t_max=24)

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import sys

class BacteriaGrowthModel:
    """
    Клас для моделювання динаміки росту популяції бактерій 
    з урахуванням обмеження субстрату за рівнянням Моно.
    """
    def __init__(self, mu_max=0.5, Ks=0.01, Y=0.4):
        # Параметри згідно з кейсом 
        self.mu_max = mu_max  # Максимальна швидкість росту (год^-1)
        self.Ks = Ks          # Константа напівнасичення (г/л)
        self.Y = Y            # Ефективність споживання (г бактерій / г субстрату)

    def _equations(self, variables, t):
        """Опис системи ЗДР"""
        N, S = variables
        
        # Запобігання від'ємним значенням концентрації
        if S < 0: S = 0
        
        # Рівняння Моно
        mu = self.mu_max * (S / (self.Ks + S))
        
        # Зміна чисельності бактерій та субстрату
        dNdt = mu * N
        dSdt = -(1 / self.Y) * dNdt
        
        return [dNdt, dSdt]

    def solve(self, N0, S0, t_max, steps=1000):
        """Чисельне розв'язання моделі [cite: 99]"""
        try:
            self.t = np.linspace(0, t_max, steps)
            y0 = [N0, S0]
            
            solution = odeint(self._equations, y0, self.t)
            
            self.N = solution[:, 0]
            self.S = solution[:, 1]
            return self.t, self.N, self.S
        except Exception as e:
            print(f"Помилка при обчисленні: {e}")
            sys.exit(1)

    def calculate_metrics(self):
        """Розрахунок додаткових характеристик моделі"""
        max_n = np.max(self.N)
        # Час подвоєння (на експоненціальній фазі)
        td = np.log(2) / self.mu_max
        
        # Пошук моменту, коли субстрат майже вичерпано (стаціонарна фаза)
        idx_stat = np.where(self.S < 0.01 * np.max(self.S))[0]
        t_stat = self.t[idx_stat[0]] if len(idx_stat) > 0 else None
        
        return max_n, td, t_stat

    def plot(self):
        """Розширена візуалізація результатів """
        max_n, td, t_stat = self.calculate_metrics()
        
        fig, ax1 = plt.subplots(figsize=(12, 7))

        # Налаштування осі для бактерій
        ax1.set_xlabel('Час (години)', fontsize=12)
        ax1.set_ylabel('Біомаса бактерій (N, г/л)', color='darkgreen', fontsize=12)
        line1, = ax1.plot(self.t, self.N, color='darkgreen', linewidth=3, label='Чисельність бактерій (N)')
        ax1.fill_between(self.t, self.N, color='green', alpha=0.1)
        ax1.tick_params(axis='y', labelcolor='darkgreen')

        # Налаштування осі для субстрату
        ax2 = ax1.twinx()
        ax2.set_ylabel('Концентрація субстрату (S, г/л)', color='darkred', fontsize=12)
        line2, = ax2.plot(self.t, self.S, color='darkred', linestyle='--', linewidth=2, label='Субстрат (S)')
        ax2.tick_params(axis='y', labelcolor='darkred')

        # Додавання індикатора стаціонарної фази
        if t_stat:
            ax1.axvline(x=t_stat, color='gray', linestyle=':', label='Початок стац. фази')

        # Оформлення
        plt.title('Моделювання росту бактерій (Модель Моно)\nДевіз: "Ріст через моделювання"', fontsize=14)
        ax1.grid(True, which='both', linestyle='--', alpha=0.5)
        
        # Об'єднана легенда
        lines = [line1, line2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='center right')

        # Текстова інформація на графіку
        info_text = f'Max N: {max_n:.2f} г/л\nЧас подвоєння: {td:.2f} год'
        plt.gcf().text(0.15, 0.8, info_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

        plt.tight_layout()
        plt.savefig("bacterial_growth_detailed.png", dpi=300)
        print(f"Аналіз завершено. Максимальна біомаса: {max_n:.2f}")
        plt.show()

if __name__ == '__main__':
    # Створення об'єкта моделі з параметрами з кейсу 
    growth_sim = BacteriaGrowthModel(mu_max=0.5, Ks=0.01, Y=0.4)
    
    # Початкові умови: N0=0.05, S0=2.0, моделювання на 30 годин
    growth_sim.solve(N0=0.05, S0=2.0, t_max=30)
    growth_sim.plot()
    print(f"Максимальна чисельність колонії: {max(N):.2f}") 
    model.plot_results(t, N, S)
