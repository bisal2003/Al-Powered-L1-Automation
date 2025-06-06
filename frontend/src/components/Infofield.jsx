import React from 'react';

const InfoField = ({ label, value = '', onChange }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm text-gray-400 uppercase tracking-wider mb-1">
        {label}
      </label>
      {onChange ? (
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full bg-gray-700 border-b rounded-sm border-gray-600 py-2 px-1 text-white focus:outline-none focus:border-cyan-400"
        />
      ) : (
        <div className="w-full bg-gray-700 border-b rounded-sm border-gray-600 py-2 px-1 text-white">
          {value || '\u00A0'}
        </div>
      )}
    </div>
  );
};

export default InfoField;