import pandas as pd
import requests

# Скачиваем данные об экзопланетах
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
df = pd.read_csv(url, low_memory=False)

print(f"Всего обнаружено экзопланет: {len(df)}")
print(f"Средний радиус: {df['pl_rade'].mean():.2f} радиусов Земли")
print(f"Средний орбитальный период: {df['pl_orbper'].mean():.2f} дней")