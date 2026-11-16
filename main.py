from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import flask

app = flask.Flask(__name__, static_folder="assets", static_url_path="/assets")


@app.route("/", methods=["GET", "POST"])
def start():
    return flask.redirect("/home")


@app.route("/home", methods=["GET", "POST"])
def insert():
    form = flask.request.form
    planned_times = form.getlist("planned_time") or [""]
    errors = []
    submitted = flask.request.method == "POST"

    if submitted:
        if not form.get("title", "").strip():
            errors.append("Enter a task title.")
        if not form.get("description", "").strip():
            errors.append("Enter a description.")

        try:
            today = datetime.now(ZoneInfo(form.get("timezone") or "UTC")).date()
        except (ZoneInfoNotFoundError, ValueError):
            today = datetime.now(ZoneInfo("UTC")).date()

        try:
            due = datetime.strptime(form.get("due", ""), "%Y-%m-%dT%H:%M")
        except ValueError:
            errors.append("Enter a valid due date and time.")
        else:
            if due.date() <= today:
                errors.append("The due date must be later than today.")

        for number, value in enumerate(planned_times, start=1):
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M")
            except ValueError:
                errors.append(f"Enter a valid date and time for work session {number}.")

        if form.get("notification") not in {"none", "email", "device"}:
            errors.append("Select a notification setting.")

    return flask.render_template(
        "homepage.html", form=form, planned_times=planned_times,
        errors=errors, accepted=submitted and not errors,
    ), 400 if errors else 200


if __name__ == "__main__":
    app.run(debug=False)
