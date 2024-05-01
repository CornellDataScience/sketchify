// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  // Function to send an IPC message to run the Python script
  // runPythonScript: () => ipcRenderer.send("run-python-script"),

  runPythonScript: (arrayBuffer: ArrayBuffer, cropCoords: any) => {
    ipcRenderer.send("run-python-script", arrayBuffer, cropCoords);
  },

  handlePythonScriptResponse: (callback: (response: any) => void) => {
    ipcRenderer.on("python-script-response", (event, response) =>
      callback(response)
    );
  },
});

// Function to subscribe to the Python script response IPC message
// handlePythonScriptResponse: (callback: any) => {
//   ipcRenderer.on("python-script-response", (event, ...args) =>
//     callback(...args)
//   );
// },
