import React, { useState } from 'react';
import InfoField from '../components/InfoField';
import FileUpload from '../components/FileUpload';

const AgentCreationPage = () => {
  const [agent, setAgent] = useState({
    name: '',
    role: '',
    company: '',
    description: ''
  });

  const handleFileUpload = (file) => {
    console.log('File uploaded:', file);
    // Handle file upload logic here
  };

  const handleChange = (field, value) => {
    setAgent(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold text-rose-400 mb-6">Create New Agent</h2>
      <div className="bg-gray-800/50 rounded-lg p-6">
        <InfoField 
          label="Agent Name" 
          value={agent.name} 
          onChange={(value) => handleChange('name', value)} 
        />
        <InfoField 
          label="Agent Role" 
          value={agent.role} 
          onChange={(value) => handleChange('role', value)} 
        />
        <InfoField 
          label="Company" 
          value={agent.company} 
          onChange={(value) => handleChange('company', value)} 
        />
        <InfoField 
          label="Description" 
          value={agent.description} 
          onChange={(value) => handleChange('description', value)} 
        />
        
        <FileUpload 
          onFileUpload={handleFileUpload} 
          acceptedTypes=".csv,.pdf,.doc,.docx"
        />
        
        <button className="mt-6 bg-cyan-600 hover:bg-cyan-700 text-white py-2 px-6 rounded-md transition-colors">
          Create Agent
        </button>
      </div>
    </div>
  );
};

export default AgentCreationPage;