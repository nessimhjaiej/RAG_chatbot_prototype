# Modern Light Theme Conversion Prompt for React + Vite Projects

You are a full-stack developer tasked with converting a Streamlit application to a modern React + Vite application with a light theme. Follow these guidelines precisely.

## Core Objectives

1. Migrate Streamlit backend logic to Node.js/Express or keep as Python backend with API
2. Build React + Vite frontend with modern light theme
3. Maintain all existing functionality from Streamlit app
4. Improve visual hierarchy and user experience
5. Apply contemporary design patterns and component architecture
6. Ensure accessibility and responsive design

## Project Structure

```
project-root/
├── frontend/                 # React + Vite app
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── styles/          # CSS/Tailwind styles
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   ├── api/             # API client functions
│   │   └── App.jsx
│   ├── public/
│   ├── vite.config.js
│   └── package.json
├── backend/                  # Node.js/Express API (or Python FastAPI)
│   ├── routes/              # API endpoints
│   ├── controllers/         # Business logic
│   ├── models/              # Data models
│   └── server.js            # Express server
└── README.md
```

## Modern Light Theme Specification

### Color Palette (Use these exact hex values)

**Base Colors:**
- Page Background: `#f5f5f7`
- Surface/Card Background: `#ffffff`
- Primary Brand: `#4f46e5` (Indigo)
- Primary Soft Background: `#eef2ff`
- Secondary: `#6366f1`

**Text Colors:**
- Primary Text: `#111827` (Near-black)
- Secondary Text: `#6b7280` (Medium gray)
- Muted Text: `#9ca3af` (Light gray)
- Text on Primary: `#ffffff` (White)

**Utility Colors:**
- Success: `#22c55e` (Green)
- Warning: `#f59e0b` (Amber)
- Danger/Error: `#ef4444` (Red)
- Info: `#06b6d4` (Cyan)

**Borders & Dividers:**
- Subtle Border: `#e5e7eb` (Light gray)
- Strong Border: `#d1d5db` (Medium gray)
- Hover Border: `#bfdbfe` (Light blue)

## Setup Instructions

### Step 1: Create React + Vite Project

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
```

### Step 2: Install Dependencies

```bash
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 3: Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-page': '#f5f5f7',
        'bg-surface': '#ffffff',
        'text-primary': '#111827',
        'text-secondary': '#6b7280',
        'text-muted': '#9ca3af',
        'accent': '#4f46e5',
        'accent-soft': '#eef2ff',
        'success': '#22c55e',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#06b6d4',
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '20px',
        '2xl': '24px',
        '3xl': '32px',
      },
      borderRadius: {
        'sm': '6px',
        'md': '12px',
        'lg': '16px',
        'full': '999px',
      },
      boxShadow: {
        'subtle': '0 4px 6px rgba(0, 0, 0, 0.07)',
        'medium': '0 10px 15px rgba(0, 0, 0, 0.1)',
        'large': '0 20px 25px rgba(0, 0, 0, 0.15)',
      },
    },
  },
  plugins: [],
}
```

Update `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-bg-page text-text-primary font-sans;
  }
  
  h1 {
    @apply text-4xl font-semibold mb-4 tracking-tight;
  }
  
  h2 {
    @apply text-2xl font-semibold mb-3 mt-6 tracking-tight;
  }
  
  h3 {
    @apply text-xl font-semibold mb-2;
  }
  
  p {
    @apply text-text-secondary mb-3 leading-relaxed;
  }
}

@layer components {
  .btn {
    @apply px-5 py-2 rounded-full font-medium transition-all duration-200 cursor-pointer;
  }
  
  .btn-primary {
    @apply bg-accent text-white hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-200;
  }
  
  .btn-secondary {
    @apply bg-accent-soft text-accent hover:bg-indigo-100;
  }
  
  .btn-outline {
    @apply border border-border text-text-primary hover:bg-bg-page;
  }
  
  .card {
    @apply bg-bg-surface border border-border rounded-md p-4 shadow-subtle hover:shadow-medium transition-shadow;
  }
  
  .input {
    @apply w-full px-3 py-2 bg-bg-surface border border-border rounded-md text-text-primary focus:border-accent focus:ring-4 focus:ring-indigo-100 placeholder-text-muted;
  }
  
  .label {
    @apply block text-sm font-medium text-text-primary mb-2;
  }
}
```

## React Component Structure

### Layout Components

**App.jsx** (Main entry point):

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import './index.css';

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-bg-page">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 overflow-auto p-6">
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
```

