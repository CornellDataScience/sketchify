import { useState } from "react";
import Model from "./Model";
import ImageSimilarity from "./ImageSimilarity";

type NavItem = "MODEL" | "IMAGE SIMILARITY";

const Home = () => {
  const [nav, setNav] = useState<NavItem>("MODEL");
  return (
    <div>
      {/* Nav bar */}
      CURRENT TAB: {nav}
      <br />
      <button onClick={() => setNav("MODEL")}>Model</button>
      <button onClick={() => setNav("IMAGE SIMILARITY")}>
        Image Similarity
      </button>
      <hr />
      {nav === "MODEL" && <Model />}
      {nav === "IMAGE SIMILARITY" && <ImageSimilarity />}
    </div>
  );
};

export default Home;
