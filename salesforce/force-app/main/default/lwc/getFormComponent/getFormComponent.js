import { LightningElement, track } from 'lwc';
import getWeekCodes from '@salesforce/apex/WeekCodesController.getWeekCodes';
import loginComponent from 'c/loginComponent';

export default class GetFormComponent extends LightningElement {
    weekCodes = [];
    data = {
        title: "",
        checked: []
    };

    buttonClicked = false;
    @track linkObtained = false;
    @track link = null;
    isLoggedIn = false;

    idToken = '';
    @track updateMessage = null;

    connectedCallback() {
        // Retrieve the week codes through Apex controller getWeekCodes
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

    // Store the indicated title
    handleText(event) {
        this.data.title = event.target.value;
    }

    // Add or remove checked or unchecked weeks
    handleChecked(event) {
        if (this.data.checked.includes(event.target.name)) {
            this.data.checked = this.data.checked.filter((i) => i !== event.target.name);
            this.data.checked = JSON.parse(JSON.stringify(this.data.checked));
        } else {
            this.data.checked = [...this.data.checked, event.target.name];
            this.data.checked = JSON.parse(JSON.stringify(this.data.checked))
        }
    }

    // Store idToken after successful login
    handleLoginSuccess(event) {
        this.idToken = event.detail;
        this.isLoggedIn = true;
    }

    // Call API to generate form
    async generateForm() {
        console.log("Clicked", this.data.checked.sort(), "/", this.data.title);
        this.buttonClicked = true;
        this.updateMessage = 'Request recorded, form is being generated.';

        try {
            const response = await fetch("https://admin-create-camps-form-vlfbkxu5pa-ew.a.run.app", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + this.idToken,
                },
                'Access-Control-Allow-Origin': 'https://independentlearningplatform.lightning.force.com',
                body: JSON.stringify({
                    "data": {
                        "week_codes": this.data.checked.sort(),
                        "title": this.data.title
                    }
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const myItems = await response.json();
            this.link = myItems?.data?.response;
            this.linkObtained = true;
            this.template.querySelector(".link").innerHTML = "Form generated. Click to view.";
            this.updateMessage = '';
        } catch (error) {
            console.error("There's a problem with your fetch operation:", error);
            this.updateMessage = 'An error occurred while generating the form. Please try again.';
        }
    }
}