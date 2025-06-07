import React from 'react';
import { CloudDownload } from 'lucide-react';

const CallLogItem = ({ call }) => {
  return (
    <div className="border-b border-gray-700 py-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">{call.agentName}</h3>
          <p className="text-gray-400 text-sm">{call.time}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${call.connected ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
          }`}>
          {call.connected ? 'Connected' : 'Failed'}
        </div>


      </div>
      <div className='flex flex-col mt-2'>
        <p className="mt-2 text-gray-300">{call.summary}</p>
        {call?.connected && (
          <div className='flex flex-row items-center gap-2.5 rounded'>
            <span>summary</span>
            <span className='relative top-1.5 cursor-pointer'><CloudDownload /></span>
          </div>
        )}
      </div>
      <div className="mt-3 flex space-x-2">
        {call.tools.map((tool, index) => (
          <span key={index} className="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">
            {tool}
          </span>
        ))}
      </div>
    </div>
  );
};

export default CallLogItem;