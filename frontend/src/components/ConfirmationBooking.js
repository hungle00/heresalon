import React from 'react';

const ConfirmationPage = ({ 
  booking, 
  selectedStaff, 
  selectedService, 
  message, 
  loading, 
  onCancel, 
  onConfirm 
}) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Confirm Your Appointment</h1>
          <p className="text-gray-600">Please review your appointment details before confirming</p>
        </div>

        {/* Success Message */}
        {message && (
          <div className={`mb-6 p-4 rounded-md ${
            message.includes('successfully') 
              ? 'bg-green-50 text-green-800 border border-green-200' 
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {message}
          </div>
        )}

        <div className="max-w-4xl mx-auto">
          {/* Appointment Summary */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Appointment Summary</h2>
            
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

          {/* Action Buttons */}
          <div className="flex justify-between">
            <button
              onClick={onCancel}
              className="px-6 py-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              ← Back to Edit
            </button>
            <button
              onClick={onConfirm}
              disabled={loading}
              className="px-8 py-3 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Confirming...' : 'Booking'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationPage;
