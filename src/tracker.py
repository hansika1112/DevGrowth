import json
import matplotlib.pyplot as plt
from datetime import date, timedelta

FILE = "data/progress.json"


def load_data():
    with open(FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)


def calculate_streak(daily_progress):
    if not daily_progress:
        return 0

    today = date.today()
    yesterday = today - timedelta(days=1)

    if str(today) in daily_progress:
        check_date = today
    elif str(yesterday) in daily_progress:
        check_date = yesterday
    else:
        return 0

    streak = 0

    while str(check_date) in daily_progress:
        streak += 1
        check_date -= timedelta(days=1)

    return streak


def add_progress():
    data = load_data()

    print("\n🌱 DevGrowth - Add Today's Progress")

    problems = int(input("Coding problems solved today: "))
    hours = float(input("Hours spent coding: "))
    topic = input("Topic studied today: ")
    learning = input("What did you learn today: ")

    today = str(date.today())

    data.setdefault("daily_progress", {})

    data["daily_progress"][today] = {
        "problems": problems,
        "hours": hours,
        "topic": topic,
        "learning": learning
    }

    total_problems = 0
    total_hours = 0

    for progress in data["daily_progress"].values():
        total_problems += progress["problems"]
        total_hours += progress["hours"]

    data["coding"]["problems_solved"] = total_problems
    data["coding"]["hours"] = total_hours
    data["total_days"] = len(data["daily_progress"])
    data["current_streak"] = calculate_streak(data["daily_progress"])

    save_data(data)

    print("\n✅ Today's progress saved!")
    print(f"📅 Date: {today}")
    print(f"💻 Problems: {problems}")
    print(f"⏱️ Coding Hours: {hours}")
    print(f"📚 Topic: {topic}")
    print(f"🧠 Learning: {learning}")


def view_progress():
    data = load_data()

    daily_progress = data.get("daily_progress", {})
    current_streak = calculate_streak(daily_progress)

    print("\n📊 Developer Progress")
    print("-------------------------")
    print(f"🔥 Current Streak: {current_streak}")
    print(f"📅 Total Days: {len(daily_progress)}")
    print(f"💻 Problems Solved: {data['coding']['problems_solved']}")
    print(f"⏱️ Coding Hours: {data['coding']['hours']}")


def weekly_report():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    today = date.today()
    week_start = today - timedelta(days=6)

    total_problems = 0
    total_hours = 0
    active_days = 0

    for day, progress in daily_progress.items():
        progress_date = date.fromisoformat(day)

        if week_start <= progress_date <= today:
            total_problems += progress["problems"]
            total_hours += progress["hours"]
            active_days += 1

    current_streak = calculate_streak(daily_progress)

    if active_days > 0:
        average_problems = total_problems / active_days
        average_hours = total_hours / active_days
    else:
        average_problems = 0
        average_hours = 0

    print("\n📊 Weekly Progress Report")
    print("-------------------------")
    print(f"🗓️ Period: {week_start} to {today}")
    print(f"🧠 Total Problems: {total_problems}")
    print(f"⏱️ Total Coding Hours: {total_hours:.1f}")
    print(f"📅 Active Days: {active_days}")
    print(f"🔥 Current Streak: {current_streak}")
    print(f"📈 Average Problems/Day: {average_problems:.1f}")
    print(f"⏰ Average Coding Hours/Day: {average_hours:.1f}")

def monthly_report():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    today = date.today()
    current_month = today.month
    current_year = today.year

    total_problems = 0
    total_hours = 0
    active_days = 0

    for day, progress in daily_progress.items():
        progress_date = date.fromisoformat(day)

        if progress_date.month == current_month and progress_date.year == current_year:
            total_problems += progress["problems"]
            total_hours += progress["hours"]
            active_days += 1

    current_streak = calculate_streak(daily_progress)

    if active_days > 0:
        average_problems = total_problems / active_days
        average_hours = total_hours / active_days
    else:
        average_problems = 0
        average_hours = 0

    print("\n📅 Monthly Progress Report")
    print("=========================")
    print(f"🗓️ Month: {today.strftime('%B %Y')}")
    print(f"🧠 Total Problems: {total_problems}")
    print(f"⏱️ Total Coding Hours: {total_hours:.1f}")
    print(f"📅 Active Days: {active_days}")
    print(f"🔥 Current Streak: {current_streak}")
    print(f"📈 Average Problems/Day: {average_problems:.1f}")
    print(f"⏰ Average Coding Hours/Day: {average_hours:.1f}")

