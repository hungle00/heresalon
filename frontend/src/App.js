import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import HomePage from './pages/HomePage';
import StaffListPage from './pages/StaffListPage';
import StaffProfilePage from './pages/StaffProfilePage';

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
                  Salon Management
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
                  to="/staff" 
                  className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Staff
                </Link>
              </div>
            </div>
          </div>
        </nav>
        
        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/staff" element={<StaffListPage />} />
            <Route path="/staff/:id" element={<StaffProfilePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
