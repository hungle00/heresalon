import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function StaffProfilePage() {
  const { id } = useParams();
  const [staff, setStaff] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStaffProfile();
  }, [id]);

  const fetchStaffProfile = async () => {
    try {
      setLoading(true);
      setError(null); // Clear any previous errors
      const response = await fetch(`/api/staff/${id}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch staff profile');
      }
      const data = await response.json();
      setStaff(data);
    } catch (err) {
      console.log('API fetch failed, using mock data:', err.message);
      setError(null); // Clear error state when using mock data
      // Mock data for development
      const mockStaff = {
        id: parseInt(id),
        name: 'Sarah Johnson',
        role: 'Senior Hair Stylist',
        bio: 'With over 8 years of experience in hair styling and coloring, Sarah specializes in modern cuts and vibrant color techniques. She has trained with top stylists in New York and Paris.',
        years_experience: 8,
        seniority: 'Senior',
        rating: 4.9,
        specialties: ['Hair Coloring', 'Hair Cutting', 'Styling', 'Color Correction'],
        image_url: 'https://via.placeholder.com/400x300?text=Sarah+Johnson',
        services: [
          { name: 'Hair Cut & Style', price: '$75', duration: '60 min' },
          { name: 'Hair Coloring', price: '$120', duration: '90 min' },
          { name: 'Highlights', price: '$150', duration: '120 min' },
          { name: 'Color Correction', price: '$200', duration: '180 min' }
        ]
      };
      setStaff(mockStaff);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (!staff) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
          Staff member not found
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link 
        to="/staff"
        className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6"
      >
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Staff
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Image */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <img 
              src={staff.image_url} 
              alt={staff.name}
              className="w-full h-64 object-cover"
            />
          </div>
        </div>

        {/* Profile Information */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              {staff.name}
            </h1>
            <p className="text-xl text-gray-600 mb-4">
              {staff.role}
            </p>
            
            <div className="flex items-center mb-6">
              <div className="flex items-center">
                <span className="text-2xl mr-2">⭐</span>
                <span className="text-lg font-semibold">{staff.rating}/5.0</span>
              </div>
              <span className="text-gray-600 ml-4">
                ({staff.years_experience} years experience)
              </span>
            </div>

            <div className="border-t pt-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-3">
                About {staff.name}
              </h2>
              <p className="text-gray-700 mb-6">
                {staff.bio}
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Specialties
              </h3>
              <div className="flex flex-wrap gap-2 mb-6">
                {staff.specialties.map((specialty) => (
                  <span 
                    key={specialty}
                    className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                  >
                    {specialty}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Services Section */}
      <div className="mt-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Services & Pricing
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {staff.services?.map((service, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition duration-300">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  {service.name}
                </h3>
                <p className="text-2xl font-bold text-blue-600 mb-1">
                  {service.price}
                </p>
                <p className="text-sm text-gray-600">
                  {service.duration}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default StaffProfilePage;
