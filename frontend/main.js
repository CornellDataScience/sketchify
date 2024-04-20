// main.js

// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain, dialog} = require('electron')
const path = require('node:path')
const fs = require('fs');
const { spawn } = require('child_process');

let mainWindow = null;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')
  document.getElementById('check-similarity').disabled = true;

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

ipcMain.on('open-directory-dialog', (event) => {
  dialog.showOpenDialog(mainWindow, {
      properties: ['openFile']
  }).then(result => {
      console.log(result.filePaths);
      event.sender.send('selected-file-path', result.filePaths[0]);
  }).catch(err => {
      console.log(err);
  });
});

ipcMain.on('open-directory-sketch', (event) => {
  dialog.showOpenDialog(mainWindow, {
      properties: ['openFile']
  }).then(result => {
      console.log(result.filePaths);
      event.sender.send('selected-sketch-path', result.filePaths[0]);
  }).catch(err => {
      console.log(err);
  });
});

ipcMain.on('check-image-similarity',(event, imgPath, sketchPath) => {
    console.log(imgPath);
    console.log(sketchPath);

    scriptPath = path.join(__dirname, '../ml/main.py');

    const pythonProcess = spawn('python', [scriptPath, imgPath, sketchPath]);

    pythonProcess.stdout.on('data', (data) => {
        event.sender.send('similarity-results', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Child process exited with code ${code}`);
    });
});


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.