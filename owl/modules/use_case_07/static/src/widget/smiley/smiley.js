import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SmileyWidget } from "@use_case_03/widget/smiley_widget";
import { calculatorStore } from "@use_case_07/models/store";

patch(SmileyWidget.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
    },

    toggleMood() {
        const total = calculatorStore.currentTotal;
        if (total === 0) {
            super.toggleMood();
        } else {
            this.notification.add(`Current Calculator Total is: ${total}`, {
                title: "HR Friendly Reminder",
                type: "info",
                sticky: false,
            });
        }
    }
});
