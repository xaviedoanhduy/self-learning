{
    "name": "Use Case 06: Simple Calculator",
    "summary": "A simple addition calculator widget for Sale Orders.",
    "description": "Adds a widget with two inputs that automatically sums up the values.",
    "author": "Do Anh Duy",
    "maintainer": "xaviedoanhduy",
    "category": "Sales",
    "version": "18.0.1.0.0",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "use_case_06/static/src/component/calculator/calculator.js",
            "use_case_06/static/src/component/calculator/calculator.xml",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3"
}
