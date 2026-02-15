# AI Meal Planner

A Raspberry Pi automation script that generates a personalized, zero-waste weekly meal plan using OpenAI GPT-4o and emails it to you every Saturday night.

## Features

- Calculates your daily calorie target using the Mifflin-St Jeor equation
- Generates a full weekly meal plan with grocery list and cost estimate
- Zero-waste policy — all perishable ingredients are used across the week
- Optional consistent meal-prep lunch for workdays
- Sends a styled HTML email via SMTP

## Quick Setup

Run the interactive setup script — it creates the virtual environment, installs dependencies, and walks you through all the configuration:

```bash
./setup.sh
```

You'll need your OpenAI API key and a Gmail app password ready.

### Getting a Gmail App Password

1. Enable 2-Step Verification on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** and your device, then click **Generate**
4. Use the 16-character password when the setup script asks for it

### Manual Setup

If you prefer to configure things manually:

1. `python3 -m venv meals && meals/bin/pip install -r requirements.txt`
2. Edit `config.json` with your biometrics, preferences, and email
3. `cp .env.example .env` and fill in your API key and SMTP credentials

## Usage

```bash
source meals/bin/activate
python main.py
```

## Cron Job (Weekly on Saturday at 11:59 PM)

```bash
crontab -e
```

Add this line (adjust paths to your setup):

```
59 23 * * 6 cd /home/pi/ai-meal-planner && /home/pi/ai-meal-planner/meals/bin/python main.py >> cron.log 2>&1
```

Note: `* * * 6` = Saturday in cron (0=Sunday, 6=Saturday). If you want Sunday night, use `59 23 * * 0`.

# Example Email Output

# Daily Meal Plan

## Monday
- **Breakfast:** Overnight oats with Greek yogurt, berries, and honey (550 kcal)  
- **Lunch:** Chicken and quinoa salad with mixed vegetables (450 kcal)  
- **Dinner:** Baked salmon with roasted sweet potatoes and broccoli (700 kcal)  
- **Snacks:** Hummus with carrot sticks (200 kcal), Protein shake (300 kcal)  

## Tuesday
- **Breakfast:** Scrambled eggs with spinach and whole-grain toast (450 kcal)  
- **Lunch:** Chicken and quinoa salad with mixed vegetables (450 kcal)  
- **Dinner:** Stir-fried beef with bell peppers and rice (700 kcal)  
- **Snacks:** Greek yogurt with granola (300 kcal), Apple (100 kcal)  

## Wednesday
- **Breakfast:** Overnight oats with Greek yogurt, berries, and honey (550 kcal)  
- **Lunch:** Chicken and quinoa salad with mixed vegetables (450 kcal)  
- **Dinner:** Grilled shrimp tacos with cabbage slaw (700 kcal)  
- **Snacks:** Mixed nuts (200 kcal), Protein bar (300 kcal)  

## Thursday
- **Breakfast:** Scrambled eggs with spinach and whole-grain toast (450 kcal)  
- **Lunch:** Chicken and quinoa salad with mixed vegetables (450 kcal)  
- **Dinner:** Baked chicken thighs with roasted Brussels sprouts and brown rice (700 kcal)  
- **Snacks:** Hummus with cucumber slices (200 kcal), Banana (100 kcal)  

## Friday
- **Breakfast:** Overnight oats with Greek yogurt, berries, and honey (550 kcal)  
- **Lunch:** Chicken and quinoa salad with mixed vegetables (450 kcal)  
- **Dinner:** Turkey meatballs with marinara sauce and zucchini noodles (700 kcal)  
- **Snacks:** Greek yogurt with honey (300 kcal), Dark chocolate square (100 kcal)  

## Saturday
- **Breakfast:** Scrambled eggs with tomatoes and avocado (450 kcal)  
- **Lunch:** Leftover turkey meatballs with marinara sauce and zucchini noodles (600 kcal)  
- **Dinner:** Grilled steak with asparagus and mashed potatoes (700 kcal)  
- **Snacks:** Cottage cheese with pineapple (200 kcal), Protein shake (300 kcal)  

## Sunday
- **Breakfast:** Overnight oats with Greek yogurt, berries, and honey (550 kcal)  
- **Lunch:** Leftover chicken salad with mixed vegetables (450 kcal)  
- **Dinner:** Vegetable stir-fry with tofu and rice (600 kcal)  
- **Snacks:** Hummus with bell pepper strips (200 kcal), Apple (100 kcal)  

**Weekly Total:** 17,500 kcal (2,500 kcal/day)

---

# Grocery List

