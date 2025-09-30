import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { mockStaff } from '../data/mockData';

function StaffProfilePage() {
  const { id } = useParams();
  const [staff, setStaff] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStaff();
  }, [id]);

  const fetchStaff = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/staff/${id}/`);
      if (response.ok) {
        const staffData = await response.json();
        setStaff(staffData);
      } else {
        throw new Error('Staff not found');
      }
    } catch (err) {
      console.log('API fetch failed, using mock data:', err.message);
      // Use mock data as fallback
      const mockStaffMember = mockStaff.find(s => s.id === parseInt(id));
      if (mockStaffMember) {
        setStaff(mockStaffMember);
      } else {
        setError('Staff not found');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600"></div>
        </div>
      </div>
    );
  }

  if (error || !staff) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Staff Not Found</h1>
          <p className="text-gray-600 mb-8">The staff member you're looking for doesn't exist.</p>
          <Link
            to="/salon"
            className="bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 transition duration-300"
          >
            Back to Salon
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button and Action Buttons - Mobile Optimized */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <Link 
          to="/salon"
          className="inline-flex items-center text-pink-600 hover:text-pink-800 text-sm sm:text-base"
        >
          <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Staff
        </Link>
        
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 w-full sm:w-auto">
          <Link
            to={`/booking?staff_id=${id}`}
            className="inline-flex items-center justify-center px-3 py-2 sm:px-4 sm:py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 text-sm sm:text-base"
          >
            <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Book Now
          </Link>
          
          <Link
            to={`/staff/${id}/edit`}
            className="inline-flex items-center justify-center px-3 py-2 sm:px-4 sm:py-2 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 text-sm sm:text-base"
          >
            <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit Profile
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Image */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <img 
              src={staff.image_url} 
              alt={staff.name}
              className="w-full h-64 sm:h-80 object-cover"
            />
            <div className="p-6">
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-2">
                {staff.name}
              </h1>
              <p className="text-lg text-gray-600 mb-4">
                {staff.role}
              </p>
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  <span className="text-yellow-400 text-lg mr-1">⭐</span>
                  <span className="font-semibold">{staff.rating}</span>
                </div>
                <span className="text-gray-500 ml-2">
                  ({staff.years_experience} years experience)
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Details */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-6">About</h2>
            <p className="text-gray-600 leading-relaxed mb-6">
              {staff.bio}
            </p>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Specialties</h3>
              <div className="flex flex-wrap gap-2">
                {staff.specialties?.map((specialty, index) => (
                  <span 
                    key={index}
                    className="bg-pink-100 text-pink-800 px-3 py-1 rounded-full text-sm"
                  >
                    {specialty}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Experience</h3>
                <p className="text-gray-600">{staff.years_experience} years</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Rating</h3>
                <div className="flex items-center">
                  <span className="text-yellow-400 text-lg mr-1">⭐</span>
                  <span className="font-semibold">{staff.rating}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StaffProfilePage;
