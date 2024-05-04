import { useState } from "react";
import Model from "./Model";
import ImageSimilarity from "./ImageSimilarity";
import Button from "../atoms/Button";

type NavItem = "MODEL" | "IMAGE SIMILARITY";

const Home = () => {
  const [nav, setNav] = useState<NavItem>("MODEL");
  return (
    <div>
      {/* Nav bar */}
      CURRENT TAB: {nav}
      <br />
      <Button disabled={nav === "MODEL"} onClick={() => setNav("MODEL")}>
        Model
      </Button>
      <Button
        disabled={nav === "IMAGE SIMILARITY"}
        onClick={() => setNav("IMAGE SIMILARITY")}
      >
        Image Similarity
      </Button>
      <hr />
      {nav === "MODEL" && <Model />}
      {nav === "IMAGE SIMILARITY" && <ImageSimilarity />}
    </div>
  );
};

export default Home;
