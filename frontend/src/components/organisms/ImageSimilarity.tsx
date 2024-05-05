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
  const [showLoadingButton, setShowLoadingButton] = useState(false);

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
      setShowLoadingButton(true);
      window.electronAPI.runImageSimilarity(ogImage, sketchImage);
    }

    window.electronAPI.handleSimilarityResponse((message: any) => {
      setShowLoadingButton(false);
      setSimilarityScore(message);
    });
  };

  return (
    <>
      <h1 className="text-3xl text-black-800 font-bold py-4">
        Image Similarity
      </h1>

      <div
        style={{
          display: "flex",
          gap: "14px",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {ogImage.bytes ? (
          <img
            src={`data:image/jpg;base64,${ogImage.bytes}`}
            alt={ogImage.path}
            className="w-80 h-60 relative overflow-hidden  border-dotted border-2 border-gray-300 cursor-pointer rounded-lg object-cover"
            onClick={uploadImage}
          />
        ) : (
          <button
            onClick={uploadImage}
            className="w-80 h-60 flex flex-col justify-center items-center relative overflow-hidden border-dotted border-2 border-gray-300 cursor-pointer rounded-lg"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-8 h-8 text-gray-500 mb-2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16s1-1 4-1 4 1 4 1 1-1 4-1 4 1 4 1V4H4v12zM4 8h16M4 12h16m-7-4v8m-4-8v8"
              />
            </svg>
            <h1 className="text-gray-500 text-lg">Upload Image</h1>
          </button>
        )}
        {sketchImage.bytes ? (
          <img
            src={`data:image/jpg;base64,${sketchImage.bytes}`}
            alt={sketchImage.path}
            className="w-80 h-60 relative overflow-hidden border-dotted border-2 border-gray-300 cursor-pointer rounded-lg object-cover"
            onClick={uploadSketch}
          />
        ) : (
          <button
            onClick={uploadSketch}
            className="w-80 h-60 flex flex-col justify-center items-center relative overflow-hidden border-dotted border-2 border-gray-300 cursor-pointer rounded-lg"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-8 h-8 text-gray-500 mb-2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16s1-1 4-1 4 1 4 1 1-1 4-1 4 1 4 1V4H4v12zM4 8h16M4 12h16m-7-4v8m-4-8v8"
              />
            </svg>
            <h1 className="text-gray-500 text-lg">Upload Sketch</h1>
          </button>
        )}
      </div>

      <div className="bg-blue-100 p-4 rounded-lg shadow-lg flex justify-between items-center mx-4 my-2 mt-4 gap-4">
        <h4 id="similarity-score">Similarity Score: {similarityScore}</h4>
        <div className="inline-flex items-center">
          <Button
            onClick={checkSimilarity}
            disabled={ogImage.path == "" || sketchImage.path == ""}
            isLoading={showLoadingButton}
            id="check-similarity"
            // className="checkSimilarity"
          >
            Check Similarity
          </Button>
        </div>
      </div>
      {output}
      {/* <Button onClick={handleClick}>asdf</Button> */}
    </>
  );
};

export default Home;
