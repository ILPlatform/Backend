// Replace with the URL to your deployed Cloud Function
var url = "https://admin-update-teacher-contract-signed-vlfbkxu5pa-ew.a.run.app/"

// This function will be called when the form is submitted
function onSubmit(event) {

  // The event is a FormResponse object:
  // https://developers.google.com/apps-script/reference/forms/form-response
  var formResponse = event.response;

  // Gets all ItemResponses contained in the form response
  // https://developers.google.com/apps-script/reference/forms/form-response#getItemResponses()
  var itemResponses = formResponse.getItemResponses();

  // Gets the actual response strings from the array of ItemResponses
  var responses = itemResponses.map(function getResponse(e) { return e.getResponse(); });

  // Post the payload as JSON to our Cloud Function
  var options = {
    "method" : "post",
    "contentType": "application/json",
    "payload" : JSON.stringify({
      "data": {
        "SF_Code": responses[0],
        "Google_Link": DriveApp.getFileById(responses[1]).getUrl()
      }
    })
  };
  var res = UrlFetchApp.fetch(url, options);
  Logger.log(res.getContentText());
}
