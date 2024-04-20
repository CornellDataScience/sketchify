const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // Function to send an IPC message to run the Python script
    runPythonScript: () => ipcRenderer.send('run-python-script'),

    // Function to subscribe to the Python script response IPC message
    handlePythonScriptResponse: (callback) => {
        ipcRenderer.on('python-script-response', (event, ...args) => callback(...args));
    }
});
