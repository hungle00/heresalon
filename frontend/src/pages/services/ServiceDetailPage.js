import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { mockServices } from '../../data/mockData';

function ServiceDetailPage() {
  const { id } = useParams();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchService();
  }, [id]);

  const fetchService = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to fetch from API first
      const response = await fetch(`/api/services/${id}/`);
      if (response.ok) {
        const serviceData = await response.json();
        setService(serviceData);
      } else {
        throw new Error('Service not found');
      }
    } catch (err) {
      console.log('API fetch failed, using mock data:', err.message);
      // Use mock data as fallback
      const mockService = mockServices.find(s => s.id === parseInt(id));
      if (mockService) {
        setService(mockService);
      } else {
        setError('Service not found');
      }
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
      'Hair': 'Hair Care',
      'Nails': 'Nail Care',
      'Skin': 'Skin Care',
      'Massage': 'Massage Therapy'
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

  if (error || !service) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Service Not Found</h1>
          <p className="text-gray-600 mb-8">The service you're looking for doesn't exist.</p>
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
      {/* Breadcrumb */}
      <nav className="mb-8">
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Link to="/" className="hover:text-pink-600">Home</Link>
          <span>/</span>
          <Link to="/salon" className="hover:text-pink-600">Salon</Link>
          <span>/</span>
          <span className="text-gray-800">{service.name}</span>
        </div>
      </nav>

      {/* Service Header */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        {/* Service Image */}
        <div className="relative">
          <img 
            src={service.image_url} 
            alt={service.name}
            className="w-full h-64 sm:h-80 lg:h-96 object-cover rounded-lg shadow-lg"
          />
          <div className="absolute top-4 left-4">
            <span className="bg-pink-100 text-pink-800 px-3 py-1 rounded-full text-sm font-medium">
              {getServiceTypeLabel(service.type)}
            </span>
          </div>
        </div>

        {/* Service Info */}
        <div className="flex flex-col justify-center">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-4">
            {service.name}
          </h1>
          
          <div className="mb-6">
            <span className="text-3xl font-bold text-pink-600">
              {formatPrice(service.price)}
            </span>
            <span className="text-gray-500 ml-2">per session</span>
          </div>

          <p className="text-lg text-gray-600 mb-8 leading-relaxed">
            {service.description}
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              to={`/booking?service_id=${service.id}`}
              className="bg-pink-600 text-white px-8 py-3 rounded-lg hover:bg-pink-700 transition duration-300 text-center font-semibold"
            >
              Book This Service
            </Link>
            <Link
              to="/salon"
              className="bg-gray-100 text-gray-700 px-8 py-3 rounded-lg hover:bg-gray-200 transition duration-300 text-center font-semibold"
            >
              View All Services
            </Link>
          </div>
        </div>
      </div>

      {/* Service Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Service Details</h2>
            
            <div className="prose max-w-none">
              <p className="text-gray-600 leading-relaxed mb-6">
                Our {service.name.toLowerCase()} service is designed to provide you with the ultimate 
                relaxation and beauty experience. Our skilled professionals use only the finest 
                products and techniques to ensure you leave feeling refreshed and rejuvenated.
              </p>
              
              <h3 className="text-xl font-semibold text-gray-800 mb-4">What's Included:</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-6">
                <li>Professional consultation and assessment</li>
                <li>High-quality products and tools</li>
                <li>Relaxing atmosphere with soothing music</li>
                <li>Expert techniques and personalized care</li>
                <li>Aftercare tips and recommendations</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-800 mb-4">Duration:</h3>
              <p className="text-gray-600 mb-6">
                Approximately 60-90 minutes depending on the specific treatment and your individual needs.
              </p>

              <h3 className="text-xl font-semibold text-gray-800 mb-4">Preparation:</h3>
              <p className="text-gray-600">
                Please arrive 10 minutes early for your appointment. We recommend wearing comfortable 
                clothing and removing any jewelry that might interfere with the treatment.
              </p>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Booking Card */}
          <div className="bg-pink-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Ready to Book?</h3>
            <p className="text-gray-600 mb-4">
              Schedule your {service.name.toLowerCase()} appointment today and experience the difference.
            </p>
            <Link
              to={`/booking?service_id=${service.id}`}
              className="w-full bg-pink-600 text-white px-4 py-3 rounded-lg hover:bg-pink-700 transition duration-300 text-center block font-semibold"
            >
              Book Now
            </Link>
          </div>

          {/* Contact Info */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Contact Us</h3>
            <div className="space-y-3 text-gray-600">
              <div className="flex items-center">
                <span className="text-pink-600 mr-3">📞</span>
                <span>+84 123 456 789</span>
              </div>
              <div className="flex items-center">
                <span className="text-pink-600 mr-3">📧</span>
                <span>info@heresalon.com</span>
              </div>
              <div className="flex items-center">
                <span className="text-pink-600 mr-3">📍</span>
                <span>123 Beauty Street, District 1, HCMC</span>
              </div>
            </div>
          </div>

          {/* Hours */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Opening Hours</h3>
            <div className="space-y-2 text-gray-600">
              <div className="flex justify-between">
                <span>Monday - Friday</span>
                <span>9:00 AM - 8:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span>Saturday</span>
                <span>9:00 AM - 6:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span>Sunday</span>
                <span>10:00 AM - 4:00 PM</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ServiceDetailPage;
