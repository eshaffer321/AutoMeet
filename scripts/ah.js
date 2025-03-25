// Logs an audio event to the journal for further processing
// #needsFile 

let filePath = event.file.filePath;

// Use well-known symlink path created by setup.sh
let journalFile = "~/AudioHijackLogs/journal.txt";
let timestamp = new Date().toISOString();

// Just append the file entry
let command = `echo "${filePath},${timestamp}" >> "${journalFile}"`;
app.runShellCommand(command);