import React from 'react';
import InfoField from '../components/InfoField';

const ProfilePage = () => {
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold text-amber-300 mb-6">Profile</h2>
      <div className="bg-gray-800/50 rounded-lg p-6">
        <InfoField label="Name" value=" John Doe" />
        <InfoField label="Origin" value=" New York" />
        <InfoField label="Team" value=" Sales" />
        
        <InfoField label="Email" value=" john.doe@example.com" />
        <InfoField label="Phone" value=" +1 (555) 123-4567" />
      </div>
    </div>
  );
};

export default ProfilePage;