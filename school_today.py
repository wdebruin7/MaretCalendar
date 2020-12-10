from datetime import datetime

import requests
from bs4 import BeautifulSoup

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def school_today():

    now = datetime.now()

    if now.weekday == 0 or now.weekday == 6:
        return False

    str_month = str(now.month - 1)
    str_day = str(now.day)

    return not closure_event(str_month=str_month, str_day=str_day)


def closure_event(str_month=11, str_day=21):
    now = datetime.now()
    calendar_url = "https://www.maret.org/school-life/calendar"
    page = requests.get(calendar_url)
    soup = BeautifulSoup(page.content, "html.parser")

    elems = soup.find_all(
        attrs={"data-day": str_day, "data-month": str_month},
    )

    important_events = get_important_events(soup)
    today_text = ""

    try:
        today_text = elems[0].parent.find("a").text
    except:
        return False

    for event_text in important_events:
        if today_text in event_text:
            return True

    return False


def get_important_events(soup):
    list_elements = soup.find_all("li")
    return [item.text for item in list_elements if is_valid_event(item.text)] + [
        "Winter Break",
        "Spring Break",
    ]


def is_valid_event(item_text):
    words = item_text.split()

    # determine if it is a calendar event
    # must match pattern {day} OR {day}-{day}
    if len(words) <= 0:
        return False

    first_word = words[0]
    is_calendar_event = first_word in days

    if not is_calendar_event and "-" in first_word:
        first_word_split = first_word.split("-")[0]
        is_calendar_event = first_word_split in days

    return is_calendar_event
