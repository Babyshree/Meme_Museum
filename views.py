from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import requests
import os, json
from .api import get_api_data


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/memeinput", methods=["GET", "POST"])
@login_required
def memeinput():
    if request.method == "POST":
        json_response = get_meme()
        # meme=request.form.get("meme")
        # querystring = {"exclude-tags":"nsfw","keywords":meme,"min-rating":"7","include-tags":"one_liner","number":"3","max-length":"200"}
        # headers=get_api_data()
        # response = requests.get(os.environ['API_URL'], headers=headers, params=querystring)
        # print(type(response.json()))
        # return response.json()

        return redirect(url_for("views.get_meme"))
    return render_template("MemeInput.html", user=current_user)


@views.route("/showmeme")
@login_required
def generatememe():
    return render_template("generatedmeme.html", user=current_user)


@views.route("/meme")
def get_meme():
    meme = request.form.get("meme")
    print(meme)
    #  querystring = {
    #      "exclude-tags": "nsfw",
    #      "keywords": "rocket",
    #      "min-rating": "7",
    #      "include-tags": "one_liner",
    #      "number": "3",
    #      "max-length": "200",
    #  }
    querystring = {
        "keywords": meme,
        "media-type": "image",
        "keywords-in-image": "false",
        "min-rating": "3",
        "number": "3",
    }
    headers = get_api_data()
    response = requests.get(os.environ["API_URL"], headers=headers, params=querystring)
    print("\n\nResponse: ", response.json(), "\n\n\n")
    json_response = response.json()
    # return json.dumps(json_response)
    # json_response = {
    #     "memes": [
    #         {
    #             "id": 6698,
    #             "description": "Bezos, Phallic Rockets, Taxes. Twitter didn’t disappoint.: https://twitter.com/TheDailyShow/status/1417478230068563973?s=20",
    #             "url": "https://i.imgur.com/8JTc5z3.jpg",
    #             "type": "image/jpeg",
    #         },
    #         {
    #             "id": 237030,
    #             "description": "Rocket Money is a scam.: Prevented a $30 charge of something I don't use anymore. Feels good.",
    #             "url": "https://i.imgur.com/q3cZlpv.png",
    #             "type": "image/png",
    #         },
    #         {
    #             "id": 237032,
    #             "description": "Rocket Money is a scam.: Cat tax.",
    #             "url": "https://i.imgur.com/yaZoCFP.jpg",
    #             "type": "image/jpeg",
    #         },
    #     ],
    #     "available": 20,
    # }

    return render_template(
        "generatedmeme.html",
        user=current_user,
        json_response=json_response,
    )
