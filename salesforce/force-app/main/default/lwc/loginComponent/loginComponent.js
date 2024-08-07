import { LightningElement, api, track } from 'lwc';

export default class LoginComponent extends LightningElement {
    @track email = '';
    @track password = '';
    @track loginErrorMessage = '';
    @track showLoginModal = false;

    // Handle change in email text field
    handleEmailChange(event) {
        this.email = event.target.value;
    }

    // Handle change in password text field
    handlePasswordChange(event) {
        this.password = event.target.value;
    }

    // Open the login modal
    openLoginModal() {
        this.showLoginModal = true;
    }

    // Close the login modal
    handleClose() {
        this.showLoginModal = false;
    }

    // On successful login, dispatch event to parent component
    handleLoginSuccess(idToken) {
        this.dispatchEvent(new CustomEvent('loginsuccess'), {idToken});
    }

    // Handle login by fetching and verifying token
    async login() {
        try {
            const idToken = await this.fetchTokenID(this.email, this.password);
            if (idToken) {
                localStorage.setItem('idToken', idToken);
                this.handleLoginSuccess(idToken);
                this.handleClose();
            } else {
                this.loginErrorMessage = 'Invalid login credentials. Please try again.';
            }
        } catch (error) {
            console.error('Login failed:', error);
            this.loginErrorMessage = 'Login failed. Please check your credentials and try again.';
        }
    }

    // Fetch the idToken based on email and password from the Google Identity Toolkit API
    async fetchTokenID(email, password) {
        try {
            const loginResponse = await fetch("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBivMgQF_uNn7gm9-UwSRkm1CBVimMrrRo", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    returnSecureToken: true
                })
            });
            const loginJson = await loginResponse.json();
            const idToken = loginJson?.idToken;
            return idToken;
        } catch (error) {
            console.error("There's a problem with your fetch operation:", error);
            throw error;
        }
    }

    // Retrieve the idToken stored locally
    static getStoredToken() {
        return localStorage.getItem('idToken');
    }
}