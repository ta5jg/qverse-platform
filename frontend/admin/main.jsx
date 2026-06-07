import React from "react";
import { createRoot } from "react-dom/client";
import ForgeAdmin from "./pages/ForgeAdmin.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ForgeAdmin />
  </React.StrictMode>
);
