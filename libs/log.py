from datetime import datetime, timedelta, timezone


def log(e: str) -> None:
    with open("log.txt", "a") as file:
        file.write(f"\n{datetime.now(timezone(timedelta(hours=3, minutes=0), 'Moscow'))} - {e}\n")
