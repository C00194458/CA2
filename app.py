import os
from flask import Flask, render_template, request

import hfpy_utils
import swim_utils

app = Flask(__name__)
FOLDER = "swimdata/"


@app.get("/")
def get_swimmers_names():
    files = os.listdir(FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names_parts = swimmer.removesuffix(".txt").split("-")[:2]
        formatted_name = "-".join(names_parts)
        names.add(formatted_name)

    return render_template(
        "select.html",
        title="Select a swimmer",
        data=sorted(names),
    )


@app.post("/displayevents")
def get_swimmer_events():
    selected_swimmer = request.form["swimmer"]
    files = os.listdir(FOLDER)
    swimmer_events = set()

    for swimmer_file in files:
        if swimmer_file.startswith(selected_swimmer):
            event_parts = swimmer_file.removesuffix(".txt").split("-")
            if len(event_parts) >= 3:
                swimmer_event = "-".join(event_parts[2:])
                swimmer_events.add(swimmer_event)

    return render_template(
        "select2.html",
        title=f"Select an event for {selected_swimmer}",
        data=sorted(swimmer_events),
        selected_swimmer=selected_swimmer,
    )


@app.post("/displaychart")
def display_chart():
    selected_swimmer = request.form["swimmer"]
    selected_event = request.form["event"]
    filename = selected_swimmer + "-" + selected_event + ".txt"

    chart_data = swim_utils.produce_bar_chart(filename)

    return render_template("chart.html", chart_data=chart_data)


if __name__ == "__main__":
    app.run(debug=True)
