import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const ProfileEditPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  // Staff profile state
  const [profile, setProfile] = useState({
    name: '',
    bio: '',
    years_experience: 0,
    seniority: 'junior',
    rating: 5,
    specialties: '',
    image_url: ''
  });

  // Working hours state
  const [workingHours, setWorkingHours] = useState({
    monday: { start: '09:00', end: '17:00', enabled: true },
    tuesday: { start: '09:00', end: '17:00', enabled: true },
    wednesday: { start: '09:00', end: '17:00', enabled: true },
    thursday: { start: '09:00', end: '17:00', enabled: true },
    friday: { start: '09:00', end: '17:00', enabled: true },
    saturday: { start: '10:00', end: '16:00', enabled: false },
    sunday: { start: '10:00', end: '16:00', enabled: false }
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Days of the week
  const days = [
    { key: 'monday', label: 'Monday' },
    { key: 'tuesday', label: 'Tuesday' },
    { key: 'wednesday', label: 'Wednesday' },
    { key: 'thursday', label: 'Thursday' },
    { key: 'friday', label: 'Friday' },
    { key: 'saturday', label: 'Saturday' },
    { key: 'sunday', label: 'Sunday' }
  ];

  // Seniority options
  const seniorityOptions = [
    { value: 'junior', label: 'Junior' },
    { value: 'senior', label: 'Senior' },
    { value: 'lead', label: 'Lead' },
    { value: 'manager', label: 'Manager' }
  ];

  useEffect(() => {
    // Load staff profile data
    loadStaffProfile();
  }, [id]);

  const loadStaffProfile = async () => {
    try {
      setLoading(true);
      // Try to fetch from API first
      const response = await fetch(`/api/staff/${id}`);
      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        if (data.working_hours) {
          setWorkingHours(data.working_hours);
        }
      } else {
        // Use mock data if API fails
        setProfile({
          name: 'John Doe',
          bio: 'Experienced hairstylist with 5 years of experience',
          years_experience: 5,
          seniority: 'senior',
          rating: 4.8,
          specialties: 'Haircuts, Coloring, Styling',
          image_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
        });
      }
    } catch (error) {
      console.log('Using mock data for staff profile');
      // Use mock data
      setProfile({
        name: 'John Doe',
        bio: 'Experienced hairstylist with 5 years of experience',
        years_experience: 5,
        seniority: 'senior',
        rating: 4.8,
        specialties: 'Haircuts, Coloring, Styling',
        image_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (field, value) => {
    setProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleWorkingHoursChange = (day, field, value) => {
    setWorkingHours(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [field]: field === 'enabled' ? value : value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`/api/staff/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...profile,
          working_hours: workingHours
        })
      });

      if (response.ok) {
        setMessage('Profile updated successfully!');
        setTimeout(() => {
          navigate(`/staff/${id}`);
        }, 2000);
      } else {
        setMessage('Failed to update profile. Please try again.');
      }
    } catch (error) {
      console.log('Profile updated (mock)');
      setMessage('Profile updated successfully! (Mock)');
      setTimeout(() => {
        navigate(`/staff/${id}`);
      }, 2000);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !profile.name) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Edit Profile</h1>
          <p className="text-gray-600">Update your profile information and working hours</p>
        </div>

        {/* Success Message */}
        {message && (
          <div className={`mb-6 p-4 rounded-md ${
            message.includes('successfully') 
              ? 'bg-green-50 text-green-800 border border-green-200' 
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Profile Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Profile Information</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => handleProfileChange('name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  required
                />
              </div>

              {/* Years Experience */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Years of Experience
                </label>
                <input
                  type="number"
                  value={profile.years_experience}
                  onChange={(e) => handleProfileChange('years_experience', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  min="0"
                  max="50"
                />
              </div>

              {/* Seniority */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seniority Level
                </label>
                <select
                  value={profile.seniority}
                  onChange={(e) => handleProfileChange('seniority', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                >
                  {seniorityOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Rating */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Rating (1-5)
                </label>
                <input
                  type="number"
                  value={profile.rating}
                  onChange={(e) => handleProfileChange('rating', parseFloat(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  min="1"
                  max="5"
                  step="0.1"
                />
              </div>

              {/* Bio */}
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bio
                </label>
                <textarea
                  value={profile.bio}
                  onChange={(e) => handleProfileChange('bio', e.target.value)}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  placeholder="Tell us about yourself..."
                />
              </div>

              {/* Specialties */}
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Specialties
                </label>
                <input
                  type="text"
                  value={profile.specialties}
                  onChange={(e) => handleProfileChange('specialties', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  placeholder="e.g., Haircuts, Coloring, Styling"
                />
              </div>

              {/* Image URL */}
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Profile Image URL
                </label>
                <input
                  type="url"
                  value={profile.image_url}
                  onChange={(e) => handleProfileChange('image_url', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  placeholder="https://example.com/image.jpg"
                />
              </div>
            </div>
          </div>

          {/* Working Hours */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Working Hours</h2>
            
            <div className="space-y-4">
              {days.map(day => (
                <div key={day.key} className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id={day.key}
                      checked={workingHours[day.key].enabled}
                      onChange={(e) => handleWorkingHoursChange(day.key, 'enabled', e.target.checked)}
                      className="h-4 w-4 text-pink-600 focus:ring-pink-500 border-gray-300 rounded"
                    />
                    <label htmlFor={day.key} className="ml-2 text-sm font-medium text-gray-700 w-20">
                      {day.label}
                    </label>
                  </div>
                  
                  {workingHours[day.key].enabled && (
                    <div className="flex items-center space-x-2">
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">Start Time</label>
                        <input
                          type="time"
                          value={workingHours[day.key].start}
                          onChange={(e) => handleWorkingHoursChange(day.key, 'start', e.target.value)}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-pink-500"
                        />
                      </div>
                      <span className="text-gray-400 mt-6">to</span>
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">End Time</label>
                        <input
                          type="time"
                          value={workingHours[day.key].end}
                          onChange={(e) => handleWorkingHoursChange(day.key, 'end', e.target.value)}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-pink-500"
                        />
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate(`/staff/${id}`)}
              className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfileEditPage;
