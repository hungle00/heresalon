import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      {/* Hero Section with Visual Image */}
      <div className="relative h-64 sm:h-80 lg:h-96 overflow-hidden">
        <img 
          src="https://images.unsplash.com/photo-1560066984-138dadb4c035?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2074&q=80"
          alt="Beautiful Salon Interior"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div className="text-center text-white px-4 max-w-4xl">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold mb-4">
              Welcome to Here Salon
            </h1>
            <p className="text-base sm:text-lg lg:text-xl mb-6 sm:mb-8">
              Professional beauty and wellness services with expert hair stylists
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
              <Link 
                to="/salon"
                className="bg-pink-600 text-white px-6 py-3 rounded-lg text-sm sm:text-base font-semibold hover:bg-pink-700 transition duration-300"
              >
                View Our Salon
              </Link>
              <Link 
                to="/booking"
                className="bg-white text-pink-600 px-6 py-3 rounded-lg text-sm sm:text-base font-semibold hover:bg-gray-100 transition duration-300"
              >
                Book Appointment
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section - Mobile First */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8 sm:mb-12 text-gray-800">
          Our Services
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {/* Hair Styling Card */}
          <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition duration-300">
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <span className="text-lg sm:text-2xl">✂️</span>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-gray-800">Hair Styling</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Professional hair cutting, styling, and coloring services by our expert stylists.
              </p>
              <Link 
                to="/salon"
                className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition duration-300 text-sm sm:text-base"
              >
                Meet Our Stylists
              </Link>
            </div>
          </div>

          {/* Beauty Services Card */}
          <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition duration-300">
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <span className="text-lg sm:text-2xl">💅</span>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-gray-800">Beauty Services</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Comprehensive beauty treatments including facials, manicures, and more.
              </p>
              <Link 
                to="/salon"
                className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition duration-300 text-sm sm:text-base"
              >
                View Services
              </Link>
            </div>
          </div>

          {/* Expert Staff Card */}
          <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 hover:shadow-lg transition duration-300 sm:col-span-2 lg:col-span-1">
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <span className="text-lg sm:text-2xl">👥</span>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-gray-800">Expert Staff</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Our experienced professionals are here to provide you with the best service.
              </p>
              <Link 
                to="/salon"
                className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition duration-300 text-sm sm:text-base"
              >
                Meet the Team
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action Section */}
      <div className="bg-pink-50 py-8 sm:py-12 lg:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-4 sm:mb-6 text-gray-800">
            Ready to Transform Your Look?
          </h2>
          <p className="text-base sm:text-lg text-gray-600 mb-6 sm:mb-8 max-w-2xl mx-auto">
            Book your appointment today and experience the difference of professional beauty services.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
            <Link 
              to="/booking"
              className="bg-pink-600 text-white px-8 py-3 rounded-lg text-sm sm:text-base font-semibold hover:bg-pink-700 transition duration-300"
            >
              Book Now
            </Link>
            <Link 
              to="/salon"
              className="bg-white text-pink-600 px-8 py-3 rounded-lg text-sm sm:text-base font-semibold hover:bg-gray-100 transition duration-300 border border-pink-600"
            >
              Explore Services
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
