import os

import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception


SYSTEM_PROMPT = """\
You are a professional meal-planning nutritionist.

CRITICAL — Zero-waste policy: Every perishable ingredient purchased \
MUST be used across the week's meals. No food should go to waste.

Assume the user already has common pantry staples (oil, salt, pepper, \
basic spices, etc.). Exclude these from the grocery list and cost estimate.

Output format (use markdown):
1. **Daily Meal Plan** — For each day (Monday–Sunday), list Breakfast, \
Lunch, Dinner, and Snacks with estimated kcal per meal.
2. **Grocery List** — Grouped by category (produce, protein, dairy, etc.) \
with quantities.
3. **Itemized Cost Estimate** — Price per item and weekly total.
4. **Meal Prep Notes** — What to prepare ahead and when."""


def build_user_prompt(biometrics_summary, preferences):
    dietary = preferences.get("dietary_blob", "No specific restrictions.")
    locale = preferences.get("locale", "en-US")
    consistent_lunch = preferences.get("consistent_lunch", False)

    sections = [
        f"Calorie budget: {biometrics_summary}",
        f"Dietary restrictions / preferences: {dietary}",
        f"Use pricing and ingredients typical for locale: {locale}.",
    ]

    if consistent_lunch:
        sections.append(
            "Consistent lunch: Design ONE meal-prep lunch that is eaten Monday–Friday. "
            "It should reheat well and stay fresh for 5 days."
        )

    return "\n\n".join(sections)


def _is_transient(error):
    """Only retry genuinely transient errors, not billing/auth issues."""
    if isinstance(error, openai.RateLimitError):
        # insufficient_quota is a billing problem, not a transient rate limit
        return "insufficient_quota" not in str(error)
    return isinstance(error, (openai.APITimeoutError, openai.APIConnectionError))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=4, min=4, max=16),
    retry=retry_if_exception(_is_transient),
)
def generate_meal_plan(biometrics_summary, preferences):
    """Call OpenAI GPT-4o-mini and return the meal plan as markdown."""
    user_prompt = build_user_prompt(biometrics_summary, preferences)

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
