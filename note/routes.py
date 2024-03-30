from flask import jsonify, make_response
from note import note


# Routes
@note.route("/")
def home():
    return jsonify({"message": "Yup! I'm here!"})


@note.route("/notes")
def notes():
    return jsonify({"notes": [
        "Fletcher,\n\nHere are some tasks for you to do:\n\n1 - Add more products to the shop\n2 - Add the shop to the navigation bar\n3 - Update the blog posts\n4 - Fix the crappy theme\n\nThere's some other bits in the dev endpoint.\n\n~ Graham\nP.S. Don't forget to update the change log!!"
    ]})


@note.route("/dev")
def dev():
    res = make_response("Do your job!")
    res.mimetype = "text/plain"
    return jsonify(["Do your job!"])


@note.route("/changelog")
def changelog():
    changelog = {
        "log": [
            {
                "version": "1.0.0 (2023-02-10)",
                "version_notes": [
                    "Well, it's a lovely afternoon",
                    "And I almost forgot that my heart was broken in two",
                    "It's a goddamn beautiful day",
                    "Yeah, the sun is shining again",
                    "It slipped my mind I got stabbed in the back by my best friend",
                    "It's a goddamn beautiful day",
                    "So I think I'll take a walk around",
                    "And pretend like I don't see my whole world crashing down",
                    "It's a goddamn beautiful day",
                ],
            },
            {
                "version": "1.1.0 (2023-05-05)",
                "version_notes": [
                    "And all these assholes all over this town",
                    "Well, nothing they can do is gonna bring me down",
                    "All these assholes try to ruin my life",
                    "But I just can't help but give 'em all a smile",
                ],
            },
            {
                "version": "1.2.0 (2023-07-17)",
                "version_notes": [
                    "Well, I look right up to the sky",
                    "My thoughts start racing, but the clouds just float on by",
                    "It's a goddamn beautiful day",
                    "And the birds in the tops of the trees",
                    "Make me feel like the whole world didn't bring me to my knees",
                    "It's a goddamn beautiful day",
                ],
            },
            {
                "version": "1.3.0 (2023-10-22)",
                "version_notes": [
                    "And all these assholes all over this town",
                    "Well, nothing they can do is gonna bring me down",
                    "All these assholes try to ruin my life",
                    "But I just can't help but give 'em all a smile",
                    "And it's a goddamn beautiful day",
                ],
            },
            {
                "version": "1.4.0 (2023-11-30)",
                "version_notes": [
                    "And I don't care anymore",
                    "About the way this all works out",
                    "I don't care anymore",
                    "About the bullshit out of your mouth",
                    "I don't care anymore",
                    "Just let it all burn to the ground",
                    "Because I've got nothing left to lose",
                    "And that means I've got nothing I have to prove",
                ],
            },
            {
                "version": "1.5.0 (2024-01-15)",
                "version_notes": [
                    "Well, it's a lovely afternoon",
                    "And I almost forgot that my heart was broken in two",
                    "It's a goddamn beautiful day",
                    "And I guess things aren't so bad",
                    "I lost everything else, but hey, I still got my health",
                ],
            },
            {"version": "2.0.0 (2024-03-22)", "version_notes": ["CBN{curl_me_maybe_4a7972e6}"]},
        ]
    }
    return jsonify(changelog)
