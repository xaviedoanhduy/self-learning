{
    "name": "Use Case 07: Calculate Instead (Clean Architecture)",
    "summary": "Connects Smiley and Calculator using a shared Store.",
    "description": "Implements a separate store to allow the Smiley widget to display the Calculator's total without direct dependency.",
    "author": "Do Anh Duy",
    "maintainer": "xaviedoanhduy",
    "category": "Sales",
    "version": "18.0.1.0.0",
    "depends": ["use_case_03", "use_case_06"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "use_case_07/static/src/models/store.js",
            "use_case_07/static/src/component/calculator/calculator.js",
            "use_case_07/static/src/component/calculator/calculator.xml",
            "use_case_07/static/src/widget/smiley/smiley.js",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3"
}
