// Add the current file to Music.app
// #needsFile

let filePath = event.file.filePath;

// TODO: Clean up these paths
let base_path = "/Users/erickshaffer/code/whisperx";
let scriptPath = app.shellEscapeArgument(`${base_path}/src/move_and_rename.py`);
let pythonPath = app.shellEscapeArgument("/Users/erickshaffer/miniconda3/envs/whisperx/bin/python");
let escapedFilePath = app.shellEscapeArgument(filePath);

let command = `${pythonPath} ${scriptPath} ${escapedFilePath}`;
let [status, stdout, stderr] = app.runShellCommand(command);

if (stderr) {
  console.log(stderr);
}