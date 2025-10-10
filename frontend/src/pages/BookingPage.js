import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import ConfirmationBooking from '../components/ConfirmationBooking';
import { mockStaff, mockServices } from '../data/mockData';

const BookingPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  // Get parameters from URL
  const staffId = searchParams.get('staff_id');
  const serviceId = searchParams.get('service_id');
  
  // Booking form state
  const [booking, setBooking] = useState({
    staff_id: staffId || '',
    service_id: serviceId || '',
    date: '',
    start_time: '',
    end_time: '',
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    notes: ''
  });

  // Data state
  const [staff, setStaff] = useState(null);
  const [allStaff, setAllStaff] = useState([]);
  const [services, setServices] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [showConfirmation, setShowConfirmation] = useState(false);

  // Time slots (30-minute intervals)
  const timeSlots = [
    '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
    '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'
  ];

  const loadStaffAndServices = useCallback(async () => {
    // Helper function to set staff from data
    const setStaffFromData = (staffData) => {
      if (staffId) {
        const selectedStaff = staffData.find(s => s.id === parseInt(staffId));
        if (selectedStaff) {
          setStaff(selectedStaff);
        }
      }
    };
    try {
      setLoading(true);
      // Try to fetch from API first
      const [staffResponse, servicesResponse] = await Promise.all([
        fetch(`/api/salons/1/staffs/`),
        fetch(`/api/salons/1/services/`)
      ]);

      if (staffResponse.ok && servicesResponse.ok) {
        const staffData = await staffResponse.json();
        const servicesData = await servicesResponse.json();
        setAllStaff(staffData);
        setServices(servicesData);
        setStaffFromData(staffData);
      } else {
        // Use mock data if API fails
        setAllStaff(mockStaff);
        setServices(mockServices);
        setStaffFromData(mockStaff);
      }
    } catch (error) {
      console.log('Using mock data for booking');
      // Use mock data
      setAllStaff(mockStaff);
      setServices(mockServices);
      setStaffFromData(mockStaff);
    } finally {
      setLoading(false);
    }
  }, [staffId]);

  useEffect(() => {
    loadStaffAndServices();
  }, [loadStaffAndServices]);

  useEffect(() => {
    if (staffId && allStaff.length > 0) {
      const selectedStaff = allStaff.find(s => s.id === parseInt(staffId));
      if (selectedStaff) {
        setStaff(selectedStaff);
      }
    }
  }, [staffId, allStaff]);

  const handleInputChange = (field, value) => {
    setBooking(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleStaffChange = (selectedStaffId) => {
    const selectedStaff = allStaff.find(s => s.id === parseInt(selectedStaffId));
    setStaff(selectedStaff);
    setBooking(prev => ({
      ...prev,
      staff_id: selectedStaffId
    }));
  };

  const handleServiceChange = (serviceId) => {
    const service = services.find(s => s.id === parseInt(serviceId));
    if (service) {
      setBooking(prev => ({
        ...prev,
        service_id: serviceId,
        end_time: calculateEndTime(prev.start_time, service.duration)
      }));
    }
  };

  const calculateEndTime = (startTime, duration = 60) => {
    if (!startTime) return '';
    
    const [hours, minutes] = startTime.split(':').map(Number);
    const startMinutes = hours * 60 + minutes;
    const endMinutes = startMinutes + duration;
    const endHours = Math.floor(endMinutes / 60);
    const endMins = endMinutes % 60;
    
    return `${endHours.toString().padStart(2, '0')}:${endMins.toString().padStart(2, '0')}`;
  };

  const handleTimeChange = (time) => {
    const service = services.find(s => s.id === parseInt(booking.service_id));
    if (service) {
      setBooking(prev => ({
        ...prev,
        start_time: time,
        end_time: calculateEndTime(time, service.duration)
      }));
    }
  };

  const getAvailableSlots = (date) => {
    // Check if date is in the past
    const today = new Date();
    const selectedDate = new Date(date);
    
    if (selectedDate < today) {
      return [];
    }
    
    // Return all time slots for demo purposes
    return timeSlots;
  };

  const handleDateChange = (date) => {
    setBooking(prev => ({
      ...prev,
      date,
      start_time: '',
      end_time: ''
    }));
    setAvailableSlots(getAvailableSlots(date));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setMessage('');

    // Validate required fields
    if (!booking.staff_id || !booking.service_id || !booking.date || !booking.start_time || !booking.end_time) {
      setMessage('Please fill in all required fields.');
      return;
    }

    // Validate customer information
    if (!booking.customer_name) {
      setMessage('Please provide your name.');
      return;
    }

    if (!booking.customer_phone) {
      setMessage('Please provide your phone number.');
      return;
    }

    // Show confirmation page
    setShowConfirmation(true);
  };

  const handleConfirmBooking = async () => {
    setLoading(true);
    setMessage('');

    try {
      // Prepare appointment data for API
      const appointmentData = {
        staff_id: parseInt(booking.staff_id),
        service_id: parseInt(booking.service_id),
        date: booking.date,
        start_time: booking.start_time,
        end_time: booking.end_time,
        customer_name: booking.customer_name,
        customer_email: booking.customer_email || null,
        customer_phone: booking.customer_phone,
        notes: booking.notes || null
      };

      console.log('Sending appointment data:', appointmentData);

      const response = await fetch('/api/appointments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication header if available
          ...(localStorage.getItem('token') && {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          })
        },
        body: JSON.stringify(appointmentData)
      });

      const responseData = await response.json();

      if (response.ok) {
        setMessage('Appointment booked successfully!');
        console.log('Appointment created:', responseData);
        
        // Navigate to BookingInfoPage with booking data
        navigate('/booking-info', {
          state: {
            bookingData: {
              booking,
              selectedStaff,
              selectedService
            },
            message: 'Appointment booked successfully!'
          }
        });
      } else {
        console.error('Appointment booking failed:', responseData);
        setMessage(`Failed to book appointment: ${responseData.error || 'Please try again.'}`);
        setShowConfirmation(false);
      }
    } catch (error) {
      console.error('Network error:', error);
      setMessage('Network error. Please check your connection and try again.');
      setShowConfirmation(false);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelConfirmation = () => {
    setShowConfirmation(false);
    setMessage('');
  };

  const selectedService = services.find(s => s.id === parseInt(booking.service_id));
  const selectedStaff = allStaff.find(s => s.id === parseInt(booking.staff_id));

  if (loading && allStaff.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading booking information...</p>
        </div>
      </div>
    );
  }

  // Confirmation Page
  if (showConfirmation) {
    return (
      <ConfirmationBooking
        booking={booking}
        selectedStaff={selectedStaff}
        selectedService={selectedService}
        message={message}
        loading={loading}
        onCancel={handleCancelConfirmation}
        onConfirm={handleConfirmBooking}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Book Appointment</h1>
          <p className="text-gray-600">
            {staff ? `Schedule your appointment with ${staff.name}` : 'Select a staff member and service to book your appointment'}
          </p>
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Staff Information */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-base sm:text-xl font-semibold text-gray-900 mb-4">
                {staff ? 'Selected Staff' : 'Select Staff Member'}
              </h2>
              
              {staff ? (
                <div className="flex items-center space-x-4">
                  <img 
                    src={staff.image_url} 
                    alt={staff.name}
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div>
                    <h3 className="text-sm sm:text-lg font-semibold text-gray-900">{staff.name}</h3>
                    <p className="text-gray-600">{staff.role}</p>
                  </div>
                </div>
              ) : (
                <div>
                  <select
                    value={booking.staff_id}
                    onChange={(e) => handleStaffChange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                    required
                  >
                    <option value="">Choose a staff member...</option>
                    {allStaff.map(staffMember => (
                      <option key={staffMember.id} value={staffMember.id}>
                        {staffMember.name} - {staffMember.role}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            {/* Selected Service */}
            {selectedService && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-base sm:text-xl font-semibold text-gray-900 mb-4">Selected Service</h2>
                <div className="border border-gray-200 rounded-lg p-4">
                  <h3 className="text-sm sm:text-lg font-semibold text-gray-900">{selectedService.name}</h3>
                  <p className="text-lg sm:text-2xl font-bold text-pink-600 mt-2">${selectedService.price}</p>
                  <p className="text-gray-600">{selectedService.duration} minutes</p>
                </div>
              </div>
            )}
          </div>

          {/* Booking Form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-base sm:text-xl font-semibold text-gray-900 mb-6">Appointment Details</h2>
              
              <div className="space-y-6">
                {/* Staff Selection (if no staff pre-selected) */}
                {!staffId && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Staff Member *
                    </label>
                    <select
                      value={booking.staff_id}
                      onChange={(e) => handleStaffChange(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                      required
                    >
                      <option value="">Choose a staff member...</option>
                      {allStaff.map(staffMember => (
                        <option key={staffMember.id} value={staffMember.id}>
                          {staffMember.name} - {staffMember.role}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                {/* Service Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Service *
                  </label>
                  <select
                    value={booking.service_id}
                    onChange={(e) => handleServiceChange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                    required
                  >
                    <option value="">Choose a service...</option>
                    {services.map(service => (
                      <option key={service.id} value={service.id}>
                        {service.name} - ${service.price} ({service.duration} min)
                      </option>
                    ))}
                  </select>
                </div>

                {/* Date Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Date *
                  </label>
                  <input
                    type="date"
                    value={booking.date}
                    onChange={(e) => handleDateChange(e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                    required
                  />
                </div>

                {/* Time Selection */}
                {booking.date && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Time *
                    </label>
                    {availableSlots.length > 0 ? (
                      <div className="grid grid-cols-3 gap-2">
                        {availableSlots.map(time => (
                          <button
                            key={time}
                            type="button"
                            onClick={() => handleTimeChange(time)}
                            className={`px-3 py-2 text-sm rounded-md border ${
                              booking.start_time === time
                                ? 'bg-pink-600 text-white border-pink-600'
                                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                            }`}
                          >
                            {time}
                          </button>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-4 text-gray-500">
                        No available time slots for this date.
                      </div>
                    )}
                  </div>
                )}

                {/* Customer Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name *
                    </label>
                    <input
                      type="text"
                      value={booking.customer_name}
                      onChange={(e) => handleInputChange('customer_name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      value={booking.customer_email}
                      onChange={(e) => handleInputChange('customer_email', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Phone Number *
                    </label>
                    <input
                      type="tel"
                      value={booking.customer_phone}
                      onChange={(e) => handleInputChange('customer_phone', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                      required
                    />
                  </div>
                </div>

                {/* Notes */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Special Requests or Notes
                  </label>
                  <textarea
                    value={booking.notes}
                    onChange={(e) => handleInputChange('notes', e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                    placeholder="Any special requests or notes for your appointment..."
                  />
                </div>


                {/* Action Buttons */}
                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={() => navigate('/salon')}
                    className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={!booking.staff_id || !booking.service_id || !booking.date || !booking.start_time}
                    className="px-6 py-2 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Review & Confirm
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookingPage;
