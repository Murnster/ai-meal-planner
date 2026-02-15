from datetime import date, datetime


ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
    "extra_active": 1.9,
}

LBS_PER_KG = 2.20462
KCAL_PER_LB = 3500


class BiometricCalculator:
    def __init__(self, age, gender, height_cm, current_weight_lbs,
                 activity_level, goal_weight_lbs, target_date):
        self.age = age
        self.gender = gender
        self.height_cm = height_cm
        self.current_weight_lbs = current_weight_lbs
        self.activity_level = activity_level
        self.goal_weight_lbs = goal_weight_lbs

        if isinstance(target_date, str):
            self.target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            self.target_date = target_date

    def _weight_kg(self):
        return self.current_weight_lbs / LBS_PER_KG

    def bmr(self):
        """Mifflin-St Jeor equation (converts lbs to kg internally)."""
        base = 10 * self._weight_kg() + 6.25 * self.height_cm - 5 * self.age
        if self.gender == "male":
            return base - 5
        return base - 161

    def tdee(self):
        """Total Daily Energy Expenditure."""
        multiplier = ACTIVITY_MULTIPLIERS[self.activity_level]
        return self.bmr() * multiplier

    def daily_calorie_target(self):
        """TDEE adjusted for weight goal. Capped at 1000 kcal/day deficit, floor 1200 kcal."""
        days_remaining = (self.target_date - date.today()).days
        if days_remaining <= 0:
            return round(self.tdee())

        weight_delta = self.goal_weight_lbs - self.current_weight_lbs
        total_kcal_delta = weight_delta * KCAL_PER_LB
        daily_adjustment = total_kcal_delta / days_remaining

        # Cap deficit at 1000 kcal/day
        daily_adjustment = max(daily_adjustment, -1000)

        target = self.tdee() + daily_adjustment
        # Floor at 1200 kcal
        return round(max(target, 1200))

    def summary(self):
        """One-line summary for prompt injection."""
        return (
            f"TDEE {round(self.tdee())} kcal | "
            f"Daily target {self.daily_calorie_target()} kcal | "
            f"Goal: {self.current_weight_lbs}lbs → {self.goal_weight_lbs}lbs by {self.target_date}"
        )


if __name__ == "__main__":
    calc = BiometricCalculator(
        age=30, gender="male", height_cm=175,
        current_weight_lbs=176, activity_level="moderately_active",
        goal_weight_lbs=165, target_date="2026-06-01",
    )
    print(f"BMR:    {calc.bmr():.0f} kcal")
    print(f"TDEE:   {calc.tdee():.0f} kcal")
    print(f"Target: {calc.daily_calorie_target()} kcal")
    print(f"Summary: {calc.summary()}")