## Produce
- Spinach - 1 bag (200g)  
- Mixed salad greens - 1 bag (200g)  
- Sweet potatoes - 4 medium (800g)  
- Broccoli - 1 head (500g)  
- Bell peppers - 3 (450g)  
- Zucchini - 2 (400g)  
- Brussels sprouts - 500g  
- Carrots - 500g  
- Tomatoes - 4 medium (600g)  
- Avocado - 2 (400g)  
- Berries (frozen or fresh) - 600g  
- Apples - 3 (450g)  
- Bananas - 3 (450g)  
- Cabbage - 1 small head (300g)  
- Fresh herbs (optional, e.g., cilantro, parsley)  

## Protein
- Chicken breast - 1.5 kg  
- Ground turkey - 500g  
- Salmon fillets - 500g  
- Shrimp - 500g  
- Eggs - 1 dozen (12)  
- Greek yogurt - 1 kg  
- Cottage cheese - 500g  
- Tofu - 400g  

## Grains
- Quinoa - 500g  
- Whole grain bread - 1 loaf  
- Brown rice - 500g  
- Granola - 250g  
- Oats - 500g  

## Dairy
- Milk (or a non-dairy alternative) - 1L  

## Snacks
- Mixed nuts - 250g  
- Dark chocolate - 100g  
- Hummus - 250g  
- Protein powder - 500g (if not already on hand)  

---

# Itemized Cost Estimate (Approximate)

| Item | Quantity | Price (CAD) | Total (CAD) |
|------|----------|-------------|-------------|
| Spinach | 200g | 2.50 | 2.50 |
| Mixed salad greens | 200g | 3.00 | 3.00 |
| Sweet potatoes | 4 | 0.80 | 3.20 |
| Broccoli | 1 head | 1.50 | 1.50 |
| Bell peppers | 3 | 1.00 | 3.00 |
| Zucchini | 2 | 1.50 | 3.00 |
| Brussels sprouts | 500g | 3.00 | 3.00 |
| Carrots | 500g | 1.50 | 1.50 |
| Tomatoes | 4 | 0.75 | 3.00 |
| Avocado | 2 | 1.50 | 3.00 |
| Berries | 600g | 5.00 | 5.00 |
| Apples | 3 | 0.80 | 2.40 |
| Bananas | 3 | 0.60 | 1.80 |
| Cabbage | 1 small | 1.00 | 1.00 |
| Chicken breast | 1.5 kg | 10.00 | 15.00 |
| Ground turkey | 500g | 5.00 | 5.00 |
| Salmon fillets | 500g | 15.00 | 15.00 |
| Shrimp | 500g | 10.00 | 10.00 |
| Eggs | 12 | 3.00 | 3.00 |
| Greek yogurt | 1 kg | 5.00 | 5.00 |
| Cottage cheese | 500g | 3.00 | 3.00 |
| Tofu | 400g | 2.00 | 2.00 |
| Quinoa | 500g | 5.00 | 5.00 |
| Whole grain bread | 1 loaf | 3.00 | 3.00 |
| Brown rice | 500g | 2.00 | 2.00 |
| Granola | 250g | 4.00 | 4.00 |
| Oats | 500g | 2.00 | 2.00 |
| Milk | 1L | 2.00 | 2.00 |
| Mixed nuts | 250g | 6.00 | 6.00 |
| Dark chocolate | 100g | 2.00 | 2.00 |
| Hummus | 250g | 3.00 | 3.00 |
| Protein powder | 500g | 20.00 | 20.00 |

**Weekly Total:** CAD 100.90

---

# Meal Prep Notes

## Sunday Evening
- Prepare overnight oats for Monday, Wednesday, and Friday breakfasts (3 servings).  
- Cook a large batch of quinoa (3 cups cooked) for the week.  
- Grill/bake chicken breast for the week (1.5 kg), season and store for lunch.  
- Chop vegetables for the chicken and quinoa salad and store in airtight containers.  
- Make the stir-fried beef, bake salmon, and prepare all sauces and marinades for easy access.  
- Prepare and portion snacks (hummus, carrot sticks, mixed nuts).  

## Wednesday Evening
- Prepare overnight oats for Thursday and Sunday breakfasts (2 servings).  
- Cook turkey meatballs and portion for Friday dinner and Saturday lunch.  
- Portion out remaining salads and vegetables as needed.  

## Daily
- Scramble eggs in the morning for Tuesday and Thursday breakfasts.  
- Ensure leftovers from dinners are saved for lunch the next day where applicable.  

---

This plan ensures you stay within your calorie budget and utilizes all purchased ingredients efficiently throughout the week, adhering to the zero-waste policy. Enjoy your meals!
