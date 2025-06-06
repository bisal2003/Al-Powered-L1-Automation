import React from 'react';

const Header = ({ onMenuClick }) => {
  return (
    <header className="border-b  border-gray-700 p-4 flex justify-even items-center">
      <div className="flex items-center md:mx-10">
        <button 
          onClick={onMenuClick}
          className="md:hidden mr-4 text-gray-400 hover:text-white"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <h1 className="text-2xl font-bold text-cyan-400">Callex</h1>
      </div>
      <div className="flex-1 flex justify-around items-center">
        
            <button className=" md:w-36 hover:bg-cyan-700 text-white py-3 px-4 rounded-md bg-red-800">
              CALLe
            </button>
            <button className="bg-purple-600 md:w-36 hover:bg-purple-700 text-white py-3 px-4 rounded-md">
              CALLx
            </button>
  
      </div>
    </header>
  );
};

export default Header;