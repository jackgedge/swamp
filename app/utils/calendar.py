import requests
from icalendar import Calendar
from icalendar.parser import ContentHandler
from datetime import datetime

def parse_webcal(webcal_url):
    # Convert webcal:// to http://
    http_url = webcal_url.replace("webcal://", "http://", "webcals://")
    resp = requests.get(http_url)
    cal = Calendar.from_ical(resp.content)
    
    shifts = []
    for event in cal.walk("vevent"):
        shifts.append({
            "start": event.decoded("dtstart").dt,
            "end": event.decoded("dtend").dt,
            "summary": str(event.get("summary", "Shift"))
        })
    return shifts