def monthly_progress_graph():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    today = date.today()
    current_month = today.month
    current_year = today.year

    dates = []
    problems = []
    hours = []

    for day, progress in sorted(daily_progress.items()):
        progress_date = date.fromisoformat(day)

        if progress_date.month == current_month and progress_date.year == current_year:
            dates.append(progress_date.strftime("%d %b"))
            problems.append(progress["problems"])
            hours.append(progress["hours"])

    if not dates:
        print("\n❌ No progress data available for this month.")
        return

    plt.figure(figsize=(10, 5))

    plt.plot(dates, problems, marker="o", label="Problems Solved")
    plt.plot(dates, hours, marker="o", label="Coding Hours")

    plt.title(f"Monthly Progress - {today.strftime('%B %Y')}")
    plt.xlabel("Date")
    plt.ylabel("Progress")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.show()


def learning_history():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    print("\n📚 Learning History")
    print("=========================")

    if not daily_progress:
        print("No learning history available yet.")
        return

    for day in sorted(daily_progress.keys(), reverse=True):
        progress = daily_progress[day]

        print(f"\n📅 {day}")
        print(f"💻 Problems: {progress['problems']}")
        print(f"⏱️ Coding Hours: {progress['hours']}")
        print(f"📚 Topic: {progress.get('topic', 'Not added')}")
        print(f"🧠 Learned: {progress.get('learning', 'Not added')}")
        print("-------------------------")


def set_goals():
    data = load_data()

    print("\n🎯 DevGrowth - Set Goals")
    print("-------------------------")

    daily_problems = int(input("Daily Problems Goal: "))
    daily_hours = float(input("Daily Coding Hours Goal: "))
    weekly_problems = int(input("Weekly Problems Goal: "))
    weekly_hours = float(input("Weekly Coding Hours Goal: "))

    data["goals"] = {
        "daily_problems": daily_problems,
        "daily_hours": daily_hours,
        "weekly_problems": weekly_problems,
        "weekly_hours": weekly_hours
    }

    save_data(data)

    print("\n✅ Goals saved successfully!")
    
def progress_bar(percentage, length=20):
    filled = int(length * percentage / 100)
    empty = length - filled
    return "█" * filled + "░" * empty

def view_goals():
    data = load_data()

    goals = data.get("goals")

    if not goals:
        print("\n❌ No goals set yet.")
        return

    daily_progress = data.get("daily_progress", {})
    today = str(date.today())

    today_data = daily_progress.get(
        today,
        {
            "problems": 0,
            "hours": 0
        }
    )

    week_start = date.today() - timedelta(days=6)

    weekly_problems = 0
    weekly_hours = 0

    for day, progress in daily_progress.items():
        progress_date = date.fromisoformat(day)

        if week_start <= progress_date <= date.today():
            weekly_problems += progress["problems"]
            weekly_hours += progress["hours"]

    daily_problem_percent = min(
        (today_data["problems"] / goals["daily_problems"]) * 100
        if goals["daily_problems"] > 0 else 0,
        100
    )

    daily_hours_percent = min(
        (today_data["hours"] / goals["daily_hours"]) * 100
        if goals["daily_hours"] > 0 else 0,
        100
    )

    weekly_problem_percent = min(
        (weekly_problems / goals["weekly_problems"]) * 100
        if goals["weekly_problems"] > 0 else 0,
        100
    )

    weekly_hours_percent = min(
        (weekly_hours / goals["weekly_hours"]) * 100
        if goals["weekly_hours"] > 0 else 0,
        100
    )

    print("\n🎯 Your Goals")
    print("=========================")

    print("\n📅 Daily Progress")
    print(f"💻 Problems: {today_data['problems']} / {goals['daily_problems']}")
    print(f"⏱️ Hours: {today_data['hours']} / {goals['daily_hours']}")
    print(f"📈 Problems Progress: {daily_problem_percent:.0f}%")
    print(f"   {progress_bar(daily_problem_percent)}")

    print(f"📈 Hours Progress: {daily_hours_percent:.0f}%")
    print(f"   {progress_bar(daily_hours_percent)}")

    print("\n📊 Weekly Progress")
    print(f"💻 Problems: {weekly_problems} / {goals['weekly_problems']}")
    print(f"⏱️ Hours: {weekly_hours} / {goals['weekly_hours']}")
    print(f"📈 Problems Progress: {weekly_problem_percent:.0f}%")
    print(f"   {progress_bar(weekly_problem_percent)}")

    print(f"📈 Hours Progress: {weekly_hours_percent:.0f}%")
    print(f"   {progress_bar(weekly_hours_percent)}")

    if daily_problem_percent >= 100 and daily_hours_percent >= 100:
        print("\n🔥 Daily Goal Completed!")

    if weekly_problem_percent >= 100 and weekly_hours_percent >= 100:
        print("🏆 Weekly Goal Completed!")

