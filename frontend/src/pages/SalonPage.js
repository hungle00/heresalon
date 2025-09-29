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
      const staffResponse = await fetch('/api/staff/');
      if (!staffResponse.ok) {
        throw new Error('Failed to fetch staff');
      }
      const staffData = await staffResponse.json();
      setStaff(staffData);

      // Fetch services data
      const servicesResponse = await fetch('/api/services/');
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

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price);
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Services Section */}
      <div className="mb-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Our Services
          </h2>
          <p className="text-lg text-gray-600">
            Professional beauty and wellness services tailored to your needs
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service) => (
            <div key={service.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
              <img 
                src={service.image_url} 
                alt={service.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-gray-800">
                    {service.name}
                  </h3>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                    {getServiceTypeLabel(service.type)}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">
                  {service.description}
                </p>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-blue-600">
                    {formatPrice(service.price)}
                  </span>
                  <Link
                    to={`/booking?service_id=${service.id}`}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300"
                  >
                    Book Now
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Staff Section */}
      <div>
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Our Professional Staff
          </h2>
          <p className="text-lg text-gray-600">
            Meet our experienced and talented team of beauty professionals
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {staff.map((member) => (
            <div key={member.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
              <img 
                src={member.image_url} 
                alt={member.name}
                className="w-full h-64 object-cover"
              />
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  {member.name}
                </h3>
                <p className="text-gray-600 mb-4">
                  {member.role}
                </p>
                <div className="flex items-center mb-4">
                  <div className="flex items-center">
                    <span className="text-yellow-400 text-lg mr-1">⭐</span>
                    <span className="font-semibold">{member.rating}</span>
                  </div>
                  <span className="text-gray-500 ml-2">
                    ({member.years_experience} years experience)
                  </span>
                </div>
                <p className="text-gray-700 mb-6">
                  {member.bio}
                </p>
                <div className="flex flex-wrap gap-2 mb-6">
                  {member.specialties?.map((specialty, index) => (
                    <span 
                      key={index}
                      className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
                
                <Link 
                  to={`/staff/${member.id}/`}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300 inline-block"
                >
                  View Profile
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SalonPage;
