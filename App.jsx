import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'

// Layouts
import AuthLayout from './layouts/AuthLayout'
import DashboardLayout from './layouts/DashboardLayout'

// Auth pages
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import ForgotPassword from './pages/auth/ForgotPassword'

// Dashboard pages
import Dashboard from './pages/dashboard/Dashboard'
import Calendar from './pages/calendar/Calendar'
import ContentCreator from './pages/content/ContentCreator'
import ContentLibrary from './pages/content/ContentLibrary'
import AIAssistant from './pages/ai/AIAssistant'

// Protected route component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Auth routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
          </Route>
          
          {/* Dashboard routes */}
          <Route element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }>
            <Route path="/" element={<Dashboard />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/content/create" element={<ContentCreator />} />
            <Route path="/content/library" element={<ContentLibrary />} />
            <Route path="/ai-assistant" element={<AIAssistant />} />
            
            {/* Placeholder routes for future implementation */}
            <Route path="/analytics" element={<div className="p-4">Page Analytique en cours de développement</div>} />
            <Route path="/social-accounts" element={<div className="p-4">Page Comptes Sociaux en cours de développement</div>} />
            <Route path="/organizations" element={<div className="p-4">Page Organisations en cours de développement</div>} />
            <Route path="/settings" element={<div className="p-4">Page Paramètres en cours de développement</div>} />
          </Route>
          
          {/* Redirect to login for unknown routes */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

