import { useState, useEffect, useRef } from "react";
import ReactCrop, {
  centerCrop,
  makeAspectCrop,
  Crop,
  PixelCrop,
  convertToPixelCrop,
} from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";

const Home = () => {
  const [image, setImage] = useState<string>("");
  // The current crop area
  const [crop, setCrop] = useState<Crop>();
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const [aspect, setAspect] = useState<number | undefined>(16 / 9);
  const [showProcessButton, setShowProcessButton] = useState(false);

  // const previewCanvasRef = useRef(null);
  const imgRef = useRef<HTMLImageElement>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;

    if (file) {
      // Create FileRedaer object to read selected file
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (e) => {
        const imageData = e.target.result as string;
        setImage(imageData);
      };
    }
  };

  const processCroppedImage = async () => {
    if (!completedCrop || !imgRef.current) {
      console.error("Required elements for processing are not present.");
      return;
    }

    // Extract the crop from the image and get it as a Blob
    const croppedImageData = await getCroppedImg(imgRef.current, completedCrop);

    // buffer is needed input to electron?
    const buffer = Buffer.from(await croppedImageData.arrayBuffer());

    const cropCoords = {
      tl: { x: completedCrop.x, y: completedCrop.y },
      br: {
        x: completedCrop.x + completedCrop.width,
        y: completedCrop.y + completedCrop.height,
      },
    };

    // Send buffer to main process
    window.electronAPI.runModel(buffer, cropCoords);

    // Listen for response from main process
    window.electronAPI.handleModelResponse((response: any) => {
      console.log("Python script response:", response);
    });
  };

  const getCroppedImg = (
    image: HTMLImageElement,
    crop: Crop
  ): Promise<Blob> => {
    const canvas = document.createElement("canvas");
    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;
    canvas.width = crop.width;
    canvas.height = crop.height;
    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      image,
      crop.x * scaleX,
      crop.y * scaleY,
      crop.width * scaleX,
      crop.height * scaleY,
      0,
      0,
      crop.width,
      crop.height
    );

    return new Promise((resolve, reject) => {
      canvas.toBlob((blob) => {
        if (!blob) {
          // Blob could not be created
          reject(new Error("Canvas is empty"));
          return;
        }
        resolve(blob);
      }, "image/jpeg");
    });
  };

  const [output, setOutput] = useState("");

  const handleClick = () => {
    window.electronAPI.runPythonScript();

    window.electronAPI.handlePythonScriptResponse((message: any) => {
      setOutput(message);
    });
  };

  return (
    <>
      {output}
      <input type="file" onChange={handleImageChange} />
      <br /> <br />
      {!!image && (
        <ReactCrop
          crop={crop}
          onChange={(_, percentCrop) => setCrop(percentCrop)}
          onComplete={(c) => {
            setCompletedCrop(c);
            setShowProcessButton(true);
          }}
          minHeight={100}
        >
          <img
            ref={imgRef}
            alt="Crop me"
            src={image}
            style={{ maxWidth: "100%", maxHeight: "300px" }}
            // onLoad={onImageLoad}
          />
        </ReactCrop>
      )}
      {!!completedCrop && showProcessButton && (
        <button onClick={processCroppedImage}>Run ML Model</button>
      )}
    </>
  );
};

export default Home;