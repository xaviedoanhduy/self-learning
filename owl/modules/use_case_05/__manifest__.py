{
    "name": "Use Case 05: Upside Down Frown",
    "summary": "Turns the smiley into an angry face after 1 minute.",
    "description": "Adds a timer to the SmileyWidget. Changes functionality to show an angry face if the sale takes too long.",
    "author": "Do Anh Duy",
    "maintainer": "xaviedoanhduy",
    "category": "Sales",
    "version": "18.0.1.0.0",
        "depends": ["use_case_04"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "use_case_05/static/src/widget/smiley_timer.js",
            "use_case_05/static/src/widget/smiley_timer.xml",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3"
}
