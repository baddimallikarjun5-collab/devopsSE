from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "clubsphere-change-this-secret"

# Demo data. Memberships are stored in memory and reset when the app restarts.
clubs = [
    {
        "name": "CodeSphere",
        "category": "Technology",
        "description": "Learn programming, build projects and take part in coding challenges.",
        "icon": "💻"
    },
    {
        "name": "Pixel Creators",
        "category": "Design",
        "description": "Explore graphic design, photography, UI/UX and creative media.",
        "icon": "🎨"
    },
    {
        "name": "RoboTech",
        "category": "Engineering",
        "description": "Experiment with robotics, electronics and automation projects.",
        "icon": "🤖"
    },
    {
        "name": "Literary Circle",
        "category": "Literature",
        "description": "Share stories, poetry, debates and public-speaking skills.",
        "icon": "📚"
    }
]

events = [
    {"title": "CodeSprint 2026", "date": "25 November 2026", "club": "CodeSphere"},
    {"title": "Creative Design Workshop", "date": "28 November 2026", "club": "Pixel Creators"},
    {"title": "Robotics Demo Day", "date": "02 December 2026", "club": "RoboTech"}
]

memberships = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        student_email = request.form.get("student_email", "").strip()
        selected_club = request.form.get("club", "").strip()

        valid_clubs = [club["name"] for club in clubs]

        if not student_name or not student_email or selected_club not in valid_clubs:
            flash("Please complete all fields and select a valid club.", "error")
        else:
            already_joined = any(
                member["email"].lower() == student_email.lower()
                and member["club"] == selected_club
                for member in memberships
            )

            if already_joined:
                flash("You have already joined this club with that email.", "error")
            else:
                memberships.append({
                    "name": student_name,
                    "email": student_email,
                    "club": selected_club
                })
                flash(f"Welcome, {student_name}! You joined {selected_club}.", "success")

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        clubs=clubs,
        events=events,
        memberships=memberships
    )


@app.route("/health")
def health():
    return {"status": "healthy", "application": "ClubSphere"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
