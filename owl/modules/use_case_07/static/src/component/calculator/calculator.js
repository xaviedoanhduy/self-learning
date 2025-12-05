import { patch } from "@web/core/utils/patch";
import { useEffect } from "@odoo/owl";
import { CalculatorWidget } from "@use_case_06/component/calculator/calculator";
import { calculatorStore } from "@use_case_07/models/store";

patch(CalculatorWidget.prototype, {
    setup() {
        super.setup();
        useEffect(() => {
            const total = (parseFloat(this.state.firstNumber) || 0) + (parseFloat(this.state.secondNumber) || 0);
            calculatorStore.currentTotal = total;
        }, () => [this.state.firstNumber, this.state.secondNumber]);
    },

    clearInputs() {
        this.state.firstNumber = 0;
        this.state.secondNumber = 0;
    }
});
