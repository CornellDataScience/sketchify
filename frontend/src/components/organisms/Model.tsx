import { useState, useEffect, useRef } from "react";
import ReactCrop, {
  centerCrop,
  makeAspectCrop,
  Crop,
  PixelCrop,
  convertToPixelCrop,
} from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";
import FileInput from "../atoms/FileInput";
import Button from "../atoms/Button";
import DropZone from "../atoms/DropZone";
import React, {useCallback} from 'react'
import {useDropzone} from 'react-dropzone'

const Model = () => {
  const [image, setImage] = useState<string>("");
  const [imageArrayBuffer, setImageArrayBuffer] = useState(null);
  const [outputImage, setOutputImage] = useState<{
    bytes: string;
    path: string;
  }>({
    bytes: "",
    path: "",
  });
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
      // Create FileRedaer object to read selected file as ArrayBuffer
      const readerArrayBuffer = new FileReader();
      readerArrayBuffer.readAsArrayBuffer(file);
      readerArrayBuffer.onload = (e) => {
        const buf = e.target.result;
        setImageArrayBuffer(buf);
      };

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

    const cropCoords = {
      tl: { x: completedCrop.x, y: completedCrop.y },
      br: {
        x: completedCrop.x + completedCrop.width,
        y: completedCrop.y + completedCrop.height,
      },
    };

    // Send buffer to main process

    const croppedImageData = await getCroppedImg(imgRef.current, completedCrop);

    // Convert the blob to a buffer to save as a file (this part is specific to Electron)

    getCroppedImg(imgRef.current, completedCrop)
      .then((blob) => {
        // Convert blob to ArrayBuffer
        const reader = new FileReader();
        reader.onloadend = () => {
          const arrayBuffer = reader.result;
          const cropCoords = {
            tl: { x: completedCrop.x, y: completedCrop.y },
            br: {
              x: completedCrop.x + completedCrop.width,
              y: completedCrop.y + completedCrop.height,
            },
          };

          // Send ArrayBuffer and crop coordinates to the main process

          // Use imageArrayBuffer instead of arrayBuffer so that we send in
          // the bytes of the original image, not the smaller cropped image
          // from Electron
          //
          // Use cropCordsOriginal instead of cropCoords because cropCoords
          // are only for the coords of the smaller image. We want the (tl, br)
          // coords of the original (much larger) image, so we need to scale
          // tl and br accordingly
          const originalImage = imgRef.current;
          const cropCoordsOriginal = {
            tl: {
              x:
                (cropCoords.tl.x / originalImage.width) *
                originalImage.naturalWidth,
              y:
                (cropCoords.tl.y / originalImage.height) *
                originalImage.naturalHeight,
            },
            br: {
              x:
                (cropCoords.br.x / originalImage.width) *
                originalImage.naturalWidth,
              y:
                (cropCoords.br.y / originalImage.height) *
                originalImage.naturalHeight,
            },
          };
          window.electronAPI.runModel(imageArrayBuffer, cropCoordsOriginal);
        };
        reader.readAsArrayBuffer(blob);
      })
      .catch((error) =>
        console.error("Failed to process the cropped image", error)
      );

    // // Listen for response from main process
    window.electronAPI.handleModelResponse((message: any) => {
      setOutputImage(message);
      // console.log("Python script response:", response);
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
      {/* <input type="file" onChange={handleImageChange} /> */}
      <DropZone onChange={handleImageChange} />
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
        <Button onClick={processCroppedImage}>Run ML Model</Button>
      )}
      <div>Output below</div>
      {outputImage.bytes && (
        <div>
          <img
            src={`data:image/svg+xml;base64,${outputImage.bytes}`}
            alt="Image is not available"
            width="100%"
          />
        </div>
      )}
      {/* <Button onClick={() => console.log(outputImage.bytes)}>asdf</Button> */}
    </>
  );
};

export default Model;
