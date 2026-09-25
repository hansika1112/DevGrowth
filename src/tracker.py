import json
import csv
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

    try:
        problems = int(input("Coding problems solved today: "))

        if problems < 0:
            print("❌ Problems cannot be negative.")
            return

        hours = float(input("Hours spent coding: "))

        if hours < 0:
            print("❌ Coding hours cannot be negative.")
            return

    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    topic = input("Topic studied today: ").strip()
    learning = input("What did you learn today: ").strip()

    if not topic:
        print("❌ Topic cannot be empty.")
        return

    if not learning:
        print("❌ Learning description cannot be empty.")
        return

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


def add_custom_progress():
    data = load_data()

    print("\n📅 DevGrowth - Add Custom Date Progress")

    selected_date = input("Enter date (YYYY-MM-DD): ")

    try:
        date.fromisoformat(selected_date)
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        problems = int(input("Coding problems solved: "))

        if problems < 0:
            print("❌ Problems cannot be negative.")
            return

        hours = float(input("Hours spent coding: "))

        if hours < 0:
            print("❌ Coding hours cannot be negative.")
            return

    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    topic = input("Topic studied: ").strip()
    learning = input("What did you learn?: ").strip()

    if not topic:
        print("❌ Topic cannot be empty.")
        return

    if not learning:
        print("❌ Learning description cannot be empty.")
        return

    data.setdefault("daily_progress", {})

    data["daily_progress"][selected_date] = {
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

    print("\n✅ Custom date progress saved!")
    print(f"📅 Date: {selected_date}")
    print(f"💻 Problems: {problems}")
    print(f"⏱️ Coding Hours: {hours}")
    print(f"📚 Topic: {topic}")
    print(f"🧠 Learning: {learning}")

def edit_progress():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    if not daily_progress:
        print("\n❌ No progress data available.")
        return

    selected_date = input("\nEnter date to edit (YYYY-MM-DD): ")

    if selected_date not in daily_progress:
        print("❌ No progress found for this date.")
        return

    print("\nCurrent Progress:")
    print(f"💻 Problems: {daily_progress[selected_date]['problems']}")
    print(f"⏱️ Hours: {daily_progress[selected_date]['hours']}")
    print(f"📚 Topic: {daily_progress[selected_date]['topic']}")
    print(f"🧠 Learning: {daily_progress[selected_date]['learning']}")

    try:
        problems = int(input("\nCoding problems solved: "))

        if problems < 0:
            print("❌ Problems cannot be negative.")
            return

        hours = float(input("Hours spent coding: "))

        if hours < 0:
            print("❌ Coding hours cannot be negative.")
            return

    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    topic = input("Topic studied: ").strip()
    learning = input("What did you learn?: ").strip()

    if not topic:
        print("❌ Topic cannot be empty.")
        return

    if not learning:
        print("❌ Learning description cannot be empty.")
        return

    daily_progress[selected_date] = {
        "problems": problems,
        "hours": hours,
        "topic": topic,
        "learning": learning
    }

    total_problems = 0
    total_hours = 0

    for progress in daily_progress.values():
        total_problems += progress["problems"]
        total_hours += progress["hours"]

    data["coding"]["problems_solved"] = total_problems
    data["coding"]["hours"] = total_hours
    data["total_days"] = len(daily_progress)
    data["current_streak"] = calculate_streak(daily_progress)

    save_data(data)

    print("\n✅ Progress updated successfully!")

def delete_progress():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    if not daily_progress:
        print("\n❌ No progress data available.")
        return

    selected_date = input("\nEnter date to delete (YYYY-MM-DD): ")

    try:
        date.fromisoformat(selected_date)
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    if selected_date not in daily_progress:
        print("❌ No progress found for this date.")
        return

    progress = daily_progress[selected_date]

    print("\nProgress to be deleted:")
    print(f"💻 Problems: {progress['problems']}")
    print(f"⏱️ Hours: {progress['hours']}")
    print(f"📚 Topic: {progress['topic']}")
    print(f"🧠 Learning: {progress['learning']}")

    confirmation = input("\nAre you sure you want to delete this progress? (yes/no): ")

    if confirmation.lower() != "yes":
        print("❌ Delete cancelled.")
        return

    del daily_progress[selected_date]

    total_problems = 0
    total_hours = 0

    for progress in daily_progress.values():
        total_problems += progress["problems"]
        total_hours += progress["hours"]

    data["coding"]["problems_solved"] = total_problems
    data["coding"]["hours"] = total_hours
    data["total_days"] = len(daily_progress)
    data["current_streak"] = calculate_streak(daily_progress)

    save_data(data)

    print("\n✅ Progress deleted successfully!")
    print(f"📅 Deleted Date: {selected_date}")
    print(f"💻 Total Problems: {total_problems}")
    print(f"⏱️ Total Coding Hours: {total_hours}")
    print(f"📅 Active Days: {len(daily_progress)}")
    print(f"🔥 Current Streak: {data['current_streak']}")
    
def search_progress():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    if not daily_progress:
        print("\n❌ No progress data available.")
        return

    keyword = input("\n🔎 Enter keyword to search: ").strip().lower()

    if not keyword:
        print("❌ Search keyword cannot be empty.")
        return

    found = False

    print("\n🔎 Search Results")
    print("================")

    for selected_date, progress in sorted(daily_progress.items()):
        topic = str(progress.get("topic", "")).lower()
        learning = str(progress.get("learning", "")).lower()
        problems = str(progress.get("problems", "")).lower()
        hours = str(progress.get("hours", "")).lower()

        if (
            keyword in selected_date.lower()
            or keyword in topic
            or keyword in learning
            or keyword in problems
            or keyword in hours
        ):
            found = True

            print(f"\n📅 Date: {selected_date}")
            print(f"💻 Problems: {progress['problems']}")
            print(f"⏱️ Hours: {progress['hours']}")
            print(f"📚 Topic: {progress['topic']}")
            print(f"🧠 Learning: {progress['learning']}")

    if not found:
        print(f"\n❌ No progress found for '{keyword}'.")

def export_progress():
    data = load_data()

    daily_progress = data.get("daily_progress", {})

    if not daily_progress:
        print("\n❌ No progress data available.")
        return

    file_path = "data/progress_export.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Problems",
            "Hours",
            "Topic",
            "Learning"
        ])

        for selected_date, progress in sorted(daily_progress.items()):
            writer.writerow([
                selected_date,
                progress["problems"],
                progress["hours"],
                progress["topic"],
                progress["learning"]
            ])

    print("\n✅ Progress exported successfully!")
    print(f"📄 File: {file_path}")
    print(f"📊 Records exported: {len(daily_progress)}")


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
        print("2. Add Custom Date Progress")
        print("3. Edit Progress")
        print("4. Delete Progress")
        print("5. Search Progress")
        print("6. Export Progress")
        print("7. View Progress")
        print("8. Weekly Report")
        print("9. Learning History")
        print("10. Set Goals")
        print("11. View Goals")
        print("12. Achievements")
        print("13. Monthly Report")
        print("14. Monthly Progress Graph")
        print("15. Progress Graph")
        print("16. Analytics Dashboard")
        print("17. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_progress()
        elif choice == "2":
            add_custom_progress()
        elif choice == "3":
            edit_progress()
        elif choice == "4":
            delete_progress()
        elif choice == "5":
            search_progress()
        elif choice == "6":
            export_progress()
        elif choice == "7":
            view_progress()
        elif choice == "8":
            weekly_report()
        elif choice == "9":
            learning_history()
        elif choice == "10":
            set_goals()
        elif choice == "11":
            view_goals()
        elif choice == "12":
            achievements()
        elif choice == "13":
            monthly_report()
        elif choice == "14":
            monthly_progress_graph()
        elif choice == "15":
            progress_graph()
        elif choice == "16":
            analytics_dashboard()
        elif choice == "17":
            print("\n🚀 Keep learning. Keep growing!")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()