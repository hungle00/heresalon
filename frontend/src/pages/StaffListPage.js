import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function StaffListPage() {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStaff();
  }, []);

  const fetchStaff = async () => {
    try {
      setLoading(true);
      setError(null); // Clear any previous errors
      const response = await fetch('/api/staff/');
      if (!response.ok) {
        throw new Error('Failed to fetch staff');
      }
      const data = await response.json();
      setStaff(data);
    } catch (err) {
      console.log('API fetch failed, using mock data:', err.message);
      setError(null); // Clear error state when using mock data
      // Mock data for development
      setStaff([
        {
          id: 1,
          name: 'Sarah Johnson',
          role: 'Senior Hair Stylist',
          bio: 'With over 8 years of experience in hair styling and coloring.',
          years_experience: 8,
          seniority: 'Senior',
          rating: 4.9,
          specialties: ['Hair Coloring', 'Hair Cutting', 'Styling'],
          image_url: 'https://via.placeholder.com/300x200?text=Sarah+Johnson'
        },
        {
          id: 2,
          name: 'Mike Chen',
          role: 'Barber',
          bio: 'Expert in men\'s grooming and traditional barbering techniques.',
          years_experience: 5,
          seniority: 'Senior',
          rating: 4.8,
          specialties: ['Men\'s Haircuts', 'Beard Trimming', 'Shaving'],
          image_url: 'https://via.placeholder.com/300x200?text=Mike+Chen'
        },
        {
          id: 3,
          name: 'Emma Davis',
          role: 'Beauty Specialist',
          bio: 'Specialized in facial treatments and beauty services.',
          years_experience: 6,
          seniority: 'Senior',
          rating: 4.7,
          specialties: ['Facials', 'Manicures', 'Pedicures'],
          image_url: 'https://via.placeholder.com/300x200?text=Emma+Davis'
        }
      ]);
    } finally {
      setLoading(false);
    }
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Our Professional Staff
        </h1>
        <p className="text-lg text-gray-600">
          Meet our experienced team of beauty and hair professionals.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {staff.map((member) => (
          <div key={member.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
            <img 
              src={member.image_url} 
              alt={member.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {member.name}
              </h3>
              <p className="text-gray-600 mb-3">
                {member.role}
              </p>
              <p className="text-gray-700 mb-4">
                {member.bio}
              </p>
              
              <div className="mb-4">
                <div className="flex items-center mb-2">
                  <span className="text-sm text-gray-600">Experience: {member.years_experience} years</span>
                </div>
                <div className="flex items-center mb-3">
                  <span className="text-sm text-gray-600">Rating: {member.rating}/5.0</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {member.specialties.map((specialty) => (
                    <span 
                      key={specialty}
                      className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>
              
              <Link 
                to={`/staff/${member.id}`}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300 inline-block"
              >
                View Profile
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StaffListPage;