**Header.jsx**:

```jsx
import React from 'react';

export default function Header() {
  return (
    <header className="sticky top-0 z-20 bg-bg-surface border-b border-border backdrop-blur-md bg-opacity-90">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-text-primary">My App</h1>
        <div className="flex items-center gap-4">
          <button className="px-4 py-2 text-text-secondary hover:text-text-primary">
            Profile
          </button>
          <button className="px-4 py-2 text-text-secondary hover:text-text-primary">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
```

**Sidebar.jsx**:

```jsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-bg-surface border-r border-border p-6 hidden md:block">
      <nav className="space-y-2">
        <Link 
          to="/" 
          className="block px-4 py-2 rounded-md text-text-primary hover:bg-bg-page"
        >
          🏠 Home
        </Link>
        <Link 
          to="/dashboard" 
          className="block px-4 py-2 rounded-md text-text-primary hover:bg-bg-page"
        >
          📊 Dashboard
        </Link>
        <Link 
          to="/settings" 
          className="block px-4 py-2 rounded-md text-text-primary hover:bg-bg-page"
        >
          ⚙️ Settings
        </Link>
      </nav>
    </aside>
  );
}
```

### Reusable Components

**Button.jsx**:

```jsx
export default function Button({ variant = 'primary', children, ...props }) {
  const variants = {
    primary: 'btn btn-primary',
    secondary: 'btn btn-secondary',
    outline: 'btn btn-outline',
  };
  
  return (
    <button className={variants[variant]} {...props}>
      {children}
    </button>
  );
}
```

**Card.jsx**:

```jsx
export default function Card({ title, children, ...props }) {
  return (
    <div className="card" {...props}>
      {title && <h3 className="text-lg font-semibold mb-4 text-text-primary">{title}</h3>}
      {children}
    </div>
  );
}
```

**Input.jsx**:

```jsx
export default function Input({ label, ...props }) {
  return (
    <div>
      {label && <label className="label">{label}</label>}
      <input className="input" {...props} />
    </div>
  );
}
```

**Metric.jsx** (Replacement for st.metric):

```jsx
export default function Metric({ label, value, delta, trend = 'up' }) {
  const deltaColor = trend === 'up' ? 'text-green-600' : 'text-red-600';
  
  return (
    <div className="card">
      <p className="text-text-muted text-sm mb-2">{label}</p>
      <p className="text-3xl font-bold text-text-primary mb-2">{value}</p>
      {delta && <p className={`text-sm ${deltaColor}`}>{delta}</p>}
    </div>
  );
}
```

**Alert.jsx**:

```jsx
export default function Alert({ type = 'info', children }) {
  const types = {
    success: 'bg-green-50 border-success text-green-800',
    error: 'bg-red-50 border-error text-red-800',
    warning: 'bg-amber-50 border-warning text-amber-800',
    info: 'bg-cyan-50 border-info text-cyan-800',
  };
  
  return (
    <div className={`border rounded-md p-4 ${types[type]}`}>
      {children}
    </div>
  );
}
```

## API Integration

**src/api/client.js**:

```javascript
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Example endpoints - replace with your actual API calls
  getMetrics: () => client.get('/metrics'),
  getAnalytics: () => client.get('/analytics'),
  updateSettings: (data) => client.post('/settings', data),
};

export default client;
```

## Example Pages

**src/pages/Dashboard.jsx**:

