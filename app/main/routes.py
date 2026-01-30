from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Shift
from app.main import main_bp
import requests
from icalendar import Calendar

def parse_webcal(webcal_url):
    http_url = webcal_url.replace("webcal://", "http://").replace("webcals://", "https://")
    resp = requests.get(http_url)
    cal = Calendar.from_ical(resp.content)
    shifts = []
    for event in cal.walk("vevent"):
        dtstart = event.decoded("dtstart")
        dtend = event.decoded("dtend")
        shifts.append({
            "start": dtstart if hasattr(dtstart, 'dt') else dtstart,
            "end": dtend if hasattr(dtend, 'dt') else dtend,
            "summary": str(event.get("summary", "Shift"))
        })
    return shifts

@main_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    shifts = Shift.query.filter_by(user_id=current_user.id).all()
    return render_template("main/home.html", title="Home", shifts=shifts)

@main_bp.route("/upload_calendar", methods=["POST"])
@login_required
def upload_calendar():
    webcal_url = request.form["webcal_url"]
    shifts = parse_webcal(webcal_url)
    for shift in shifts:
        new_shift = Shift(
            user_id=current_user.id,
            start=shift["start"],
            end=shift["end"],
            summary=shift["summary"]
        )
        db.session.add(new_shift)
    db.session.commit()
    flash(f"Uploaded {len(shifts)} shifts")
    return redirect(url_for("main.home"))

