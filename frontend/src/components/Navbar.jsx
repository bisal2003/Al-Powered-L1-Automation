import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";

const Navbar = () => {

    const [isActive, setIsActive] = useState("Home");

  // Common gradient styles for all NavLinks
  const baseGradientStyle = {
    background: "linear-gradient(to right, #111827 50%, #374151 50%)",
    backgroundSize: "200% 100%",       // Make the gradient 2x the width
    transition: "background-position 0.5s ease-out",
  };

  // Function to decide background position based on which link is active
  const getBackgroundPosition = (linkName) => {
    return isActive === linkName ? "0% 0%" : "100% 0";
  };

  // Handlers for hover to move background from right to left
  const handleMouseEnter = (e) => {
    e.currentTarget.style.backgroundPosition = "0% 0%";
  };
  const handleMouseLeave = (e, linkName) => {
    // If link is not active, reset background to the right
    if (isActive !== linkName) {
      e.currentTarget.style.backgroundPosition = "100% 0";
    }
  };

  return (
    <nav className="absolute top-[16px] right-10 w-[90%] flex font-bold uppercase justify-end bg-[#374151] py-2 rounded-full px-8 space-x-6 text-lg z-10">
    <NavLink
      to="/call"
      onClick={() => setIsActive("Home")}
      style={{
        ...baseGradientStyle,
        backgroundPosition: getBackgroundPosition("Home"),
      }}
      className="rounded-4xl px-4 py-1 text-center"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={(e) => handleMouseLeave(e, "Home")}
    >
      Home
    </NavLink>


    <NavLink
      to="/Dashboard"
      onClick={() => setIsActive("Dashboard")}
      style={{
        ...baseGradientStyle,
        backgroundPosition: getBackgroundPosition("Dashboard"),
      }}
      className="rounded-4xl px-4 py-1 text-center"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={(e) => handleMouseLeave(e, "Dashboard")}
    >
      Dashboard
    </NavLink>
  </nav>
  )
}

export default Navbar