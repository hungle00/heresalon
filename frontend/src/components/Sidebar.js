import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoginModal from './LoginModal';

const Sidebar = ({ isOpen, onClose }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const location = useLocation();
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLogout = async () => {
    await logout();
    onClose();
  };

  const handleLoginClick = () => {
    onClose();
    setShowLoginModal(true);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />
      
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl transform transition-transform duration-300 ease-in-out">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <Link to="/" className="text-pink-600 text-xl font-bold" onClick={onClose}>
              Heresalon
            </Link>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <Link
              to="/salon"
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/salon') 
                  ? 'bg-pink-100 text-pink-600' 
                  : 'text-gray-700 hover:bg-pink-50 hover:text-pink-600'
              }`}
              onClick={onClose}
            >
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Salon
            </Link>

            {isAuthenticated && (
              <Link
                to="/staff/calendar"
                className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/staff/calendar') 
                    ? 'bg-pink-100 text-pink-600' 
                    : 'text-gray-700 hover:bg-pink-50 hover:text-pink-600'
                }`}
                onClick={onClose}
              >
                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Calendar
              </Link>
            )}
          </nav>

          {/* User Section */}
          <div className="border-t border-gray-200 p-4">
            {isAuthenticated ? (
              <div className="space-y-3">
                <div className="text-gray-600 text-sm">
                  <p className="font-medium text-pink-600">Welcome back!</p>
                  <p className="text-gray-500 truncate">{user?.username || user?.email}</p>
                </div>
                <button
                  onClick={handleLogout}
                  className="w-full bg-pink-600 text-white py-2 px-4 rounded-md hover:bg-pink-700 transition-colors text-sm font-medium"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-gray-600 text-sm">Please login to access all features</p>
                <button
                  onClick={handleLoginClick}
                  className="w-full bg-pink-600 text-white py-2 px-4 rounded-md hover:bg-pink-700 transition-colors text-sm font-medium"
                >
                  Login
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLoginSuccess={() => setShowLoginModal(false)}
      />
    </>
  );
};

export default Sidebar;
