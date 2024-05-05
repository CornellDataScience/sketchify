# sketchify

Turning images into coloring book pages with infinite resolution.

The following features are supported:

1. Users can upload a full color image and select a bounding box of the area they would like to draw. The application converts the selected area into a vector sketch with infinite resolution.
2. Users can upload a full color image and a sketch that they drew themselves. The applicaiton converts the full color image to a sketch and then compares the similarity between the generated sketch and the user-submitted sketch. A similarity score is returned as a float value.

## Download

Binaries are available in the Releases section.

## Getting started

To get started with the project, do the following steps:

1. Clone the repository
2. Run `make init` to download Meta's Segment Anything model and create a Python venv with all required dependencies.
3. Run `make build` to start the full build pipeline. This runs Pyinstaller on the ML model and then runs Electron Forge to create the final packaged application. The only currently supported format is a `zip` file, but other formats are supported by Electron Forge.

### Architecture

The frontend is an Electron application built with the latest web technologies, including React, TypeScript, and Tailwind CSS. A context bridge is used so that the renderer can send calls to the Node.js backend which has access to system processes.

The backend is a full ML pipeline that takes in a full color image and outputs a sketch in vector format. The pipeline is outlined below:

1. Image segmentation, using Meta's Segment Anything model.
2. Edge detection, using Canny edge detection and TEED.
3. Edge smoothing, using OpenCV functions.
4. SVG conversion, using VTracer.

Pyinstaller is used to compile the Python scripts into binary executables. These binaries are then copied over to the `resources` folder of the Electron app during the build process of Electron Forge.

### Team (SP24)

- Leads
  - Jason Zheng (Technical Lead)
  - Laura Gong (Project Manager)
- Developers
  - Darren Key
  - Cody Torvognik
  - Peter Ha
  - Samantha Vaca
  - Alice Um
  - Temi Adebowale
  - Kayla Shan
  - Tamara Kasikovic
