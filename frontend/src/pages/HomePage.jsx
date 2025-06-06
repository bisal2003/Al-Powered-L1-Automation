import React from 'react';

const HomePage = () => {
  return (
    <div className="min-h-screen">
      <h2 className="text-2xl font-semibold text-purple-400 mb-6">Dashboard</h2>
      <div className="grid grid-cols-1  gap-6">
        <div className="bg-gray-800/50 rounded-lg p-6">
          <h3 className="text-lg font-medium mb-4">Recent Activity</h3>
          <div className="space-y-4">
            <p className="text-gray-300">No recent activity</p>
          </div>
        </div>
        {/* <div className="bg-gray-800/50 rounded-lg p-6">
          <h3 className="text-lg font-medium mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-4">
            <button className="bg-cyan-600 hover:bg-cyan-700 text-white py-3 px-4 rounded-md transition-colors">
              CALLe
            </button>
            <button className="bg-purple-600 hover:bg-purple-700 text-white py-3 px-4 rounded-md transition-colors">
              CALLx
            </button>
          </div>
        </div> */}
      </div>
    </div>
  );
};

export default HomePage;