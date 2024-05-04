import { useState } from "react";
import Model from "./Model";
import ImageSimilarity from "./ImageSimilarity";
import Button from "../atoms/Button";

type NavItem = "MODEL" | "IMAGE SIMILARITY";

const Home = () => {
  const [nav, setNav] = useState<NavItem>("MODEL");
  const toggleNav = (item: NavItem) => {
    setNav(item);
  };
  return (
    <div>
      {/* Nav bar */}
      <div>
        {/* Sidebar */}
        <aside className="bg-gray-100 dark:bg-gray-900 w-64 h-full fixed top-0 left-0 z-50">
          <div className="px-5 py-3 border-b border-gray-200 dark:border-gray-800">
            <h1 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
              NOT Sketchy
            </h1>
          </div>
          <nav className="flex flex-col mt-5">
            <button
              className={`flex items-center px-4 py-2 text-sm font-medium transition-colors duration-200 focus:outline-none ${
                nav === "MODEL"
                  ? "bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-gray-300"
                  : "text-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800"
              }`}
              onClick={() => toggleNav("MODEL")}
            >
              <svg
                className="w-5 h-5 me-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 18.5A2.493 2.493 0 0 1 7.51 20H7.5a2.468 2.468 0 0 1-2.4-3.154 2.98 2.98 0 0 1-.85-5.274 2.468 2.468 0 0 1 .92-3.182 2.477 2.477 0 0 1 1.876-3.344 2.5 2.5 0 0 1 3.41-1.856A2.5 2.5 0 0 1 12 5.5m0 13v-13m0 13a2.493 2.493 0 0 0 4.49 1.5h.01a2.468 2.468 0 0 0 2.403-3.154 2.98 2.98 0 0 0 .847-5.274 2.468 2.468 0 0 0-.921-3.182 2.477 2.477 0 0 0-1.875-3.344A2.5 2.5 0 0 0 14.5 3 2.5 2.5 0 0 0 12 5.5m-8 5a2.5 2.5 0 0 1 3.48-2.3m-.28 8.551a3 3 0 0 1-2.953-5.185M20 10.5a2.5 2.5 0 0 0-3.481-2.3m.28 8.551a3 3 0 0 0 2.954-5.185"
                ></path>
              </svg>
              Model
            </button>
            <button
              className={`flex items-center px-4 py-2 text-sm font-medium transition-colors duration-200 focus:outline-none ${
                nav === "IMAGE SIMILARITY"
                  ? "bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-gray-300"
                  : "text-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800"
              }`}
              onClick={() => toggleNav("IMAGE SIMILARITY")}
            >
              <svg
                className="w-5 h-5 me-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                ></path>
              </svg>
              Image Similarity
            </button>
          </nav>
        </aside>

        {/* Main content */}
        <main className="p-8 ml-64">
          {nav === "MODEL" && <Model />}
          {nav === "IMAGE SIMILARITY" && <ImageSimilarity />}
        </main>
      </div>
    </div>
  );
};

export default Home;
