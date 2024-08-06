import { LightningElement } from 'lwc';
import getWeekCodes from '@salesforce/apex/WeekCodesController.getWeekCodes';


export default class ExampleLWC extends LightningElement {
    weekCodes = [];
    data = {
        title: "",
        checked: []
    };
    buttonClicked = false;
    linkObtained = false;
    link = null;

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

    // async fetchWeekCodes() {
    //     // event.preventDefault();
    //     try {
    //         const idToken = await this.fetchTokenID()
    //         console.log(idToken);
    //         const response = await fetch("https://admin-get-week-codes-vlfbkxu5pa-ew.a.run.app",
    //             {
    //                 method: "POST",
    //                 headers: {
    //                     'Content-Type': 'application/json',
    //                     "Authorization": "Bearer " + idToken,
    //                 },
    //                 'Access-Control-Allow-Origin': 'https://independentlearningplatform.lightning.force.com',
    //                 body: JSON.stringify({ 
    //                     "data": {

    //                     }
    //                 })
    //             }
    //         );
    //         if (!response.ok) {
    //             throw Error(response);
    //         }
    //         const myItems = await response.json();
    //         const myResult = await myItems;
    //         console.log(myResult);
    //         return myResult?.data?.response;
    //     } catch (error) {
    //       console.error("There's a problem with your fetch operation:", error);
    //     }
    // }

    connectedCallback() {
        getWeekCodes()
            .then(result => {
                this.weekCodes = result;
            })
            .catch(error => {
                console.log(error);
            });
    }

    // async loadWeekCodes() {
    //     this.weekCodes = await this.fetchWeekCodes();
    // }

    handleText(event) {
        this.data.title = event.target.value;
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

    async generateForm() {
        console.log("Clicked", this.data.checked.sort(), "/", this.data.title);
        this.buttonClicked = true;

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
                        "week_codes": this.data.checked.sort(),
                        "title": this.data.title
                    }
                })
            }
        );
        if (!response.ok) {
            throw Error(response);
        }
        const myItems = await response.json();
        const myResult = await myItems;
        this.link = myResult?.data?.response;
        this.linkObtained = true;
        console.log(this.link);
        this.template.querySelector(".link").innerHTML = this.link;
    }
}

// CHECK OUT https://webcomponents.dev/pricing/