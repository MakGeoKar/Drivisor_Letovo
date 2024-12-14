def calculate_driver_fatigue(co2, temperature, monotony, speed, fatigue_level, time_of_day, season, trip_length):
    # Функция для расчёта коэффициента времени
    def calculate_time_factor(hour, season):
        if season.lower() == 'зима':
            if 8 <= hour < 16:  # День
                return 0.5
            elif 16 <= hour < 22:  # Вечер
                return 0.7
            else:  # Ночь
                return 1.0
        elif season.lower() in ['весна', 'осень']:
            if 7 <= hour < 18:  # День
                return 0.5
            elif 18 <= hour < 22:  # Вечер
                return 0.7
            else:  # Ночь
                return 1.0
        elif season.lower() == 'лето':
            if 6 <= hour < 20:  # День
                return 0.5
            elif 20 <= hour < 23:  # Вечер
                return 0.7
            else:  # Ночь
                return 1.0
        else:
            raise ValueError("Неверный сезон. Укажите: 'зима', 'весна', 'лето', 'осень'.")

    
    time_factor = calculate_time_factor(time_of_day, season)

    # Весовые коэффициенты
    weights = {
        "w1": 0.15,  # CO2
        "w2": 0.12,  # Температура
        "w3": 0.08,  # Монотонность
        "w4": 0.10,  # Скорость
        "w5": 0.12,  # Усталость
        "w6": 0.15,  # Время
        "w7": 0.10,  # Длина поездки
        "w8": 0.05,  # Температура × Время
        "w9": 0.08,  # Скорость × Длина поездки
        "w10": 0.05,  # Температура² × CO₂²
    }

    f_co2 = (co2 - 600) / 600
    f_temperature = abs(temperature - 23) / 23
    f_monotony = monotony
    f_speed = abs(speed - 75) / 75
    f_fatigue = (fatigue_level - 1) / 4
    f_trip_length = trip_length / 240

    fatigue_index = (
        weights["w1"] * f_co2**3 +
        weights["w2"] * f_temperature**3 +
        weights["w3"] * f_monotony +
        weights["w4"] * f_speed**3 +
        weights["w5"] * f_fatigue**2 +
        weights["w6"] * time_factor**4 +
        weights["w7"] * f_trip_length +
        weights["w8"] * f_temperature * time_factor**2 +
        weights["w9"] * f_speed * f_trip_length +
        weights["w10"] * f_temperature**2 * f_co2**2
    )

    threshold = 1.3

    if fatigue_index > threshold:
        return f"Индекс усталости: {fatigue_index:.2f}. Рекомендуется остановиться и отдохнуть."
    else:
        return f"Индекс усталости: {fatigue_index:.2f}. Можно продолжить движение."


result = calculate_driver_fatigue(
    co2=1200,              # Текущий уровень CO2
    temperature=28,        # Температура в салоне
    monotony= 1,           # Монотонность
    speed=65,              # Скорость
    fatigue_level=4,       # Усталость (1-5)
    time_of_day=21,        # Время суток (час)
    season='зима',         # Сезон
    trip_length=200        # Длина поездки (минуты)
)
print(result)
