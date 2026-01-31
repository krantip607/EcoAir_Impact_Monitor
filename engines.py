def calculate_bio_risk(pm25, age, activity_level):
    base_rate = 0.6 if activity_level == "Sedentary" else 1.5
    inhaled_dose = pm25 * base_rate
    equiv_cigs = round(pm25 / 22, 2)
    return round(inhaled_dose, 2), equiv_cigs

def calculate_environmental_decay(so2, humidity):
    if so2 > 20 and humidity > 80:
        return "CRITICAL", 3.0
    return "STABLE", 1.0

def calculate_fiscal_loss(city_pop, avg_wage, aqi):
    if aqi <= 100: return 0.0
    loss_coeff = ((aqi - 100) / 10) * 0.00001
    return round((city_pop * avg_wage) * loss_coeff, 2)