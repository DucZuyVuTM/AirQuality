import json

# Чтение JSON-файла
try:
    with open("air_quality_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Вывод данных в консоль
    print("Данные качества воздуха:")
    print(f"ID устройства: {data['device_id']}")
    print(f"Временная метка: {data['timestamp']}")
    print(f"PM2.5: {data['pm25']} мкг/м³")
    print(f"PM10: {data['pm10']} мкг/м³")
    print(f"CO2: {data['co2']} ppm")
    print(f"Температура: {data['temperature']} °C")
    print(f"Влажность: {data['humidity']} %")
    print(f"Состояние реле: {'Включено' if data['relay_state'] else 'Выключено'}")

except FileNotFoundError:
    print("Ошибка: Файл air_quality_data.json не найден")
except json.JSONDecodeError:
    print("Ошибка: Неверный формат JSON")
