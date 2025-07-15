def call_ai(prompt):
    payload = {
        "model": "openhermes-2.5-mistral-7b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://127.0.0.1:1234/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_menu_data(meal_type, year, month, day, target_date, dining_hall):
    url = f"https://techdining.api.nutrislice.com/menu/api/weeks/school/{dining_hall}/menu-type/{meal_type}/{year}/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    menu_data = []
    for day_data in data.get('days', []):
        if day_data.get('date') == target_date:
            for item in day_data.get('menu_items', []):
                food = item.get('food')
                if food is None:
                    continue
                nutrition = food.get('rounded_nutrition_info', {})
                size = food.get('serving_size_info', {})
                if not food.get('name') or not nutrition.get('calories') or not nutrition.get('g_protein'):
                    continue
                menu_data.append({
                    'Item': food['name'],
                    'Calories': nutrition.get('calories'),
                    'Protein': nutrition.get('g_protein'),
                    'Fat (g)': nutrition.get('g_fat'),
                    'Carbs (g)': nutrition.get('g_carbs'),
                    'Serving Size': size.get('serving_size_amount'),
                    'Serving Unit': size.get('serving_size_unit')
                })
    return pd.DataFrame(menu_data)