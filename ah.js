// add the current file to Music.app
// #needsFile

// TODO: Clean up these paths
let filePath = event.file.filePath;
let base_path =  "/Users/erickshaffer/code/whisperx"
let scriptPath = `${base_path}/move_and_rename.py"`;
let pythonPath = "/Users/erickshaffer/miniconda3/envs/whisperx/bin/python"

let command = `${pythonPath} ${scriptPath} "${filePath}"`;
let [status, stdout, stderr] = app.runShellCommand( command );

if (stderr) {
  console.log(stderr)
}