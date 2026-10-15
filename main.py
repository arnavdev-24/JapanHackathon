from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def match_score(japan, india):
    """Return an explainable potential-fit score from 0 to 100."""
    score = 0

    if japan["sector"] and japan["sector"] == india["sector"]:
        score += 30

    # Japan's requested partner capabilities should match India's offerings.
    if set(japan["needs"]) & set(india["offers"]):
        score += 40

    # Both sides should be open to the same type of partnership.
    if set(japan["partnership_types"]) & set(india["partnership_types"]):
        score += 15

    # Japan's target states should overlap India's operating regions.
    if "India" in india["regions"] or set(japan["regions"]) & set(india["regions"]):
        score += 15

    return score


@app.route("/")
def home():
    return render_template("land.html")


@app.route("/log", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/regi", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get() reads one value; getlist() reads all checked boxes.
        country = request.form.get("country")
        requested_or_offered = request.form.getlist("requirement")
        profile = {
            "country": country,
            "company_name": request.form.get("username", "").strip(),
            "sector": request.form.get("sector"),
            "description": request.form.get("description", "").strip(),
            "services": request.form.get("services", "").strip(),
            "regions": request.form.getlist("region"),
            "languages": request.form.getlist("language"),
            "partnership_types": request.form.getlist("partner"),
            "needs": requested_or_offered if country == "japan" else [],
            "offers": requested_or_offered if country == "india" else [],
        }
        print(profile)

        # At this stage the form is parsed but not saved to MySQL yet.
        # Do not print or store the submitted password.
        print("Registration profile received:", profile)
        # return redirect(url_for("home"))
        return ("Registration received. Profile data was read successfully.") 
        

    country = request.args.get("country")
    if country == "india":
        return render_template("registeri.html")
    if country == "japan":
        return render_template("registerj.html")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
