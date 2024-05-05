import { useState } from "react";

const Carousel = ({
  picSrc1,
  picSrc2,
}: {
  picSrc1: string;
  picSrc2: string;
}) => {
  const [activeIndex, setActiveIndex] = useState(0); // State to track the active slide

  const handlePrev = () => {
    setActiveIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : 1));
  };

  const handleNext = () => {
    setActiveIndex((prevIndex) => (prevIndex < 1 ? prevIndex + 1 : 0));
  };

  const indicators = [0, 1]; // Update where current slide is position wise

  return (
    <div
      id="controls-carousel"
      className="relative w-full border border-gray-200 rounded-lg shadow-sm"
      data-carousel="static"
    >
      {/* Carousel wrapper */}
      <div className="relative h-56 overflow-hidden rounded-lg md:h-96">
        {/* Item 1 */}
        <div
          className={`duration-700 ease-in-out ${
            activeIndex === 0 ? "block" : "hidden"
          }`}
          data-carousel-item
        >
          <img
            src={picSrc1}
            className="absolute block w-full h-full object-cover rounded-lg top-0 left-0"
            alt="Original"
          />
        </div>
        {/* Item 2 */}
        <div
          className={`duration-700 ease-in-out ${
            activeIndex === 1 ? "block" : "hidden"
          }`}
          data-carousel-item
        >
          <img
            src={picSrc2}
            className="absolute block w-full h-full object-cover rounded-lg top-0 left-0"
            alt="Processed"
          />
        </div>
      </div>
      {/* Slider indicators */}
      <div className="absolute z-30 flex -translate-x-1/2 space-x-3 rtl:space-x-reverse bottom-5 left-1/2 transform">
        {indicators.map((index) => (
          <button
            key={index}
            type="button"
            className={`w-3 h-3 rounded-full ${
              activeIndex === index
                ? "bg-blue-500 ring-2 ring-white"
                : "bg-white border border-gray-400 ring-2 ring-gray-300"
            }`}
            aria-current={activeIndex === index ? "true" : "false"}
            aria-label={`Slide ${index + 1}`}
            onClick={() => setActiveIndex(index)}
          ></button>
        ))}
      </div>
      {/* Slider controls */}
      <button
        type="button"
        className="absolute top-0 start-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
        data-carousel-prev
        onClick={handlePrev}
      >
        <span className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-500 hover:bg-blue-600 focus:ring-4 focus:ring-blue-300 text-white shadow-md ring-2 ring-white group-focus:outline-none">
          <svg
            className="w-6 h-6"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 19l-7-7 7-7"
            />
          </svg>
          <span className="sr-only">Previous</span>
        </span>
      </button>
      <button
        type="button"
        className="absolute top-0 end-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
        data-carousel-next
        onClick={handleNext}
      >
        <span className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-blue-500 hover:bg-blue-600 focus:ring-4 focus:ring-blue-300 text-white shadow-md ring-2 ring-white group-focus:outline-none">
          <svg
            className="w-6 h-6"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="m9 5 7 7-7 7"
            />
          </svg>
          <span className="sr-only">Next</span>
        </span>
      </button>
    </div>
  );
};

export default Carousel;
