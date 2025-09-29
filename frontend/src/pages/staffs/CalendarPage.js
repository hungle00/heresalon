import React from 'react';
import Calendar from '../../components/Calendar';

const StaffCalendarPage = () => {
    return (
        <div className="min-h-screen bg-gray-50">
            <div className="container mx-auto px-4 py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Staff Calendar</h1>
                    <p className="text-gray-600">Manage your appointments and schedule</p>
                </div>
                
                <Calendar />
            </div>
        </div>
    );
};

export default StaffCalendarPage;
