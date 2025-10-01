import React, { useState } from 'react';
import { mockEvents, getEventsForDate } from '../data/mockData';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDay, setSelectedDay] = useState(null); // Track selected day
  const [selectedDayEvents, setSelectedDayEvents] = useState([]); // Events for selected day

  // Generate calendar data
  const generateCalendarData = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay()); // Start from Sunday

    const days = [];
    const totalDays = 42; // 6 weeks * 7 days

    for (let i = 0; i < totalDays; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      
      const dayNumber = date.getDate();
      const isCurrentMonth = date.getMonth() === month;
      const isToday = date.getDate() === 9 && date.getMonth() === month; // Sample today
      
      // Get only the first event for this day (if multiple events exist)
      const firstEvent = isCurrentMonth ? getEventsForDate(year, month, dayNumber)[0] : null;
      
      days.push({
        date: date,
        dayNumber,
        isCurrentMonth,
        isToday,
        event: firstEvent // Only store the first event
      });
    }

    return days;
  };

  const calendarData = generateCalendarData();
  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const getEventColorClasses = (color) => {
    const colorMap = {
      pink: 'bg-pink-50 text-pink-600',
      emerald: 'bg-emerald-50 text-emerald-600',
      sky: 'bg-sky-50 text-sky-600',
      indigo: 'bg-indigo-50 text-indigo-600',
      blue: 'bg-blue-50 text-blue-600',
      purple: 'bg-purple-50 text-purple-600',
      orange: 'bg-orange-50 text-orange-600',
      red: 'bg-red-50 text-red-600',
      yellow: 'bg-yellow-50 text-yellow-600',
      teal: 'bg-teal-50 text-teal-600',
      cyan: 'bg-cyan-50 text-cyan-600',
      rose: 'bg-rose-50 text-rose-600',
      lime: 'bg-lime-50 text-lime-600',
      violet: 'bg-violet-50 text-violet-600',
      amber: 'bg-amber-50 text-amber-600',
      fuchsia: 'bg-fuchsia-50 text-fuchsia-600',
      slate: 'bg-slate-50 text-slate-600',
      green: 'bg-green-50 text-green-600',
      gold: 'bg-yellow-100 text-yellow-800',
      gray: 'bg-gray-50 text-gray-600'
    };
    return colorMap[color] || 'bg-pink-50 text-pink-600';
  };

  const getDayClasses = (day) => {
    let classes = 'flex xl:aspect-square max-xl:min-h-[60px] p-3.5 border-r border-b border-pink-200 transition-all duration-300 hover:bg-pink-50 cursor-pointer';
    
    // Check if this day is selected first
    const isSelected = selectedDay && selectedDay.dayNumber === day.dayNumber && day.isCurrentMonth;
    
    if (isSelected) {
      classes += ' ring-2 ring-pink-500 bg-pink-100';
    } else if (!day.isCurrentMonth) {
      classes += ' bg-gray-50';
    } else {
      classes += ' bg-white';
    }

    // Add rounded corners for specific positions
    if (day.dayNumber === 1 && day.isCurrentMonth) {
      classes += ' rounded-tl-xl';
    }
    if (day.dayNumber === 7 && day.isCurrentMonth) {
      classes += ' rounded-tr-xl';
    }
    if (day.dayNumber === 29 && day.isCurrentMonth) {
      classes += ' rounded-bl-xl';
    }
    if (day.dayNumber === 6 && !day.isCurrentMonth) {
      classes += ' rounded-br-xl';
    }

    return classes;
  };

  const getDayNumberClasses = (day) => {
    let classes = 'text-xs font-semibold';
    
    if (!day.isCurrentMonth) {
      classes += ' text-gray-400';
    } else if (day.isToday) {
      classes += ' text-pink-600 sm:text-white sm:w-6 sm:h-6 rounded-full sm:flex items-center justify-center sm:bg-pink-600';
    } else {
      classes += ' text-gray-900';
    }

    return classes;
  };

  // Handle day click
  const handleDayClick = (day) => {
    if (!day.isCurrentMonth) return; // Don't allow clicking on days from other months
    
    setSelectedDay(day);
    
    // Get all events for this day
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const events = getEventsForDate(year, month, day.dayNumber);
    setSelectedDayEvents(events);
  };

  // Get today's events (default display)
  const getTodaysEvents = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const today = 9; // Sample today for demo
    return getEventsForDate(year, month, today);
  };

  // Get events to display in sidebar
  const getSidebarEvents = () => {
    // If a day is selected and it has events, show those events
    if (selectedDay && selectedDayEvents.length > 0) {
      return selectedDayEvents;
    }
    
    // If a day is selected but has no events, show empty state
    if (selectedDay && selectedDayEvents.length === 0) {
      return [];
    }
    
    // Default: show today's events
    return getTodaysEvents();
  };

  // Get sidebar title
  const getSidebarTitle = () => {
    if (selectedDay) {
      if (selectedDayEvents.length > 0) {
        return `Events for ${selectedDay.dayNumber}`;
      } else {
        return `No events for ${selectedDay.dayNumber}`;
      }
    }
    return 'Today\'s Events';
  };

  return (
    <section className="relative bg-stone-50">
      <div className="bg-pink-400 w-full sm:w-20 h-20 sm:h-20 rounded-full absolute top-4 opacity-20 sm:left-8 z-0"></div>
      <div className="bg-pink-500 w-full sm:w-20 h-12 sm:h-16 absolute top-2 opacity-20 z-0"></div>
      <div className="bg-pink-600 w-full sm:w-20 h-12 sm:h-14 absolute top-32 opacity-20 z-0"></div>
      <div className="w-full py-12 relative z-10 backdrop-blur-3xl">
        <div className="w-full max-w-7xl mx-auto px-2 lg:px-8">
          <div className="grid grid-cols-12 gap-8 max-w-4xl mx-auto xl:max-w-full">
            <div className="col-span-12 xl:col-span-7 px-2.5 py-5 sm:p-8 bg-gradient-to-b from-white/25 to-white xl:bg-white rounded-2xl max-xl:row-start-1">
              <div className="flex flex-col md:flex-row gap-4 items-center justify-between mb-5">
                <div className="flex items-center gap-4">
                  <h5 className="text-xl leading-8 font-semibold text-gray-900">
                    {currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                  </h5>
                  <div className="flex items-center">
                    <button 
                      className="text-pink-600 p-1 rounded transition-all duration-300 hover:text-white hover:bg-pink-600"
                      onClick={() => {
                        const newDate = new Date(currentDate);
                        newDate.setMonth(newDate.getMonth() - 1);
                        setCurrentDate(newDate);
                        setSelectedDay(null); // Clear selection when changing month
                        setSelectedDayEvents([]);
                      }}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M10.0002 11.9999L6 7.99971L10.0025 3.99719" stroke="currentcolor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"></path>
                      </svg>
                    </button>
                    <button 
                      className="text-pink-600 p-1 rounded transition-all duration-300 hover:text-white hover:bg-pink-600"
                      onClick={() => {
                        const newDate = new Date(currentDate);
                        newDate.setMonth(newDate.getMonth() + 1);
                        setCurrentDate(newDate);
                        setSelectedDay(null); // Clear selection when changing month
                        setSelectedDayEvents([]);
                      }}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M6.00236 3.99707L10.0025 7.99723L6 11.9998" stroke="currentcolor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div className="border border-pink-200 rounded-xl">
                {/* Week day headers */}
                <div className="grid grid-cols-7 rounded-t-3xl border-b border-pink-200">
                  {weekDays.map((day, index) => (
                    <div
                      key={day}
                      className={`py-3.5 border-r border-pink-200 bg-pink-50 flex items-center justify-center text-sm font-medium text-pink-600 ${
                        index === 0 ? 'rounded-tl-xl' : ''
                      } ${index === 6 ? 'rounded-tr-xl border-r-0' : ''}`}
                    >
                      {day}
                    </div>
                  ))}
                </div>
                
                {/* Calendar days */}
                <div className="grid grid-cols-7 rounded-b-xl">
                  {calendarData.map((day, index) => (
                    <div
                      key={index}
                      className={getDayClasses(day)}
                      onClick={() => handleDayClick(day)}
                    >
                      <span className={getDayNumberClasses(day)}>
                        {day.dayNumber}
                      </span>
                      
                      {/* Event - only show first event if it exists */}
                      {day.event && (
                        <div
                          className={`left-3.5 p-1.5 xl:px-2.5 h-max rounded ${getEventColorClasses(day.event.color)}`}
                        >
                          <p className="hidden xl:block text-xs font-medium mb-px whitespace-nowrap">
                            {day.event.title}
                          </p>
                          {day.event.time && (
                            <span className="hidden xl:block text-xs font-normal whitespace-nowrap">
                              {day.event.time}
                            </span>
                          )}
                          <p className="xl:hidden w-2 h-2 rounded-full bg-pink-600"></p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Sidebar */}
            <div className="col-span-12 xl:col-span-5 px-2.5 py-5 sm:p-8 bg-gradient-to-b from-white/25 to-white xl:bg-white rounded-2xl max-xl:row-start-2">
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <h5 className="text-xl leading-8 font-semibold text-gray-900">{getSidebarTitle()}</h5>
                  {selectedDay && (
                    <button
                      onClick={() => {
                        setSelectedDay(null);
                        setSelectedDayEvents([]);
                      }}
                      className="text-sm text-pink-600 hover:text-pink-700 underline"
                    >
                      Show Today
                    </button>
                  )}
                </div>
                <div className="space-y-3">
                  {getSidebarEvents().length > 0 ? (
                    getSidebarEvents().map((event, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className={`w-3 h-3 rounded-full ${getEventColorClasses(event.color).split(' ')[0]}`}></div>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">{event.title}</p>
                          <p className="text-xs text-gray-500">{event.time}</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8">
                      <div className="text-gray-400 mb-2">
                        <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <p className="text-gray-500 text-sm">
                        {selectedDay ? `No events for day ${selectedDay.dayNumber}` : 'No events today'}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Calendar;
