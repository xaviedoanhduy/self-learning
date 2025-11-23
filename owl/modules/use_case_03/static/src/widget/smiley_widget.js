import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class SmileyWidget extends Component {
    static template = "use_case_03.SmileyWidget";
    setup() {
        super.setup();
        this.state = useState({
            isCool: false, // Normal smiley
        });
    }
    toggleMood() {
        this.state.isCool = !this.state.isCool;
    }
}

export const smileyWidget = {
    component: SmileyWidget,
    supportedAttributes: [],
};

registry.category("view_widgets").add("smiley_face", smileyWidget);
