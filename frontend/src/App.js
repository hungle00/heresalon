import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginModal from './components/LoginModal';
import Sidebar from './components/Sidebar';
import ProtectedRoute from './components/ProtectedRoute';
import ChatWidget from './components/ChatWidget';

// Import pages
import HomePage from './pages/HomePage';
import SalonPage from './pages/SalonPage';
import StaffProfilePage from './pages/StaffProfilePage';
import StaffCalendarPage from './pages/staffs/CalendarPage';
import ProfileEditPage from './pages/staffs/ProfileEditPage';
import BookingPage from './pages/BookingPage';
import ServiceDetailPage from './pages/services/ServiceDetailPage';

function Navigation() {
  const { user, logout, isAuthenticated } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <>
      <nav className="bg-pink-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Link to="/" className="text-white text-xl font-bold">
                Heresalon
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-4">
              <Link 
                to="/salon" 
                className="text-white hover:text-pink-200 px-3 py-2 rounded-md text-sm font-medium"
              >
                Salon
              </Link>
              
              {isAuthenticated && (
                <Link 
                  to="/staff/calendar" 
                  className="text-white hover:text-pink-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Calendar
                </Link>
              )}
              
              {isAuthenticated ? (
                <div className="flex items-center space-x-4">
                  <span className="text-white text-sm">
                    Welcome, {user?.username || user?.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="text-white hover:text-pink-200 px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="text-white hover:text-pink-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Login
                </button>
              )}
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setShowSidebar(true)}
                className="text-white hover:text-pink-200 p-2"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Sidebar */}
      <Sidebar 
        isOpen={showSidebar} 
        onClose={() => setShowSidebar(false)} 
      />

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLoginSuccess={() => setShowLoginModal(false)}
      />
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navigation />
          
          {/* Main Content */}
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/salon" element={<SalonPage />} />
              <Route path="/service/:id" element={<ServiceDetailPage />} />
              <Route path="/staff/:id" element={<StaffProfilePage />} />
              <Route path="/staff/:id/edit" element={<ProfileEditPage />} />
              <Route path="/booking" element={<BookingPage />} />
              <Route 
                path="/staff/calendar" 
                element={
                  <ProtectedRoute>
                    <StaffCalendarPage />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
          {/* Chat widget (global) */}
          <ChatWidget />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
