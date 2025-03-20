// Logs an audio event to the journal for further processing
// #needsFile 
let filePath = event.file.filePath;
// Update this to yor path
let basePath = "/Users/erickshaffer/code/AutoMeet";
let journalFile = `${basePath}/data/journal.txt`;
let timestamp = new Date().toISOString();

// Just append the file entry
let command = `echo "${filePath},${timestamp}" >> ${journalFile}`;
app.runShellCommand(command);
