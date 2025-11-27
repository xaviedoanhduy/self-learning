import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class CalculatorWidget extends Component {
    static template = "use_case_06.Calculator";

    setup() {
        this.state = useState({
            firstNumber: 0,
            secondNumber: 0,
        });
    }

    get total() {
        return (
            (parseFloat(this.state.firstNumber) || 0) +
            (parseFloat(this.state.secondNumber) || 0)
        );
    }
}

export const calculatorWidget = {
    component: CalculatorWidget,
};

registry.category("view_widgets").add("simple_calculator", calculatorWidget);
