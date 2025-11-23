{
    "name": "Use Case 03: Motivation Smiley",
    "summary": "Adds a motivational smiley face to Sale Orders for TR Inc.",
    "description": "Injects a custom OWL widget displaying a smiley face into the Sale Order form view.",
    "author": "Do Anh Duy",
    "maintainer": "xaviedoanhduy",
    "website": "https://github.com/xaviedoanhduy/self-learning",
    "category": "Sales",
    "version": "18.0.1.0.0",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "use_case_03/static/src/widget/smiley_widget.js",
            "use_case_03/static/src/widget/smiley_widget.xml",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3"
}
