import { LightningElement, track } from 'lwc';
import getWeekCodes from '@salesforce/apex/WeekCodesController.getWeekCodes';
import loginComponent from 'c/loginComponent';

export default class UpdateEventComponent extends LightningElement {
    weekCodes = [];
    data = {
        checked: []
    };
    buttonClicked = false;
    @track updateMessage = null;
    isLoggedIn = false;
    idToken = '';

    connectedCallback() {
        // Load week codes
        getWeekCodes()
            .then(result => {
                this.weekCodes = result;
            })
            .catch(error => {
                console.log(error);
            });

        // Check if user is already logged in
        this.idToken = loginComponent.getStoredToken();
        this.isLoggedIn = !!this.idToken;
    }

    handleChecked(event) {
        if (this.data.checked.includes(event.target.name)) {
            this.data.checked = this.data.checked.filter((i) => i !== event.target.name);
            this.data.checked = JSON.parse(JSON.stringify(this.data.checked));
        } else {
            this.data.checked = [...this.data.checked, event.target.name];
            this.data.checked = JSON.parse(JSON.stringify(this.data.checked))
        }
    }

    async updateEvents() {
        this.buttonClicked = true;
        this.updateMessage = 'The update function has been called and might take a few minutes. You can safely leave the page in the meantime.';

        try {
            const response = await fetch("https://admin-update-camps-events-vlfbkxu5pa-ew.a.run.app", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + this.idToken,
                },
                'Access-Control-Allow-Origin': 'https://independentlearningplatform.lightning.force.com',
                body: JSON.stringify({
                    "data": {
                        "week_codes": this.data.checked.sort()
                    }
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

        } catch (error) {
            console.error("There's a problem with your fetch operation:", error);
            this.updateMessage = 'An error occurred while updating events. Please try again.';
        } finally {
            this.updateMessage = 'Events created or updated successfully.';
        }
    }

    handleLoginSuccess(idToken) {
        this.idToken = idToken;
        this.isLoggedIn = true;
        this.closeLoginPopup();
    }
}