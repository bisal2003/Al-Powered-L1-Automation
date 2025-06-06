import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ProfilePage from './pages/ProfilePage';
import HomePage from './pages/HomePage';
import AgentCreationPage from './pages/AgentCreationPage';
import CallLogPage from './pages/CallLogPage';

const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <Router>
      <div className="min-h-screen min-w-screen  bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100 font-sans">
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <div className="flex">
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          <div className="flex-1 p-6">
            <Routes>
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/" element={<HomePage />} />
              <Route path="/create-agent" element={<AgentCreationPage />} />
              <Route path="/call-logs" element={<CallLogPage />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;