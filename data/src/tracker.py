import json
from datetime import date

FILE = "data/progress.json"


def load_data():
    with open(FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_progress():
    data = load_data()

    print("\n🌱 DevGrowth - Add Today's Progress")

    problems = int(input("Coding problems solved today: "))
    hours = float(input("Hours spent coding: "))

    data["coding"]["problems_solved"] += problems
    data["coding"]["hours"] += hours
    data["total_days"] += 1

    today = str(date.today())

    data.setdefault("daily_progress", {})
    data["daily_progress"][today] = {
        "problems": problems,
        "hours": hours
    }

    save_data(data)

    print("\n✅ Today's progress saved!")
    print(f"📅 Date: {today}")
    print(f"💻 Problems: {problems}")
    print(f"⏱️ Coding Hours: {hours}")


def view_progress():
    data = load_data()

    print("\n📊 Developer Progress")
    print("-------------------------")
    print(f"🔥 Current Streak: {data['current_streak']}")
    print(f"📅 Total Days: {data['total_days']}")
    print(f"💻 Problems Solved: {data['coding']['problems_solved']}")
    print(f"⏱️ Coding Hours: {data['coding']['hours']}")


def main():
    while True:
        print("\n🌱 DevGrowth Tracker")
        print("-------------------------")
        print("1. Add Today's Progress")
        print("2. View Progress")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_progress()
        elif choice == "2":
            view_progress()
        elif choice == "3":
            print("\n🚀 Keep learning. Keep growing!")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
