import requests
import pandas as pd
import numpy as np
from scipy.optimize import linprog

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "openhermes-2.5-mistral-7b"

def call_ai(prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)
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

def ask_ai_to_pick_items(meal_name, item_list, dietary_restrictions=None):
    restriction_text = (
        f" The user has these dietary restrictions: {dietary_restrictions}."
        if dietary_restrictions else ""
    )
    prompt = (
        f"From the following list of {meal_name} items:\n\n"
        + "\n".join(item_list)
        + f"\n\nPick 3–5 items that sound like a tasty high protein meal for a bodybuilder. Make sure there is one meat/protein per meal. Make the portions of each item reasonable and enjoyable to eat so not pounds of the same thing. {restriction_text} "
          "Just return the item names separated by commas. No commentary."
    )
    response = call_ai(prompt)
    selected_items = [item.strip() for item in response.split(',') if item.strip()]
    return selected_items

def optimize_servings(df, calorie_target, max_servings=10, protein_cap=None):
    if df.empty:
        return ["No items available."]
    
    df = df.head(10)
    calories = df['Calories'].values
    protein = df['Protein'].values
    items = df['Item'].values
    sizes = df['Serving Size'].values
    units = df['Serving Unit'].values

    n = len(df)
    c = -1 * protein  # Maximize protein

    A = [calories, [1]*n]
    b = [calorie_target, max_servings]

    if protein_cap:
        A.append(protein)
        b.append(protein_cap)

    bounds = [(0, 3) for _ in range(n)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        servings = res.x
        results = []
        for i in np.argsort(-servings):
            count = int(round(servings[i]))
            if count > 0:
                size_str = f"{sizes[i]} {units[i]}" if pd.notnull(sizes[i]) and pd.notnull(units[i]) else "unknown size"
                results.append(
                    f"{items[i]} x{count} (Serving: {size_str}) → {int(calories[i]*count)} cal, {int(protein[i]*count)}g)"
                )
        return results
    else:
        return ["Optimization failed."]

def process_meal(meal_type, meal_name, year, month, day, target_date, cal_target, protein_goal, dining_hall, dietary_restrictions=None):
    df = get_menu_data(meal_type, year, month, day, target_date, dining_hall)
    if df.empty or 'Item' not in df.columns:
        return [f"No {meal_name} items available."]
    item_names = df['Item'].tolist()
    selected_names = ask_ai_to_pick_items(meal_name, item_names, dietary_restrictions)
    selected_df = df[df['Item'].isin(selected_names)].reset_index(drop=True)
    protein_cap = protein_goal / 3
    return optimize_servings(selected_df, cal_target, protein_cap=protein_cap)

def format_meal(name, items):
    return f"({name}) " + " + ".join(items)