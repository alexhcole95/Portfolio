// the current date
const now = new Date();

// the URL of the external IPs updated via API
const url = "https://ip-ranges.shipt.com/";

// the RegExp for IPv4
const pattern = /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/g;

// function that creates a trigger for automation purposes
function createTrigger() {
// this script will run every Tuesday at 19:30 CT.
  ScriptApp.newTrigger('automatedRetrieval')
      .timeBased()
      .atHour(19)
      .nearMinute(30)
      .everyWeeks(1)
      .onWeekDay(ScriptApp.WeekDay.TUESDAY)
      .create();
}

// function that creates a new spreadsheet
function automatedRetrieval() {
  // id of the folder titled 'GCP Reports'
  var folder = "[folder ID]";

  // retrieves the date at runtime and formats it to MMM DD, YYYY
  var date = Utilities.formatDate(now, 'America/Chicago', 'MMMM dd, yyyy');

  // creates a new spreadsheet named 'Report on "Current Date"'
  var fileName = "Report on " + date;
  var file = Drive.Files.insert({title: fileName, mimeType: MimeType.GOOGLE_SHEETS, parents: [{id: folder}]});

  // opens the sheet
  var ss = SpreadsheetApp.openById(file.id);
  var sheet = ss.getSheets()[0];

  // fetches and parses the data
  var response = UrlFetchApp.fetch(url);
  var data = JSON.parse(response.getContentText());

  // matches the data with the RegExp and appends to the sheet
  var match = pattern.exec(data)
  while ((match = pattern.exec(data.addresses)) !== null) {
    sheet.appendRow([match[0]]);
}
}