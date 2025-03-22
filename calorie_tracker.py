import requests
import json


# ANSI escape sequences for colors
BLUE = "\033[34m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"


app_id = "c96a3aca"
app_key = "73ff72f872f07804b3072e110788980a"


weekly_log = {
   "Monday": {"entries": [], "tdee": 0},
   "Tuesday": {"entries": [], "tdee": 0},
   "Wednesday": {"entries": [], "tdee": 0},
   "Thursday": {"entries": [], "tdee": 0},
   "Friday": {"entries": [], "tdee": 0},
   "Saturday": {"entries": [], "tdee": 0},
   "Sunday": {"entries": [], "tdee": 0}
}


def get_calories_from_api(product, amount_grams):
   url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
  
   headers = {
       "Content-Type": "application/json",
       "x-app-id": app_id,
       "x-app-key": app_key,
   }
  
   body = json.dumps({
       "query": product
   })
  
   try:
       response = requests.post(url, headers=headers, data=body)
       response.raise_for_status()
      
       data = response.json()
       calories_per_serving = data['foods'][0]['nf_calories']
       serving_size_g = data['foods'][0]['serving_weight_grams']
       calories_consumed = (calories_per_serving / serving_size_g) * amount_grams
      
       return calories_consumed
   except requests.RequestException as e:
       print(f"Error making request to Nutritionix API: {e}")
       return 0


def log_day_data(day, product, amount, calories, tdee):
   if day in weekly_log:
       weekly_log[day]["entries"].append({"product": product, "amount": amount, "calories": calories})
       if weekly_log[day]["tdee"] == 0:





           weekly_log[day]["tdee"] = tdee
   else:
       print("Invalid day of the week.")


def calculate_daily_totals():
   weekly_totals = {"tdee": 0, "calories_consumed": 0, "calorie_deficit": 0, "weight_loss": 0}
   for day, data in weekly_log.items():
       total_calories = sum(entry["calories"] for entry in data["entries"])
       tdee = data["tdee"]
       calorie_deficit = tdee - total_calories if tdee else 0
       weight_loss = calorie_deficit / 3500
      
       # Add to weekly totals
       weekly_totals["tdee"] += tdee
       weekly_totals["calories_consumed"] += total_calories
       weekly_totals["calorie_deficit"] += calorie_deficit
       weekly_totals["weight_loss"] += weight_loss
      
       print(f"\n{YELLOW}{day}:{RESET}")
       print(f"{YELLOW}Total calories consumed:{RESET} {GREEN}{total_calories}{RESET}")
       if tdee:
           print(f"{YELLOW}TDEE:{RESET} {GREEN}{tdee}{RESET}")
           print(f"{YELLOW}Calorie deficit:{RESET} {GREEN}{calorie_deficit}{RESET}")
           print(f"{YELLOW}Estimated weight loss:{RESET} {GREEN}{weight_loss:.2f} pounds{RESET}")
  
   # Print weekly totals
   print(f"\n{MAGENTA}Weekly Totals:{RESET}")
   print(f"{YELLOW}Total TDEE:{RESET} {GREEN}{weekly_totals['tdee']}{RESET}")
   print(f"{YELLOW}Total calories consumed:{RESET} {GREEN}{weekly_totals['calories_consumed']}{RESET}")
   print(f"{YELLOW}Total calorie deficit:{RESET} {GREEN}{weekly_totals['calorie_deficit']}{RESET}")
   print(f"{YELLOW}Total estimated weight loss:{RESET} {GREEN}{weekly_totals['weight_loss']:.2f} pounds{RESET}")


def colored_input(prompt, color):
   print(color + prompt + RESET, end='')
   return input()


def main():
   while True:
       day_of_week = colored_input("Enter the day of the week (or 'done' to finish): ", MAGENTA).capitalize()
       if day_of_week.lower() == 'done':
           break
      
       if day_of_week in weekly_log:
           tdee = float(colored_input("Enter your TDEE (Total Daily Energy Expenditure) in calories for this day: ", MAGENTA))
          
           while True:
               product = colored_input("Enter food product (or 'done' to finish entries for this day): ", MAGENTA)
               if product.lower() == 'done':
                   break
               amount = float(colored_input("Enter amount of the product in grams: ", MAGENTA))
              
               calories = get_calories_from_api(product, amount)
               print(f"{BLUE}Calories for {amount}g of {product}: {calories}{RESET}")
              
               log_day_data(day_of_week, product, amount, calories, tdee)
       else:
           print(f"{RED}Please enter a valid day of the week.{RESET}")


   # Calculate and print daily totals, deficits, and estimated weight loss
   calculate_daily_totals()


if __name__ == "__main__":
   main()




