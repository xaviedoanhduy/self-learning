import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SmileyWidget } from "@use_case_03/widget/smiley_widget";


patch(SmileyWidget.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
    },

    toggleMood() {
        super.toggleMood();

        if (!this.state.isCool) {
            this.notification.add("Get Back To Work!!!!!!", {
                title: "Manager Alert",
                type: "danger",
                sticky: false,
            });
        } else {
            this.notification.add("You're back!!!", {
                title: "Manager Alert",
                type: "success",
                sticky: false,
            });
        }
        
        console.log("Use Case 04: Patch executed successfully!");
    }
})
