import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-pink-500 to-orange-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Welcome to Salon Management
          </h1>
          <p className="text-xl md:text-2xl mb-8">
            Professional salon services with expert staff
          </p>
          <Link 
            to="/staff"
            className="bg-white text-pink-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition duration-300"
          >
            View Our Staff
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          Our Services
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Hair Styling Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition duration-300">
            <div className="text-center">
              <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">✂️</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Hair Styling</h3>
              <p className="text-gray-600 mb-4">
                Professional hair cutting, styling, and coloring services by our expert stylists.
              </p>
              <Link 
                to="/staff"
                className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition duration-300"
              >
                Meet Our Stylists
              </Link>
            </div>
          </div>

          {/* Beauty Services Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition duration-300">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💅</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Beauty Services</h3>
              <p className="text-gray-600 mb-4">
                Comprehensive beauty treatments including facials, manicures, and more.
              </p>
              <Link 
                to="/staff"
                className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition duration-300"
              >
                View Specialists
              </Link>
            </div>
          </div>

          {/* Expert Staff Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition duration-300">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">👥</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Expert Staff</h3>
              <p className="text-gray-600 mb-4">
                Our experienced professionals are here to provide you with the best service.
              </p>
              <Link 
                to="/staff"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300"
              >
                Meet the Team
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
