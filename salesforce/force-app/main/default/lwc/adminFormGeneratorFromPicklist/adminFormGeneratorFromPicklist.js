import { LightningElement, api } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import getWeekCodesPicklist from '@salesforce/apex/WeekCodesPicklistController.getWeekCodesPicklist';


export default class AdminFormGeneratorFromPicklist extends LightningElement {
    @api recordIds;

    async fetchTokenID() {
        try {
            const loginResponse = await fetch("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBivMgQF_uNn7gm9-UwSRkm1CBVimMrrRo", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: 'bot@ilplatform.be',
                    password: 'ILP2022@',
                    returnSecureToken: true
                })
            });
            const loginJson = await loginResponse.json();
            const loginJson2 = await loginJson;
            const idToken = loginJson2?.idToken;
            return idToken;
        } catch (error) {
            console.error("There's a problem with your fetch operation:", error);
        }
    }

    async handleButtonClick() {
        await setTimeout(function() {window.history.back()}, 1000);

        if (!this.recordIds || this.recordIds.length === 0) {
            this.showToast('Error', 'No records selected', 'error');
            return;
        }

        const data = JSON.stringify(this.recordIds);

        const campCodes = await getWeekCodesPicklist({ recordIds: this.recordIds });

        const idToken = await this.fetchTokenID()
        const response = await fetch("https://admin-create-camps-form-vlfbkxu5pa-ew.a.run.app",
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + idToken,
                },
                'Access-Control-Allow-Origin': 'https://independentlearningplatform.lightning.force.com',
                body: JSON.stringify({ 
                    "data": {
                        "week_codes": campCodes.sort(),
                        "title": "Test"
                    }
                })
            }
        );
        const responseJSON = await response.json();
        if (responseJSON) {
            this.showToast('Success', 'API call successful', 'success');
        } else {
            console.error('Error:', error);
            this.showToast('Error', 'API call failed', 'error');
        }
    }

    showToast(title, message, variant) {
        const event = new ShowToastEvent({
            title: title,
            message: message,
            variant: variant,
        });
        this.dispatchEvent(event);
    }
}