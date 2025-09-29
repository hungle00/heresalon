import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import HomePage from './pages/HomePage';
import SalonPage from './pages/SalonPage';
import StaffProfilePage from './pages/StaffProfilePage';
import StaffCalendarPage from './pages/staffs/CalendarPage';
import ProfileEditPage from './pages/staffs/ProfileEditPage';
import BookingPage from './pages/BookingPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-blue-600 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="text-white text-xl font-bold">
                  Heresalon
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link 
                  to="/" 
                  className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Home
                </Link>
                <Link 
                  to="/salon" 
                  className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Salon
                </Link>
                <Link 
                  to="/staff/calendar" 
                  className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Calendar
                </Link>
              </div>
            </div>
          </div>
        </nav>
        
        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/salon" element={<SalonPage />} />
            <Route path="/staff/:id" element={<StaffProfilePage />} />
            <Route path="/staff/:id/edit" element={<ProfileEditPage />} />
            <Route path="/booking" element={<BookingPage />} />
            <Route path="/staff/calendar" element={<StaffCalendarPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
