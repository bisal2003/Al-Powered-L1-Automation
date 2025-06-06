import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { name: 'Profile', path: '/profile' },
    { name: 'Home', path: '/' },
    { name: 'Create Agent', path: '/create-agent' },
    { name: 'Call Logs', path: '/call-logs' },
  ];

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
          onClick={onClose}
        ></div>
      )}
      
      <aside className={`fixed min-h-screen md:static inset-y-0 left-0 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 transition-transform duration-200 ease-in-out z-30 w-64 bg-gray-800 border-r border-gray-700 p-4`}>
        <nav className="mt-8">
          <ul className="space-y-2">
            {menuItems.map((item) => (
              <li key={item.path}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) => 
                    `block px-4 py-2 rounded-md ${isActive ? 'bg-gray-700 text-cyan-400' : 'text-gray-300 hover:bg-gray-700'}`
                  }
                  onClick={onClose}
                >
                  {item.name}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;