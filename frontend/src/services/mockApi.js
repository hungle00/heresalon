// Mock API service for testing without backend
class MockApiService {
  constructor() {
    this.token = localStorage.getItem('auth_token');
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

  // Mock authentication methods
  async register(email, password, username) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mockUser = {
      id: Date.now(),
      username: username || email.split('@')[0],
      email: email,
      role: 'customer',
      created_at: new Date().toISOString()
    };

    const mockToken = `mock_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    this.setToken(mockToken);
    
    return {
      message: 'User registered successfully',
      token: mockToken,
      user: mockUser
    };
  }

  async login(email, password) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mockUser = {
      id: Date.now(),
      username: email.split('@')[0],
      email: email,
      role: 'customer',
      created_at: new Date().toISOString()
    };

    const mockToken = `mock_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    this.setToken(mockToken);
    
    return {
      message: 'Login successful',
      token: mockToken,
      user: mockUser
    };
  }

  async logout() {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    this.setToken(null);
    return { message: 'Logout successful' };
  }

  async getCurrentUser() {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    if (!this.token) {
      throw new Error('No token found');
    }

    // Extract user info from token (mock implementation)
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      role: 'customer',
      created_at: new Date().toISOString()
    };

    return mockUser;
  }

  // Mock other API methods
  async getStaff() {
    await new Promise(resolve => setTimeout(resolve, 500));
    return [
      { id: 1, name: 'John Doe', specialty: 'Hair Styling' },
      { id: 2, name: 'Jane Smith', specialty: 'Makeup' }
    ];
  }

  async getSalons() {
    await new Promise(resolve => setTimeout(resolve, 500));
    return [
      { id: 1, name: 'Beauty Salon', location: 'Downtown' },
      { id: 2, name: 'Hair Studio', location: 'Uptown' }
    ];
  }

  async getServices() {
    await new Promise(resolve => setTimeout(resolve, 500));
    return [
      { id: 1, name: 'Haircut', price: 50 },
      { id: 2, name: 'Manicure', price: 30 }
    ];
  }
}

export default new MockApiService();
