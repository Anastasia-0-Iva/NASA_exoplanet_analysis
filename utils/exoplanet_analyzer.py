import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Optional
import requests
#import utils.api

print("Начинаем загрузку данных...")
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
df = pd.read_csv(url, low_memory=False)
print(f"Данные загружены! {len(df)} планет")

class PlanetExplorer:
    def __init__(self):
        self.name = None
        self.planet_row = None

    #Общие данные о планете
    def data_planet(self, planet_name):
        self.name = planet_name
        self.planet_row = df[df['pl_name'] == planet_name]
        if self.planet_row.empty:
            return 'Планета не найдена.'
        else:
            radius = self.planet_row['pl_rade'].values[0] #Радиус в Землях
            distance = self.planet_row['sy_dist'].values[0] #Дистанция в световых годах
            temperature = self.planet_row['pl_eqt'].values[0] #Температура в кельвинах
            bmasse = self.planet_row['pl_bmasse'].values[0] #Масса в массах Земли
            density = self.planet_row['pl_dens'].values[0] #Плотность в (г/см³)
            insolation = self.planet_row['pl_insol'].values[0] #Количество получаемой энергии от звезды (относительно Земли)

            radius_info = "неизвестно" if pd.isna(radius) else f"{radius:.2f}"
            distance_info = "неизвестно" if pd.isna(distance) else f"{distance:.2f}"
            temperature_info = "неизвестна" if pd.isna(temperature) else f"{temperature:.2f}"
            bmasse_info = "неизвестна" if pd.isna(bmasse) else f"{bmasse:.2f}"
            density_info = "неизвестна" if pd.isna(density) else f"{density:.2f}"
            insolation_info = "неизвестна" if pd.isna(insolation) else f"{insolation:.2f}"
            return (
                f'Название планеты: {self.name}; Температура в кельвинах: {temperature_info}; Масса планеты в массах Земли: {bmasse_info};\n'
                f'Плотность: {density_info}(г/см³); Радиусов Земли: {radius_info}; Расстояние в световых годах: {distance_info};\n'
                f'Инсоляция относительно Земли: {insolation_info}'
            )

    #Данные о звёздах
    def data_star(self):
        if self.planet_row is None or self.planet_row.empty:
            return 'Информация отсутствует.'
        else:
            number_star = self.planet_row['sy_snum'].values[0] #Кол-во звёзд в системе
            nearest_star = self.planet_row['hostname'].values[0] #Звезда-хозяин
            age_star = self.planet_row['st_age'].values[0]  # Возраст звезды в миллиардах лет
            k_star = self.planet_row['st_teff'].values[0] #Температура звезды в кельвинах
            star_radius =  self.planet_row['st_rad'].values[0] #Радиус в радиусах Солнца
            star_mass = self.planet_row['st_mass'].values[0] #Масса в солнечных массах

            number_info = "неизвестно" if pd.isna(number_star) else f"{number_star}"
            nearest_info = "неизвестна" if pd.isna(nearest_star) else f"{nearest_star}"
            kelvin_info = "неизвестна" if pd.isna(k_star) else f"{k_star:.2f}"
            age_star_info = "неизвестен" if pd.isna(age_star) else f"{age_star:.1f}"
            radius_info = "неизвестен" if pd.isna(star_radius) else f"{star_radius:.2f}"
            mass_info = "неизвестна" if pd.isna(star_mass) else f"{star_mass:.2f}"
            return (
                f'Звёзд в системе: {number_info}; Звезда-хозяин: {nearest_info}; Возраст в Ga: {age_star_info};\n'
                f'Температура звезды в кельвинах: {kelvin_info}; Радиус звезды в радиусах Солнца: {radius_info};\n'
                f'Масса звезды в солнечных массах: {mass_info}'
            )

    #Данные об орбите
    def data_orbit(self):
        if self.planet_row is None or self.planet_row.empty:
            return 'Информация отсутствует.'
        else:
            semi_axis = self.planet_row['pl_orbsmax'].values[0] #Большая полуось в астрономических единицах
            orbital_period = self.planet_row['pl_orbper'].values[0] #Период обращения в Земных днях
            eccentricity = self.planet_row['pl_orbeccen'].values[0]  #Насколько орбита вытянута

            if pd.isna(eccentricity):
                eccentricity_info_dop = "неизвестен"
            elif eccentricity < 0.01:
                eccentricity_info_dop = "почти идеальный круг"
            elif eccentricity < 0.1:
                eccentricity_info_dop = "слегка вытянутая"
            elif eccentricity < 0.3:
                eccentricity_info_dop = "вытянутая"
            elif eccentricity < 0.6:
                eccentricity_info_dop = "сильно вытянутая"
            elif eccentricity < 0.9:
                eccentricity_info_dop = "очень сильно вытянутая"
            else:
                eccentricity_info_dop = "гиперболическая (почти парабола)"


            semi_axis_info = "неизвестна" if pd.isna(semi_axis) else f"{semi_axis:.2f}"
            orbital_period_info = "неизвестен" if pd.isna(orbital_period) else f"{int(round(orbital_period))}"

            if pd.isna(eccentricity):
                eccentricity_info = "неизвестен"
            else:
                eccentricity_info = f"{eccentricity:.4f} | {eccentricity_info_dop}"

            return f'Эксцентриситет: {eccentricity_info}; Большая полуось в а.е.: {semi_axis_info}; Орбитальный период в Земных днях: {orbital_period_info}'

    #Данные Земли
    def get_earth_data(self):
        earth_data = {
            'name': 'Земля',
            'radius': 1.0,  #Радиусов Земли
            'mass': 1.0,  #Масс Земли
            'density': 5.51,  #Плотность в (г/см³)
            'temperature': 255,  #Температура в кельвинах
            'insolation': 1.0,  #Количество получаемой энергии от звезды относительно Земли
            'semi_major_axis': 1.0,  #Большая полуось
            'orbital_period': 365.25,  #Период обращения
            'eccentricity': 0.0167,  #Насколько орбита вытянута (почти круг)
            'distance': 0.0,  #Дистанция в световых годах (мы на ней)
        }
        return earth_data

    #Сравнение экзопланеты с Землёй
    def compare_with_earth(self):
        if self.planet_row is None or self.planet_row.empty:
            return 'Планета не найдена.'
        earth = self.get_earth_data()

        # Данные планеты
        radius = self.planet_row['pl_rade'].values[0] #Радиус
        mass = self.planet_row['pl_bmasse'].values[0]  #Масса
        density = self.planet_row['pl_dens'].values[0] #Плотность в (г/см³)
        temperature = self.planet_row['pl_eqt'].values[0] #Температура
        insolation = self.planet_row['pl_insol'].values[0] #Инсоляция
        semi_axis = self.planet_row['pl_orbsmax'].values[0] #Большая полуось
        orbital_period = self.planet_row['pl_orbper'].values[0] #Период обращения
        eccentricity = self.planet_row['pl_orbeccen'].values[0] #Насколько орбита вытянута
        star_temp = self.planet_row['st_teff'].values[0] #Температура звезды в кельвинах

        result = f"СРАВНЕНИЕ: {self.name} vs Земля\n"
        percentages = []

        # РАДИУС
        if not pd.isna(radius):
            diff = abs(radius - earth['radius']) / earth['radius']
            percent = max(0, 100 - diff * 100)
            result += f"Радиус: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # МАССА
        if not pd.isna(mass):
            diff = abs(mass - earth['mass']) / earth['mass']
            percent = max(0, 100 - diff * 100)
            result += f"Масса: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ПЛОТНОСТЬ
        if not pd.isna(density):
            diff = abs(density - earth['density']) / earth['density']
            percent = max(0, 100 - diff * 100)
            result += f"Плотность: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ТЕМПЕРАТУРА
        if not pd.isna(temperature):
            diff = abs(temperature - earth['temperature']) / earth['temperature']
            percent = max(0, 100 - diff * 100)
            result += f"процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ИНСОЛЯЦИЯ
        if not pd.isna(insolation):
            diff = abs(insolation - earth['insolation']) / earth['insolation']
            percent = max(0, 100 - diff * 100)
            result += f"Инсоляция: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # БОЛЬШАЯ ПОЛУОСЬ
        if not pd.isna(semi_axis):
            diff = abs(semi_axis - earth['semi_major_axis']) / earth['semi_major_axis']
            percent = max(0, 100 - diff * 100)
            result += f"Большая полуось: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ПЕРИОД ОБРАЩЕНИЯ
        if not pd.isna(orbital_period):
            diff = abs(orbital_period - earth['orbital_period']) / earth['orbital_period']
            percent = max(0, 100 - diff * 100)
            result += f"Период обращения: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ЭКСЦЕНТРИСИТЕТ
        if not pd.isna(eccentricity):
            diff = abs(eccentricity - earth['eccentricity']) / earth['eccentricity']
            percent = max(0, 100 - diff * 100)
            result += f"Эксцентриситет: процент схожести ~{percent:.1f}%\n"
            percentages.append(percent)

        # ДАННЫЕ О ЗВЕЗДЕ
        if not pd.isna(star_temp):
            sun_temp = 5778
            star_ratio = star_temp / sun_temp
            result += f"Звезда: {star_temp:.0f}K ({star_ratio:.1f}x Солнца)"


        # Считаем средний процент
        if percentages:
            avg_percent = sum(percentages) / len(percentages)
            result += f"\nОБЩАЯ СХОЖЕСТЬ С ЗЕМЛЁЙ: ~{avg_percent:.1f}%\n"

            # Оценка обитаемости
            if avg_percent > 70:
                result += "ВЫСОКИЙ ПОТЕНЦИАЛ ОБИТАЕМОСТИ"
            elif avg_percent > 40:
                result += "УМЕРЕННЫЙ ПОТЕНЦИАЛ ОБИТАЕМОСТИ"
            else:
                result += "НИЗКИЙ ПОТЕНЦИАЛ ОБИТАЕМОСТИ"

        return result

    # Визуализация сравнения с Землёй
    def visualize_comparison(self):
        if self.planet_row is None or self.planet_row.empty:
            return "Планета не найдена."

        # Получаем данные планеты
        planet_data = self._get_planet_data_dict()
        earth_data = self.get_earth_data()

        # ASCII-визуализация
        ascii_result = self._create_ascii_chart(planet_data, earth_data)

        # График
        chart_result = self._create_comparison_chart(planet_data, earth_data)

        return ascii_result + "\n" + (chart_result if chart_result else "")

    # Вспомогательные методы
    def _get_planet_data_dict(self):
        return {
            'radius': self.planet_row['pl_rade'].values[0],
            'mass': self.planet_row['pl_bmasse'].values[0],
            'density': self.planet_row['pl_dens'].values[0],
            'temperature': self.planet_row['pl_eqt'].values[0],
            'insolation': self.planet_row['pl_insol'].values[0],
            'semi_axis': self.planet_row['pl_orbsmax'].values[0],
            'orbital_period': self.planet_row['pl_orbper'].values[0],
            'eccentricity': self.planet_row['pl_orbeccen'].values[0]
        }

    def _create_ascii_chart(self, planet_data, earth_data):
        result = "\n" + "═" * 50
        result += f"\n ВИЗУАЛИЗАЦИЯ: {self.name} vs Земля\n"
        result += "═" * 50 + "\n"

        param_mapping = [
            ('Радиус', 'radius', 'radius'),
            ('Масса', 'mass', 'mass'),
            ('Плотность', 'density', 'density'),
            ('Температура', 'temperature', 'temperature'),
            ('Инсоляция', 'insolation', 'insolation'),
            ('Орбита', 'semi_axis', 'semi_major_axis'),
            ('Период', 'orbital_period', 'orbital_period')
        ]

        for display_name, planet_key, earth_key in param_mapping:
            p_val = planet_data.get(planet_key)
            e_val = earth_data.get(earth_key)

            if pd.isna(p_val) or not e_val or e_val == 0:
                continue

            similarity = max(0, 100 - abs(p_val / e_val - 1) * 100)
            bars = "█" * int(similarity / 3.33)  # 30 символов = 100%
            spaces = " " * (30 - len(bars))
            result += f"{display_name:<10} {similarity:>5.1f}% [{bars}{spaces}]\n"

        return result

    def _create_comparison_chart(self, planet_data, earth_data):
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import os

            # Создаём папку для результатов
            os.makedirs('results', exist_ok=True)

            # Параметры для сравнения
            parameters = ['Радиус', 'Масса', 'Плотность', 'Температура',
                          'Инсоляция', 'Большая полуось', 'Период обращения']

            # Подготавливаем данные
            earth_vals = []
            planet_vals = []
            valid_params = []

            param_mapping = {
                'Радиус': ('radius', 'radius'),
                'Масса': ('mass', 'mass'),
                'Плотность': ('density', 'density'),
                'Температура': ('temperature', 'temperature'),
                'Инсоляция': ('insolation', 'insolation'),
                'Большая полуось': ('semi_axis', 'semi_major_axis'),
                'Период обращения': ('orbital_period', 'orbital_period')
            }

            for param_display, (planet_key, earth_key) in param_mapping.items():
                p_val = planet_data.get(planet_key)
                e_val = earth_data.get(earth_key)

                if not pd.isna(p_val) and e_val and e_val != 0:
                    earth_vals.append(1.0)
                    planet_vals.append(p_val / e_val)
                    valid_params.append(param_display)

            if not valid_params:
                return "Недостаточно данных для построения графика"

            # Создаём график
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.arange(len(valid_params))

            colors = plt.cm.Set2(np.linspace(0, 1, 2))
            ax.bar(x - 0.2, earth_vals, 0.4, label='Земля', color=colors[0])
            ax.bar(x + 0.2, planet_vals, 0.4, label=self.name, color=colors[1])

            ax.set_xlabel('Параметры')
            ax.set_ylabel('Относительное значение (Земля = 1.0)')
            ax.set_title(f'Сравнение: {self.name} vs Земля', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(valid_params, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3, linestyle='--')

            # Добавляем проценты схожести
            for i, (e, p) in enumerate(zip(earth_vals, planet_vals)):
                similarity = max(0, 100 - abs(p - 1) * 100)
                ax.text(i, max(e, p) + 0.1, f'{similarity:.0f}%',
                        ha='center', fontweight='bold', fontsize=9)

            plt.tight_layout()

            # Сохраняем
            filename = f'results/{self.name.replace(" ", "_")}_comparison.png'
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            return f"График сохранён: {filename}"

        except ImportError:
            return "Установите matplotlib для графиков: pip install matplotlib"
        except Exception as e:
            return f"Ошибка при создании графика: {e}"



explorer = PlanetExplorer()
planet_name = input("Введите название планеты: ")
print("ОБЩИЕ ДАННЫЕ ОБ ЭКЗОПЛАНЕТЕ:")
print(explorer.data_planet(planet_name))
print("ДАННЫЕ О ЗВЁЗДАХ:")
print(explorer.data_star())
print("ДАННЫЕ ОБ ОРБИТЕ:")
print(explorer.data_orbit())
print("СРАВНЕНИЕ С ЗЕМЛЁЙ:")
print(explorer.compare_with_earth())
print("ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ:")
print(explorer.visualize_comparison())