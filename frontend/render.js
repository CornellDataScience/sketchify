const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

var imgPath = "";
var sketchPath = "";

document.getElementById('upload-image').addEventListener('click', () => {
    ipcRenderer.send('open-directory-dialog');
});

ipcRenderer.on('selected-file-path', (event, path) => {
    //imgPath = path;
    document.getElementById('displayImage').src = path;
    imgPath = path;
});

document.getElementById('upload-sketch').addEventListener('click', () => {
    ipcRenderer.send('open-directory-sketch');
})

ipcRenderer.on('selected-sketch-path', (event, path) => {
    //sketchPath = path;
    document.getElementById('displaySketch').src = path;
    sketchPath = path;
});

ipcRenderer.on('similarity-results', (event, data) => {
    document.getElementById('similarity-score').textContent = data;
});

document.getElementById('check-similarity').addEventListener('click', () => {
    if (imgPath && sketchPath) {
        ipcRenderer.send('check-image-similarity', imgPath, sketchPath);
    }
});