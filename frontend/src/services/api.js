const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Staff API
  async getStaff() {
    return this.request('/api/staff/');
  }

  async getStaffById(id) {
    return this.request(`/api/staff/${id}/`);
  }

  // Salon API
  async getSalons() {
    return this.request('/api/salons/');
  }

  async getSalonById(id) {
    return this.request(`/api/salons/${id}/`);
  }

  // Services API
  async getServices() {
    return this.request('/api/services/');
  }

  async getServiceById(id) {
    return this.request(`/api/services/${id}/`);
  }

  // Appointments API
  async getAppointments() {
    return this.request('/api/appointments/');
  }

  async getAppointmentById(id) {
    return this.request(`/api/appointments/${id}/`);
  }
}

export default new ApiService();
