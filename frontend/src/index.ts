import { app, BrowserWindow, ipcMain, dialog } from "electron";
import { exec } from "child_process";
import fs from "fs";
import isDev from "electron-is-dev";
import path from "path";

// const path = require("node:path");
// const { spawn } = require("child_process");

// This allows TypeScript to pick up the magic constants that's auto-generated by Forge's Webpack
// plugin that tells the Electron app where to look for the Webpack-bundled app code (depending on
// whether you're running in development or production).
declare const MAIN_WINDOW_WEBPACK_ENTRY: string;
declare const MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY: string;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require("electron-squirrel-startup")) {
  app.quit();
}

let mainWindow: any;

const createWindow = (): void => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    height: 600,
    width: 800,
    webPreferences: {
      preload: MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY,
    },
    autoHideMenuBar: true,
  });

  // and load the index.html of the app.
  mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);

  // Open the DevTools.
  //mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

/**
 * In production mode, this returns process.resourcesPath/python because we want
 * all of our Python files to be stored inside the `python` directory in `resources`.
 *
 * In dev mode, this returns ./python because we assume that all of our python
 * files are just stored in the root directory in a `python` folder.
 */
const getPythonFilesPath = () => {
  if (isDev) {
    console.log("Running in development");
    return "../ml/dist/main/main";
  } else {
    console.log("Running in production");
    return `${process.resourcesPath}/main/main`;
  }
};

ipcMain.on("run-python-script", (event) => {
  // Use the resources path since we want to store all of our Python files there.
  // If you want to access the app.asar in resources, use app.getAppPath()
  const pythonFilePath = getPythonFilesPath();
  exec(`cd ${pythonFilePath} && python -m cool`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      event.reply("python-script-response", `Error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      event.reply("python-script-response", `Error: ${stderr}`);
      return;
    }
    event.reply("python-script-response", stdout);
  });
});

ipcMain.on("run-model", async (event, arrayBuffer, cropCoords) => {
  // Create a temporary file path
  const tempImagePath = path.join(
    app.getPath("temp"),
    "temp_cropped_image.jpg"
  );

  console.log("Received arrayBuffer:", arrayBuffer);
  const imageBuffer = Buffer.from(arrayBuffer);
  console.log("Converted arrayBuffer to imageBuffer:", imageBuffer);

  fs.writeFileSync(tempImagePath, imageBuffer);
  const { tl, br } = cropCoords;

  const pythonFilePath = getPythonFilesPath();

  // const command = `python ${pythonFilePath}/cool.py "${tempImagePath}" ${tl.x} ${tl.y} ${br.x} ${br.y}`;
  // const pythonScriptPath = path.join(
  //   __dirname,
  //   "..",
  //   "..",
  //   "..",
  //   "ml",
  //   "model.py"
  // );

  const command = `${pythonFilePath} model ${tempImagePath} ${tl.x} ${tl.y} ${br.x} ${br.y}`;
  console.log(command);

  exec(command, (error, stdout, stderr) => {
    // error handling
    if (error) {
      console.error(`exec error: ${error}`);
      event.reply("model-response", `Error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      event.reply("model-response", `Error: ${stderr}`);
      return;
    }
    console.log(stdout);
    // Send the result back to the renderer process
    // const outputImagePath = stdout;
    // const base64 = fs.readFileSync(outputImagePath).toString("base64");
    const base64 = stdout;
    event.reply("model-response", { bytes: base64, path: "" });
  });
});

ipcMain.on("open-directory-dialog", (event) => {
  dialog
    .showOpenDialog(mainWindow, {
      properties: ["openFile"],
    })
    .then((result) => {
      // console.log(result.filePaths);
      const imgPath = result.filePaths[0];
      const base64 = fs.readFileSync(imgPath).toString("base64");
      event.reply("open-image-response", { bytes: base64, path: imgPath });
      //event.sender.send('selected-file-path', result.filePaths[0]);
    })
    .catch((err) => {
      console.log(err);
    });
});

ipcMain.on("open-directory-sketch", (event) => {
  dialog
    .showOpenDialog(mainWindow, {
      properties: ["openFile"],
    })
    .then((result) => {
      // console.log(result.filePaths);
      const imgPath = result.filePaths[0];
      const base64 = fs.readFileSync(imgPath).toString("base64");
      event.reply("open-sketch-response", { bytes: base64, path: imgPath });
      //event.sender.send('selected-sketch-path', result.filePaths[0]);
    })
    .catch((err) => {
      console.log(err);
    });
});

ipcMain.on("check-image-similarity", (event, imgPath, sketchPath) => {
  console.log(imgPath);
  console.log(sketchPath);

  const pythonFilePath = getPythonFilesPath();
  exec(
    `${pythonFilePath} similarity ${imgPath.path} ${sketchPath.path}`,
    (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        event.reply("python-script-response", `Error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`stderr: ${stderr}`);
        event.reply("python-script-response", `Error: ${stderr}`);
        return;
      }
      event.reply("check-similarity-response", stdout);
    }
  );

  /*
    var scriptPath = path.join(__dirname, '../ml/main.py');

    const pythonProcess = spawn('python', [scriptPath, imgPath, sketchPath]);

    pythonProcess.stdout.on('data', (data: any) => {
        event.reply("check-similarity-response", data.toString());
        //event.sender.send('similarity-results', data.toString());
    });

    pythonProcess.stderr.on('data', (data: any) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code: any) => {
        console.log(`Child process exited with code ${code}`);
    });
    */
});
