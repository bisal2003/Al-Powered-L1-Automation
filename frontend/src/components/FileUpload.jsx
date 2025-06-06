import React, { useCallback } from 'react';

const FileUpload = ({ onFileUpload, acceptedTypes = '.csv,.pdf' }) => {
  const handleFileChange = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  }, [onFileUpload]);

  return (
    <div className="mt-4">
      <label className="block text-sm text-gray-400 uppercase tracking-wider mb-2">
        Upload File
      </label>
      <div className="flex items-center">
        <label className="cursor-pointer bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors">
          Choose File
          <input 
            type="file" 
            className="hidden" 
            accept={acceptedTypes}
            onChange={handleFileChange}
          />
        </label>
        <span className="ml-4 text-gray-300 text-sm">Accepted: {acceptedTypes}</span>
      </div>
    </div>
  );
};

export default FileUpload;