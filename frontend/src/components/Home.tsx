import { useState, useEffect } from "react";

const Home = () => {
  const [output, setOutput] = useState("");

  const handleClick = () => {
    window.electronAPI.runPythonScript();

    window.electronAPI.handlePythonScriptResponse((message: any) => {
      setOutput(message);
    });
  };

  return (
    <>
      <div>Hello cool!</div>
      {output}
      <button onClick={handleClick}>asdf</button>
    </>
  );
};

export default Home;
