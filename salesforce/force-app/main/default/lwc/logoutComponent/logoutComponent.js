import { LightningElement, api } from 'lwc';

export default class LogoutComponent extends LightningElement {
    @api handleLogoutSuccess;

    logout() {
        localStorage.removeItem('idToken');
        this.handleLogoutSuccess();
    }
}