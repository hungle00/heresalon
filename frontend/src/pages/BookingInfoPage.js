import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const BookingInfoPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get booking data from location state
  const bookingData = location.state?.bookingData;
  const successMessage = location.state?.message;

  // If no booking data, redirect to salon page
  if (!bookingData) {
    navigate('/salon');
    return null;
  }

  const { booking, selectedStaff, selectedService } = bookingData;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Success Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Appointment Booked Successfully!</h1>
          <p className="text-gray-600">Your appointment has been confirmed. Here are the details:</p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="mb-6 p-4 rounded-md bg-green-50 text-green-800 border border-green-200">
            {successMessage}
          </div>
        )}

        <div className="max-w-4xl mx-auto">
          {/* Appointment Details */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Appointment Details</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Staff Information */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Staff Member</h3>
                {selectedStaff && (
                  <div className="flex items-center space-x-4">
                    <img 
                      src={selectedStaff.image_url} 
                      alt={selectedStaff.name}
                      className="w-16 h-16 rounded-full object-cover"
                    />
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">{selectedStaff.name}</h4>
                      <p className="text-gray-600">{selectedStaff.role}</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Service Information */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Service</h3>
                {selectedService && (
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-gray-900">{selectedService.name}</h4>
                    <p className="text-2xl font-bold text-pink-600 mt-2">${selectedService.price}</p>
                    <p className="text-gray-600">{selectedService.duration} minutes</p>
                  </div>
                )}
              </div>
            </div>

            {/* Date & Time */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Date & Time</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Date</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {new Date(booking.date).toLocaleDateString('en-US', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Time</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {booking.start_time} - {booking.end_time}
                  </p>
                </div>
              </div>
            </div>

            {/* Customer Information */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Your Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Name</p>
                  <p className="text-lg font-semibold text-gray-900">{booking.customer_name}</p>
                </div>
                {booking.customer_email && (
                  <div>
                    <p className="text-sm text-gray-600">Email</p>
                    <p className="text-lg font-semibold text-gray-900">{booking.customer_email}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm text-gray-600">Phone</p>
                  <p className="text-lg font-semibold text-gray-900">{booking.customer_phone}</p>
                </div>
              </div>
              {booking.notes && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600">Special Requests</p>
                  <p className="text-lg font-semibold text-gray-900">{booking.notes}</p>
                </div>
              )}
            </div>
          </div>

          {/* Important Information */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Important Information</h3>
            <ul className="space-y-2 text-blue-800">
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Please arrive 10 minutes before your appointment time.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>We'll send you a confirmation SMS shortly.</span>
              </li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/salon')}
              className="px-6 py-3 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500"
            >
              Book Another Appointment
            </button>
            <button
              onClick={() => navigate('/')}
              className="px-6 py-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Back to Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookingInfoPage;