def progress_graph():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    if not daily_progress:
        print("\n❌ No progress data available.")
        return

    dates = sorted(daily_progress.keys())

    problems = []
    hours = []

    for day in dates:
        problems.append(daily_progress[day]["problems"])
        hours.append(daily_progress[day]["hours"])

    short_dates = [day[5:] for day in dates]

    plt.figure(figsize=(10, 5))

    plt.plot(short_dates, problems, marker="o", label="Problems Solved")
    plt.plot(short_dates, hours, marker="o", label="Coding Hours")

    plt.title("🌱 DevGrowth Progress")
    plt.xlabel("Date")
    plt.ylabel("Progress")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def achievements():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    total_problems = data["coding"]["problems_solved"]
    total_hours = data["coding"]["hours"]
    total_days = len(daily_progress)
    current_streak = calculate_streak(daily_progress)

    print("\n🏆 DevGrowth Achievements")
    print("=========================")

    if total_days >= 1:
        print("\n🔥 First Step")
        print("   Complete your first coding day")
        print("   ✅ Unlocked")
    else:
        print("\n🔥 First Step")
        print("   Complete your first coding day")
        print("   🔒 Locked")

    if total_problems >= 10:
        print("\n💻 Problem Solver")
        print("   Solve 10 coding problems")
        print("   ✅ Unlocked")
    else:
        print("\n💻 Problem Solver")
        print("   Solve 10 coding problems")
        print(f"   🔒 {10 - total_problems} more problems needed")

    if total_problems >= 50:
        print("\n🚀 Rising Developer")
        print("   Solve 50 coding problems")
        print("   ✅ Unlocked")
    else:
        print("\n🚀 Rising Developer")
        print("   Solve 50 coding problems")
        print(f"   🔒 {50 - total_problems} more problems needed")

    if total_problems >= 100:
        print("\n🏆 Coding Master")
        print("   Solve 100 coding problems")
        print("   ✅ Unlocked")
    else:
        print("\n🏆 Coding Master")
        print("   Solve 100 coding problems")
        print(f"   🔒 {100 - total_problems} more problems needed")

    if total_hours >= 10:
        print("\n⏱️ Coding Warrior")
        print("   Complete 10 coding hours")
        print("   ✅ Unlocked")
    else:
        print("\n⏱️ Coding Warrior")
        print("   Complete 10 coding hours")
        print(f"   🔒 {10 - total_hours:.1f} more hours needed")

    if total_hours >= 50:
        print("\n💪 Dedicated Coder")
        print("   Complete 50 coding hours")
        print("   ✅ Unlocked")
    else:
        print("\n💪 Dedicated Coder")
        print("   Complete 50 coding hours")
        print(f"   🔒 {50 - total_hours:.1f} more hours needed")

    if current_streak >= 7:
        print("\n📚 Consistent Learner")
        print("   Maintain a 7-day streak")
        print("   ✅ Unlocked")
    else:
        print("\n📚 Consistent Learner")
        print("   Maintain a 7-day streak")
        print(f"   🔒 {7 - current_streak} more streak days needed")

    if current_streak >= 30:
        print("\n🔥 Unstoppable Developer")
        print("   Maintain a 30-day streak")
        print("   ✅ Unlocked")
    else:
        print("\n🔥 Unstoppable Developer")
        print("   Maintain a 30-day streak")
        print(f"   🔒 {30 - current_streak} more streak days needed")

def analytics_dashboard():
    data = load_data()

    coding = data.get("coding", {})
    daily_progress = data.get("daily_progress", {})

    total_problems = coding.get("problems_solved", 0)
    total_hours = coding.get("hours", 0)
    active_days = len(daily_progress)
    current_streak = calculate_streak(daily_progress)

    if active_days > 0:
        average_problems = total_problems / active_days
        average_hours = total_hours / active_days
    else:
        average_problems = 0
        average_hours = 0

    print("\n📊 DevGrowth Analytics Dashboard")
    print("===============================")
    print(f"💻 Total Problems Solved: {total_problems}")
    print(f"⏱️ Total Coding Hours: {total_hours}")
    print(f"📅 Active Days: {active_days}")
    print(f"🔥 Current Streak: {current_streak}")
    print(f"📈 Average Problems/Day: {average_problems:.1f}")
    print(f"⏰ Average Coding Hours/Day: {average_hours:.1f}")

def main():
    while True:
        print("1. Add Today's Progress")
        print("2. View Progress")
        print("3. Weekly Report")
        print("4. Learning History")
        print("5. Set Goals")
        print("6. View Goals")
        print("7. Achievements")
        print("8. Monthly Report")
        print("9. Monthly Progress Graph")
        print("10. Progress Graph")
        print("11. Analytics Dashboard")
        print("12. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_progress()
        elif choice == "2":
            view_progress()
        elif choice == "3":
            weekly_report()
        elif choice == "4":
            learning_history()
        elif choice == "5":
            set_goals()
        elif choice == "6":
            view_goals()
        elif choice == "7":
            achievements()
        elif choice == "8":
            monthly_report()
        elif choice == "9":
            monthly_progress_graph()
        elif choice == "10":
            progress_graph()
        elif choice == "11":
            analytics_dashboard()
        elif choice == "12":
            print("\n🚀 Keep learning. Keep growing!")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()