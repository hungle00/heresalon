# Salon Management Frontend

A modern React frontend for the salon management system, built with React Router and Tailwind CSS.

## Tech Stack

- **React 18**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Yarn**: Package manager for dependency management

## Quick Start

### Prerequisites

- Node.js 16+ (recommended: Node.js 20+)
- Yarn package manager

### Installation

1. **Install dependencies**:
   ```bash
   yarn install
   ```

2. **Start development server**:
   ```bash
   yarn start
   ```

3. **Open in browser**:
   Navigate to `http://localhost:3000`

### Available Scripts

- `yarn start` - Start development server
- `yarn build` - Build for production
- `yarn test` - Run tests
- `yarn eject` - Eject from Create React App

## API Integration

### Backend Connection
The frontend is configured to connect to the Flask backend running on port 8080:

```javascript
// API Base URL
const API_BASE_URL = 'http://localhost:8080';

// Available Endpoints
GET /api/staff/          # List all staff
GET /api/staff/:id/      # Get staff by ID
GET /api/salons/         # List all salons
GET /api/services/       # List all services
GET /api/appointments/   # List all appointments
```

### Mock Data
When the backend is not available, the application automatically falls back to mock data:

- **Sarah Johnson** - Senior Hair Stylist (8 years experience)
- **Mike Chen** - Barber (5 years experience)
- **Emma Davis** - Beauty Specialist (6 years experience)

