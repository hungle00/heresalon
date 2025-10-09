import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { mockStaff, mockServices } from '../data/mockData';

function SalonPage() {
  const [staff, setStaff] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch staff data
      const staffResponse = await fetch('/api/salons/1/staffs');
      if (!staffResponse.ok) {
        throw new Error('Failed to fetch staff');
      }
      const staffData = await staffResponse.json();
      setStaff(staffData);

      // Fetch services data
      const servicesResponse = await fetch('/api/salons/1/services');
      if (!servicesResponse.ok) {
        throw new Error('Failed to fetch services');
      }
      const servicesData = await servicesResponse.json();
      setServices(servicesData);

    } catch (err) {
      console.log('API fetch failed, using mock data:', err.message);
      setError(null);
      
      // Use mock data from separate file
      setStaff(mockStaff);
      setServices(mockServices);
    } finally {
      setLoading(false);
    }
  };

  const getServiceTypeLabel = (type) => {
    const typeLabels = {
      'Hair': 'Hair',
      'Nails': 'Nails',
      'Skin': 'Skin Care',
      'Massage': 'Massage'
    };
    return typeLabels[type] || type;
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

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
      {/* Hero Section with Visual Image */}
      <div className="mb-8 sm:mb-16">
        <div className="relative h-64 sm:h-80 lg:h-96 rounded-lg overflow-hidden">
          <img 
            src="https://images.unsplash.com/photo-1560066984-138dadb4c035?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2074&q=80"
            alt="Salon Interior"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <div className="text-center text-white px-4">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
                Here Salon
              </h1>
              <p className="text-lg sm:text-xl mb-6">
                Professional Beauty & Wellness Services
              </p>
              <Link
                to="/booking"
                className="bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 transition duration-300 text-sm sm:text-base"
              >
                Book Appointment
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Services Section - Updated Layout */}
      <div className="mb-12 sm:mb-16">
        <div className="text-center mb-8 sm:mb-12">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-800 mb-2 sm:mb-4">
            Our Services
          </h2>
          <p className="text-base sm:text-lg text-gray-600 px-4">
            Professional beauty and wellness services
          </p>
        </div>
        
        {/* Updated Grid: 2 columns on mobile, 4 columns on desktop */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
          {services.map((service) => (
            <Link 
              key={service.id} 
              to={`/service/${service.id}`}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300 group"
            >
              <img 
                src={service.image_url} 
                alt={service.name}
                className="w-full h-32 sm:h-40 object-cover group-hover:scale-105 transition duration-300"
              />
              <div className="p-3 sm:p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-sm sm:text-base font-semibold text-gray-800 line-clamp-2">
                    {service.name}
                  </h3>
                  <span className="bg-pink-100 text-pink-800 text-xs px-2 py-1 rounded-full ml-2 flex-shrink-0">
                    {getServiceTypeLabel(service.type)}
                  </span>
                </div>
                {/* Removed price and booking button - now just clickable card */}
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Hair Stylists Section - Updated Layout */}
      <div>
        <div className="text-center mb-8 sm:mb-12">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-800 mb-2 sm:mb-4">
            Our Hair Stylists
          </h2>
          <p className="text-base sm:text-lg text-gray-600 px-4">
            Meet our talented hair stylists
          </p>
        </div>
        
        {/* Updated Grid: 2 columns on mobile, 4 columns on desktop */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
          {staff.map((member) => (
            <Link 
              key={member.id} 
              to={`/staff/${member.id}/`}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300 group"
            >
              <img 
                src={member.image_url} 
                alt={member.name}
                className="w-full h-32 sm:h-40 object-cover group-hover:scale-105 transition duration-300"
              />
              <div className="p-3 sm:p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-sm sm:text-base font-semibold text-gray-800 line-clamp-2">
                    {member.name}
                  </h3>
                  <span className="bg-pink-100 text-pink-800 text-xs px-2 py-1 rounded-full ml-2 flex-shrink-0">
                    {member.role}
                  </span>
                </div>
                <div className="flex items-center mb-2">
                  <div className="flex items-center">
                    <span className="text-yellow-400 text-xs mr-1">⭐</span>
                    <span className="font-semibold text-xs">{member.rating}</span>
                  </div>
                  <span className="text-gray-500 ml-2 text-xs">
                    ({member.years_experience} years)
                  </span>
                </div>
                {/* Removed bio and specialties for compact design */}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SalonPage;
