# Lightning Web Components for Salesforce

This project includes a set of Lightning Web Components (LWCs) designed to facilitate various functionalities within Salesforce. Notably, the `getFormComponent` and `updateEventsComponent` can be included as standalone components in apps, specifically on the Lightning Home Page.

## Components

### loginComponent
**Location**: `salesforce/force-app/main/default/lwc/loginComponent`  
**Former Names**: None  
**Description**: This reusable component provides a login modal for users to enter their email and password. It handles the authentication process by calling the Google Toolkit API and returns the token, which it can use to authenticate further actions.

### getFormComponent
**Location**: `salesforce/force-app/main/default/lwc/getFormComponent`  
**Former Names**: `adminGenerateForm`  
**Description**: This component allows users to generate a form by providing a title and selecting specific weeks from a list of checkboxes. If the user is not logged in, it displays a login button. Upon clicking, a login modal appears to enter credentials. Once logged in, the form generation functionality is enabled.

### updateEventsComponent
**Location**: `salesforce/force-app/main/default/lwc/updateEventsComponent`  
**Former Names**: None  
**Description**: This component allows users to update events by selecting specific weeks from a list of checkboxes. If the user is not logged in, it displays a login button. Upon clicking, a login modal appears to enter credentials. Once logged in, the event update functionality is enabled.

### adminFormGenerateButtonFromPicklist
**Location**: `salesforce/force-app/main/default/lwc/adminFormGenerateButtonFromPicklist`  
**Former Names**: `adminFormGenerateFromPicklist`  
**Description**: This component is intended to generate a form using a picklist for selection. Note: This component is currently a work in progress and does not function as expected.
