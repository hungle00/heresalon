import mockApi from './mockApi';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('auth_token');
    this.useMockApi = !API_BASE_URL || process.env.REACT_APP_USE_MOCK === 'true';
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  getAuthHeaders() {
    return this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
  }

  async request(endpoint, options = {}) {
    // Use mock API if no backend URL or mock mode enabled
    if (this.useMockApi) {
      throw new Error('Use specific mock methods instead of generic request');
    }

    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication API
  async register(email, password, username) {
    if (this.useMockApi) {
      return await mockApi.register(email, password, username);
    }

    const data = await this.request('/api/auth/register/', {
      method: 'POST',
      body: JSON.stringify({ email, password, username })
    });
    if (data.token) {
      this.setToken(data.token);
    }
    return data;
  }

  async login(email, password) {
    if (this.useMockApi) {
      return await mockApi.login(email, password);
    }

    const data = await this.request('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    if (data.token) {
      this.setToken(data.token);
    }
    return data;
  }

  async logout() {
    if (this.useMockApi) {
      return await mockApi.logout();
    }

    try {
      await this.request('/api/auth/logout/', {
        method: 'POST'
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.setToken(null);
    }
  }

  async getCurrentUser() {
    if (this.useMockApi) {
      return await mockApi.getCurrentUser();
    }

    return this.request('/api/auth/me/');
  }

  // Staff API
  async getStaff() {
    if (this.useMockApi) {
      return await mockApi.getStaff();
    }
    return this.request('/api/staff/');
  }

  async getStaffById(id) {
    if (this.useMockApi) {
      const staff = await mockApi.getStaff();
      return staff.find(s => s.id === parseInt(id));
    }
    return this.request(`/api/staff/${id}/`);
  }

  // Salon API
  async getSalons() {
    if (this.useMockApi) {
      return await mockApi.getSalons();
    }
    return this.request('/api/salons/');
  }

  async getSalonById(id) {
    if (this.useMockApi) {
      const salons = await mockApi.getSalons();
      return salons.find(s => s.id === parseInt(id));
    }
    return this.request(`/api/salons/${id}/`);
  }

  // Services API
  async getServices() {
    if (this.useMockApi) {
      return await mockApi.getServices();
    }
    return this.request('/api/services/');
  }

  async getServiceById(id) {
    if (this.useMockApi) {
      const services = await mockApi.getServices();
      return services.find(s => s.id === parseInt(id));
    }
    return this.request(`/api/services/${id}/`);
  }

  // Appointments API
  async getAppointments() {
    if (this.useMockApi) {
      return [];
    }
    return this.request('/api/appointments/');
  }

  async getAppointmentById(id) {
    if (this.useMockApi) {
      return null;
    }
    return this.request(`/api/appointments/${id}/`);
  }
}

export default new ApiService();
