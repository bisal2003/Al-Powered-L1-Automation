import React from 'react';
import CallLogItem from '../components/CallLogItem';

const CallLogPage = () => {
  const callLogs = [
    {
      id: 1,
      agentName: 'John Doe',
      time: '2023-05-15 14:30',
      connected: true,
      summary: 'Discussed product features and pricing. Client interested in demo.',
      tools: ['CRM', 'Notes']
    },
    {
      id: 2,
      agentName: 'Jane Smith',
      time: '2023-05-15 11:15',
      connected: false,
      summary: 'Call failed to connect. Left voicemail.',
      tools: ['Voicemail']
    },
    {
      id: 3,
      agentName: 'Mike Johnson',
      time: '2023-05-14 16:45',
      connected: true,
      summary: 'Technical support call. Resolved issue with account access.',
      tools: ['Support Ticket', 'Knowledge Base']
    }
  ];

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold text-green-400 mb-6">Call Logs</h2>
      <div className="bg-gray-800/50 rounded-lg p-6">
        <div className="mb-6 flex justify-between items-center">
          <div className="relative w-64">
            <input
              type="text"
              placeholder="Search calls..."
              className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-4 text-white focus:outline-none focus:border-cyan-400"
            />
            <svg className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <select className="bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white focus:outline-none focus:border-cyan-400">
            <option>All Status</option>
            <option>Connected</option>
            <option>Failed</option>
          </select>
        </div>
        
        <div className="space-y-4">
          {callLogs.map(call => (
            <CallLogItem key={call.id} call={call} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default CallLogPage;