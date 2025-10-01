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

## Mock Mode Setup

This React app can run in mock mode for testing without a backend server.

### How to Enable Mock Mode
Create a `.env.local` file in the frontend directory:
```
REACT_APP_USE_MOCK=true
REACT_APP_API_URL=
```

Or the app automatically uses mock mode when:
- No `REACT_APP_API_URL` is set
- `REACT_APP_USE_MOCK=true` is set

## Mock Mode Features

### Authentication
- **Any email/password combination works**
- Users are automatically logged in
- Mock JWT tokens are generated
- User data is stored in localStorage

### Mock Data
- Staff members
- Salon information
- Services
- Appointments (empty array)

## Testing Login

1. Click the "Login" button
2. Enter any email (e.g., `test@example.com`)
3. Enter any password (e.g., `password123`)
4. Click "Login" - you'll be automatically signed in!

## Switching to Real Backend

To use the real backend:
1. Set `REACT_APP_API_URL=http://localhost:8080` in `.env.local`
2. Set `REACT_APP_USE_MOCK=false` or remove it
3. Make sure the backend server is running


