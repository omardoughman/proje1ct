// PiHub Google Apps Script Backend (main.gs)

// Simple in-memory log (use Sheets in real usage)
let LOGS = [];

/**
 * INIT endpoint (like /init)
 */
function doGet(e) {
  const action = e.parameter.action;

  if (action === "init") {
    return initSystem();
  }

  if (action === "logs") {
    return jsonResponse(LOGS);
  }

  return jsonResponse({ status: "ok", message: "PiHub running" });
}

/**
 * POST handler (send data)
 */
function doPost(e) {
  const data = JSON.parse(e.postData.contents || "{}");

  LOGS.push({
    time: new Date().toISOString(),
    data: data
  });

  return jsonResponse({ status: "saved", received: data });
}

/**
 * INIT system (like git init for your cloud backend)
 */
function initSystem() {
  LOGS = [];

  return jsonResponse({
    status: "initialized",
    message: "PiHub GS backend ready"
  });
}

/**
 * Helper: JSON response
 */
function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
