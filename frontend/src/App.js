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
import BookingInfoPage from './pages/BookingInfoPage';
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
  // Example callbacks for ChatWidget: you can replace sendMessageToApi with your real API
  const handleDispatch = (userMsg) => {
    // Called immediately when user sends a message
    console.log('Dispatched message:', userMsg);
  };

  const sendMessageToApi = async (userMsg) => {
    // Try calling a backend endpoint `/api/chat` (adjust path as needed).
    // Expected backend response JSON: { reply: '...' }
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userMsg.text }),
      });
      if (!res.ok) throw new Error('Network response was not ok');
      const data = await res.json();
      // Return an object compatible with ChatWidget message format
      return { id: Date.now(), from: 'bot', text: data.reply ?? String(data) };
    } catch (err) {
      console.error('sendMessageToApi error', err);
      // Let ChatWidget handle fallback/timeout; return a fallback text to display immediately if desired
      return { id: Date.now(), from: 'bot', text: 'Sorry, could not reach server.' };
    }
  };

  const handleResponse = (botMsg) => {
    // Called when a bot response is received
    console.log('Bot response:', botMsg);
  };
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
              <Route path="/booking-info" element={<BookingInfoPage />} />
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
          <ChatWidget onDispatch={handleDispatch} sendMessageToApi={sendMessageToApi} onResponse={handleResponse} />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
