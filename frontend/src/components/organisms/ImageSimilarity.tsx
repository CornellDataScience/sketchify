import { useState, useEffect } from "react";
import Button from "../atoms/Button";

const Home: React.FC = () => {
  const [output, setOutput] = useState("");
  const [ogImage, setOgImage] = useState<{ bytes: string; path: string }>({
    bytes: "",
    path: "",
  });
  const [sketchImage, setSketchImage] = useState<{
    bytes: string;
    path: string;
  }>({ bytes: "", path: "" });
  const [similarityScore, setSimilarityScore] = useState("");

  const handleClick = () => {
    window.electronAPI.runPythonScript();

    window.electronAPI.handlePythonScriptResponse((message: any) => {
      setOutput(message);
    });
  };

  const uploadImage = () => {
    window.electronAPI.runUploadImage();

    window.electronAPI.handleImageSetResponse((message: any) => {
      setOgImage(message);
    });
  };

  const uploadSketch = () => {
    window.electronAPI.runUploadSketch();

    window.electronAPI.handleSketchSetResponse((message: any) => {
      setSketchImage(message);
    });
  };

  const checkSimilarity = () => {
    if (ogImage && sketchImage) {
      window.electronAPI.runImageSimilarity(ogImage, sketchImage);
    }

    window.electronAPI.handleSimilarityResponse((message: any) => {
      setSimilarityScore(message);
    });
  };

  return (
    <>
      <Button onClick={uploadImage} id="upload-image">
        Upload Image
      </Button>
      <Button onClick={uploadSketch} id="upload-sketch">
        Upload Sketch
      </Button>
      <Button
        onClick={checkSimilarity}
        disabled={ogImage.path == "" || sketchImage.path == ""}
        id="check-similarity"
        // className="checkSimilarity"
      >
        Check Similarity
      </Button>

      <h4 id="similarity-score">Similarity Score: {similarityScore}</h4>

      <img src={`data:image/jpg;base64,${ogImage.bytes}`} alt={ogImage.path} />
      <img
        src={`data:image/jpg;base64,${sketchImage.bytes}`}
        alt={sketchImage.path}
      />
      {output}
      {/* <Button onClick={handleClick}>asdf</Button> */}
    </>
  );
};

export default Home;
