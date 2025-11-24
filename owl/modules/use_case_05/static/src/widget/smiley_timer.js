import { patch } from "@web/core/utils/patch";
import { onMounted, onWillDestroy } from "@odoo/owl";
import { SmileyWidget } from "@use_case_03/widget/smiley_widget";

patch(SmileyWidget.prototype, {
    setup() {
        super.setup();
        this.state.isAngry = false;

        onMounted(() => {
            this.timer = setTimeout(() => {
                this.state.isAngry = true; 
            }, 5000); // 5000 is only for testing - while according to the exercise 1 minute corresponds to 60000
        });

        onWillDestroy(() => {
            if (this.timer) {
                clearTimeout(this.timer);
            }
        });
    },
    
    toggleMood() {
        if (this.state.isAngry) {
            this.notification.add("TOO LATE! CLOSE THE DEAL NOW!", {
                title: "ANGRY MANAGER",
                type: "danger",
            });
            return;
        }
        super.toggleMood();
    }
});
