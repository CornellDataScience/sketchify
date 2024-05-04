import { useState } from "react";
import Model from "./Model";
import ImageSimilarity from "./ImageSimilarity";
import Welcome from "./Welcome";
import Button from "../atoms/Button";

type NavItem = "WELCOME" | "MODEL" | "IMAGE SIMILARITY";

const Home = () => {
  const [nav, setNav] = useState<NavItem>("WELCOME");
  return (
    <div>
      {/* Nav bar */}
      CURRENT TAB: {nav}
      <br />
      <Button disabled={nav === "WELCOME"} onClick={() => setNav("WELCOME")}>
        Welcome
      </Button>
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
      {nav === "WELCOME" && <Welcome />}
      {nav === "MODEL" && <Model />}
      {nav === "IMAGE SIMILARITY" && <ImageSimilarity />}
    </div>
  );
};

export default Home;
