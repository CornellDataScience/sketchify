document.addEventListener('DOMContentLoaded', () => {
  const runPythonBtn = document.getElementById('run-python');
  const outputArea = document.getElementById('output');

  runPythonBtn.addEventListener('click', () => {
      window.electronAPI.runPythonScript();
  });

  window.electronAPI.handlePythonScriptResponse((message) => {
      outputArea.textContent = message;
  });
});