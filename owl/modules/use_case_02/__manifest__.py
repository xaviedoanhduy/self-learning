{
    "name": "Use Case 02: Tyrannical Requests Font",
    "summary": "Change backend font to Oswald as requested by TR Inc.",
    "description": "Overrides the default system font with Oswald font for the entire Odoo backend interface.",
    "author": "Do Anh Duy",
    "maintainer": "xaviedoanhduy",
    "website": "https://github.com/xaviedoanhduy/self-learning",
    "category": "Customization",
    "version": "18.0.1.0.0",
    "depends": ["base", "web"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "use_case_02/static/src/scss/style.scss",
        ],
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
