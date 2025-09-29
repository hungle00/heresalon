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
];

export const mockServices = [
  {
    id: 1,
    name: 'Hair Cut & Style',
    description: 'Professional haircut and styling service',
    type: 'hair_cut',
    price: 250000,
    image_url: 'https://via.placeholder.com/300x200?text=Hair+Cut'
  },
  {
    id: 2,
    name: 'Hair Coloring',
    description: 'Full hair coloring service with premium products',
    type: 'hair_color',
    price: 450000,
    image_url: 'https://via.placeholder.com/300x200?text=Hair+Color'
  },
  {
    id: 3,
    name: 'Facial Treatment',
    description: 'Deep cleansing and moisturizing facial treatment',
    type: 'facial',
    price: 300000,
    image_url: 'https://via.placeholder.com/300x200?text=Facial'
  },
  {
    id: 4,
    name: 'Manicure & Pedicure',
    description: 'Complete nail care and polish service',
    type: 'nail_care',
    price: 200000,
    image_url: 'https://via.placeholder.com/300x200?text=Manicure'
  },
  {
    id: 5,
    name: 'Massage Therapy',
    description: 'Relaxing full body massage therapy',
    type: 'massage',
    price: 400000,
    image_url: 'https://via.placeholder.com/300x200?text=Massage'
  },
  {
    id: 6,
    name: 'Hair Styling',
    description: 'Special occasion hair styling and updo',
    type: 'hair_styling',
    price: 350000,
    image_url: 'https://via.placeholder.com/300x200?text=Styling'
  }
];
