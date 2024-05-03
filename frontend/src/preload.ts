// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  // Function to send an IPC message to run the Python script
  runPythonScript: () => ipcRenderer.send("run-python-script"),
  runModel: (arrayBuffer: ArrayBuffer, cropCoords: any) => {
    ipcRenderer.send("run-model", arrayBuffer, cropCoords);
  },
  runUploadImage: () => ipcRenderer.send("open-directory-dialog"),
  runUploadSketch: () => ipcRenderer.send("open-directory-sketch"),
  runImageSimilarity: (path_og: any, path_sketch: any) =>
    ipcRenderer.send("check-image-similarity", path_og, path_sketch),

  // Function to subscribe to the Python script response IPC message
  handlePythonScriptResponse: (callback: any) => {
    ipcRenderer.on("python-script-response", (event, ...args) =>
      callback(...args)
    );
  },
  handleModelResponse: (callback: any) => {
    ipcRenderer.on("model-response", (event, ...args) => callback(...args));
  },
  handleImageSetResponse: (callback: any) => {
    ipcRenderer.on("open-image-response", (event, ...args) =>
      callback(...args)
    );
  },
  handleSketchSetResponse: (callback: any) => {
    ipcRenderer.on("open-sketch-response", (event, ...args) =>
      callback(...args)
    );
  },
  handleSimilarityResponse: (callback: any) => {
    ipcRenderer.on("check-similarity-response", (event, ...args) =>
      callback(...args)
    );
  },
});