```jsx
import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import Metric from '../components/Metric';
import { api } from '../api/client';

export default function Dashboard() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    api.getMetrics()
      .then(res => setMetrics(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <p>Loading...</p>;
  
  return (
    <div>
      <h1>📊 Analytics Dashboard</h1>
      <p className="text-text-secondary mb-6">Welcome to your dashboard</p>
      
      <div className="grid grid-cols-4 gap-4 mb-8">
        <Metric label="Users" value="1,234" delta="+5%" />
        <Metric label="Revenue" value="$45K" delta="+12%" />
        <Metric label="Conversion" value="3.21%" delta="-0.5%" trend="down" />
        <Metric label="Avg Order" value="$125" delta="+2%" />
      </div>
      
      <div className="grid grid-cols-2 gap-6">
        <Card title="Chart Section">
          <p className="text-text-muted">Chart placeholder</p>
        </Card>
        <Card title="Summary">
          <p className="text-text-muted">Summary content</p>
        </Card>
      </div>
    </div>
  );
}
```

## Backend Setup (Node.js/Express)

**server.js**:

```javascript
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

// API Routes
app.get('/api/metrics', (req, res) => {
  res.json({
    users: 1234,
    revenue: 45000,
    conversion: 3.21,
  });
});

app.get('/api/analytics', (req, res) => {
  res.json({
    data: [1, 2, 3, 4, 5],
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Development Workflow

### Step 1: Start Backend
```bash
cd backend
npm install
npm run dev
```

### Step 2: Start Frontend (Vite dev server)
```bash
cd frontend
npm run dev
```

### Step 3: Build for Production
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
npm run build
```

## Vite Configuration

**vite.config.js**:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  }
})
```

## Migration Checklist

- [ ] React + Vite project created and configured
- [ ] Tailwind CSS installed and configured
- [ ] Color palette tokens defined in Tailwind config
- [ ] Reusable components created (Button, Card, Input, Metric, Alert)
- [ ] Layout components built (Header, Sidebar, App)
- [ ] React Router configured for multi-page navigation
- [ ] API client setup with axios
- [ ] Backend API endpoints created
- [ ] Pages migrated from Streamlit to React
- [ ] Form components implemented
- [ ] Data fetching with useEffect and states
- [ ] Error handling and loading states
- [ ] Responsive design tested
- [ ] Accessibility checks passed
- [ ] Light theme colors consistently applied
- [ ] Production build optimized

## Performance Optimization

1. **Code Splitting**: Use React.lazy() for route-based code splitting
2. **Image Optimization**: Use responsive images with srcset
3. **Caching**: Implement HTTP caching headers
4. **Minification**: Vite handles this automatically
5. **Bundle Analysis**: Use `vite-plugin-visualizer`

## Deployment Options

**Netlify/Vercel (Frontend)**:
```bash
npm run build
# Deploy the dist/ folder
```

**Heroku/Railway (Backend)**:
```bash
git push heroku main
```

**Docker**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 5000
CMD ["npm", "start"]
```

## Quality Checklist

- [ ] All Streamlit functionality replicated in React
- [ ] Light theme colors applied throughout
- [ ] Components are reusable and maintainable
- [ ] Responsive design works on all screen sizes
- [ ] API calls properly handle errors and loading states
- [ ] Accessibility standards met (WCAG 2.1 AA)
- [ ] Performance optimized (Lighthouse 90+)
- [ ] Mobile navigation implemented
- [ ] Forms validated client and server-side
- [ ] User feedback (loading, success, error states)

---

## How to Use This Prompt

1. Copy this entire prompt
2. Provide it to your AI agent along with your Streamlit project code
3. Ask: "Migrate my Streamlit app to React + Vite with modern light theme"
4. The agent should:
   - Create React + Vite project structure
   - Set up Tailwind CSS with light theme colors
   - Build reusable components matching Streamlit functionality
   - Create pages and layouts
   - Set up backend API
   - Configure routing and state management
5. Test locally: `npm run dev` (frontend), `npm run dev` (backend)
6. Deploy to production using Netlify/Vercel + Railway/Heroku

Good luck with your React migration! 🚀