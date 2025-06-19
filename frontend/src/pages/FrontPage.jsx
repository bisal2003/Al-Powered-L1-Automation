import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

const FrontPage = () => {
  return (
    <div className="flex flex-col items-center  h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white overflow-hidden">
        <motion.h1 
        className="centerhead flex text-[30vh] font-bold font-square mt-[10vh]  relative"
        initial={{ opacity: 0, x: 500 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1 }}
      >
        CALL.E
      </motion.h1>
      <motion.h1 
        className="text-5xl font-bold mb-4 relative"
        initial={{ opacity: 0, x: -500 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1 }}
        whileHover={{ scale: 1.0, textShadow: "0px 0px 8px rgba(255,255,255,0.8)" }}
      >
        Welcome to Our Platform
      </motion.h1>
      <motion.p 
        className="text-lg text-gray-400 mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
      >
        Get started with the best tools and resources.
      </motion.p>
      <div className="flex space-x-4">
        <Link to="/call">
        <motion.button 
          className="px-8 py-3 bg-blue-600 rounded-lg transition shadow-lg hover:bg-blue-500 cursor-pointer"
          whileHover={{ boxShadow: "0px 0px 10px rgba(59,130,246,0.7)" }}
          whileTap={{ scale: 0.8 }}
          >
          Get Started
        </motion.button>
          </Link>
      </div>
      <motion.div 
        className="absolute w-40 h-40 bg-blue-500 rounded-full opacity-30 blur-xl top-10 left-10"
        animate={{ x: [0, 50, 0], y: [0, 50, 0] }}
        transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
      />
      <motion.div 
        className="absolute w-40 h-40 bg-purple-500 rounded-full opacity-30 blur-xl bottom-10 right-10"
        animate={{ x: [0, -50, 0], y: [0, -50, 0] }}
        transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
      />
    </div>
  );
};

export default FrontPage;