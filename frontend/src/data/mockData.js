// Mock data for development and fallback when API is unavailable

export const mockStaff = [
  {
    id: 1,
    name: 'Sarah Johnson',
    role: 'Senior Hair Stylist',
    bio: 'With over 8 years of experience in hair styling and coloring.',
    years_experience: 8,
    seniority: 'Senior',
    rating: 4.9,
    specialties: ['Hair Coloring', 'Hair Cutting', 'Styling'],
    image_url: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face'
  },
  {
    id: 2,
    name: 'Mike Chen',
    role: 'Master Barber',
    bio: 'Expert in men\'s grooming and traditional barbering techniques.',
    years_experience: 5,
    seniority: 'Senior',
    rating: 4.8,
    specialties: ['Men\'s Haircuts', 'Beard Trimming', 'Shaving'],
    image_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
  },
  {
    id: 3,
    name: 'Emma Wilson',
    role: 'Nail Specialist',
    bio: 'Specialized in facial treatments and beauty services.',
    years_experience: 6,
    seniority: 'Senior',
    rating: 4.7,
    specialties: ['Facials', 'Manicures', 'Pedicures'],
    image_url: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face'
  }
];

export const mockServices = [
  {
    id: 1,
    name: 'Hair Cut & Style',
    description: 'Professional haircut and styling service',
    type: 'hair_cut',
    price: 75,
    duration: 60,
    image_url: 'https://via.placeholder.com/300x200?text=Hair+Cut'
  },
  {
    id: 2,
    name: 'Hair Coloring',
    description: 'Full hair coloring service with premium products',
    type: 'hair_color',
    price: 120,
    duration: 90,
    image_url: 'https://via.placeholder.com/300x200?text=Hair+Color'
  },
  {
    id: 3,
    name: 'Facial Treatment',
    description: 'Deep cleansing and moisturizing facial treatment',
    type: 'facial',
    price: 80,
    duration: 60,
    image_url: 'https://via.placeholder.com/300x200?text=Facial'
  },
  {
    id: 4,
    name: 'Manicure & Pedicure',
    description: 'Complete nail care and polish service',
    type: 'nail_care',
    price: 45,
    duration: 45,
    image_url: 'https://via.placeholder.com/300x200?text=Manicure'
  },
  {
    id: 5,
    name: 'Massage Therapy',
    description: 'Relaxing full body massage therapy',
    type: 'massage',
    price: 100,
    duration: 90,
    image_url: 'https://via.placeholder.com/300x200?text=Massage'
  },
  {
    id: 6,
    name: 'Hair Styling',
    description: 'Special occasion hair styling and updo',
    type: 'hair_styling',
    price: 90,
    duration: 75,
    image_url: 'https://via.placeholder.com/300x200?text=Styling'
  }
];

export const mockEvents = [
  // January 2024 Events
  { date: 3, title: 'Team Meeting', time: '10:00 - 11:00', color: 'pink' },
  { date: 3, title: 'Client Consultation', time: '14:00 - 15:00', color: 'blue' },
  { date: 5, title: 'Hair Styling Workshop', time: '09:00 - 12:00', color: 'purple' },
  { date: 7, title: 'Developer Meetup', time: '10:00 - 11:00', color: 'emerald' },
  { date: 7, title: 'Staff Training', time: '15:00 - 17:00', color: 'orange' },
  { date: 9, title: 'Today', time: '', color: 'indigo' },
  { date: 9, title: 'Appointment Review', time: '11:00 - 12:00', color: 'red' },
  { date: 12, title: 'Salon Maintenance', time: '08:00 - 10:00', color: 'yellow' },
  { date: 15, title: 'New Product Launch', time: '13:00 - 14:30', color: 'teal' },
  { date: 15, title: 'Client Feedback Session', time: '16:00 - 17:00', color: 'cyan' },
  { date: 18, title: 'Hair Show Preparation', time: '09:00 - 18:00', color: 'rose' },
  { date: 19, title: 'Developer Meetup', time: '10:00 - 11:00', color: 'sky' },
  { date: 19, title: 'Equipment Check', time: '14:00 - 15:00', color: 'lime' },
  { date: 22, title: 'Staff Meeting', time: '10:00 - 11:30', color: 'violet' },
  { date: 22, title: 'Inventory Check', time: '15:00 - 16:00', color: 'amber' },
  { date: 25, title: 'Client Appreciation Day', time: '10:00 - 17:00', color: 'fuchsia' },
  { date: 25, title: 'Special Offers Launch', time: '09:00 - 10:00', color: 'emerald' },
  { date: 28, title: 'Monthly Review', time: '14:00 - 16:00', color: 'indigo' },
  { date: 30, title: 'Equipment Upgrade', time: '08:00 - 12:00', color: 'slate' },
  { date: 30, title: 'Staff Training Session', time: '13:00 - 15:00', color: 'green' },
];


// Helper function to get events for a specific date
export const getEventsForDate = (year, month, day) => {
  return mockEvents.filter(event => event.date === day);
};

// Helper function to get the first event for a date (when multiple events exist)
export const getFirstEventForDate = (year, month, day) => {
  const events = getEventsForDate(year, month, day);
  return events.length > 0 ? events[0] : null;
};
