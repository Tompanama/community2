import { Outlet } from 'react-router-dom'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import logo from '../assets/logo.png'

const AuthLayout = () => {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background">
      <div className="w-full max-w-md p-8 space-y-8 bg-card rounded-lg shadow-lg">
        <div className="flex flex-col items-center">
          <img src={logo} alt="CommunityAI Logo" className="h-16 mb-4" />
          <h2 className="text-2xl font-bold text-center text-foreground">
            CommunityAI
          </h2>
          <p className="text-sm text-muted-foreground text-center">
            Gestion communautaire avec assistant IA intégré
          </p>
        </div>
        
        {/* Outlet renders the child route components */}
        <Outlet />
      </div>
      
      <footer className="mt-8 text-center text-sm text-muted-foreground">
        <p>© 2025 CommunityAI. Tous droits réservés.</p>
      </footer>
    </div>
  )
}

export default AuthLayout

