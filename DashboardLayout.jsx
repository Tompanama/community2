import { useState, useEffect } from 'react'
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import logo from '../assets/logo.png'

// Import icons
import {
  LayoutDashboard,
  Calendar,
  PenSquare,
  BarChart3,
  Settings,
  MessageSquareText,
  Share2,
  Building2,
  FolderOpen,
  Menu,
  X,
  Bell,
  User,
  LogOut,
  ChevronDown
} from 'lucide-react'

const DashboardLayout = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false)

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false)
  }, [location.pathname])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  // Navigation items
  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard className="h-5 w-5" /> },
    { path: '/calendar', label: 'Calendrier', icon: <Calendar className="h-5 w-5" /> },
    { 
      label: 'Contenu', 
      icon: <PenSquare className="h-5 w-5" />,
      children: [
        { path: '/content/create', label: 'Créer du contenu' },
        { path: '/content/library', label: 'Bibliothèque' }
      ]
    },
    { path: '/analytics', label: 'Analytique', icon: <BarChart3 className="h-5 w-5" /> },
    { path: '/ai-assistant', label: 'Assistant IA', icon: <MessageSquareText className="h-5 w-5" /> },
    { path: '/social-accounts', label: 'Comptes sociaux', icon: <Share2 className="h-5 w-5" /> },
    { path: '/organizations', label: 'Organisations', icon: <Building2 className="h-5 w-5" /> },
    { path: '/settings', label: 'Paramètres', icon: <Settings className="h-5 w-5" /> }
  ]

  // Mock notifications
  const notifications = [
    { id: 1, title: 'Nouveau commentaire', message: 'Marie a commenté votre publication Instagram', time: '2 min' },
    { id: 2, title: 'Publication programmée', message: 'Votre publication a été publiée sur Facebook', time: '1h' },
    { id: 3, title: 'Suggestion IA', message: 'L\'IA a généré de nouvelles idées de contenu', time: '3h' }
  ]

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top navigation bar */}
      <header className="bg-card border-b border-border h-16 flex items-center justify-between px-4 lg:px-6">
        <div className="flex items-center">
          {/* Mobile menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden mr-2 p-2 rounded-md hover:bg-muted"
          >
            {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
          
          {/* Logo */}
          <div className="flex items-center">
            <img src={logo} alt="CommunityAI Logo" className="h-8 w-8" />
            <span className="ml-2 text-lg font-semibold hidden sm:block">CommunityAI</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => {
                setIsNotificationsOpen(!isNotificationsOpen)
                setIsUserMenuOpen(false)
              }}
              className="p-2 rounded-md hover:bg-muted relative"
            >
              <Bell className="h-5 w-5" />
              <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-primary"></span>
            </button>
            
            {/* Notifications dropdown */}
            {isNotificationsOpen && (
              <div className="absolute right-0 mt-2 w-80 bg-card rounded-md shadow-lg border border-border z-50">
                <div className="p-3 border-b border-border">
                  <h3 className="font-semibold">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map(notification => (
                    <div key={notification.id} className="p-3 border-b border-border hover:bg-muted/50 cursor-pointer">
                      <div className="flex justify-between">
                        <h4 className="font-medium">{notification.title}</h4>
                        <span className="text-xs text-muted-foreground">{notification.time}</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{notification.message}</p>
                    </div>
                  ))}
                </div>
                <div className="p-2 text-center border-t border-border">
                  <button className="text-sm text-primary hover:underline">
                    Voir toutes les notifications
                  </button>
                </div>
              </div>
            )}
          </div>
          
          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => {
                setIsUserMenuOpen(!isUserMenuOpen)
                setIsNotificationsOpen(false)
              }}
              className="flex items-center space-x-2 p-2 rounded-md hover:bg-muted"
            >
              <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
                <User className="h-5 w-5" />
              </div>
              <span className="hidden md:block">{user?.name || 'Utilisateur'}</span>
              <ChevronDown className="h-4 w-4" />
            </button>
            
            {/* User dropdown */}
            {isUserMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-card rounded-md shadow-lg border border-border z-50">
                <div className="p-3 border-b border-border">
                  <p className="font-semibold">{user?.name || 'Utilisateur'}</p>
                  <p className="text-xs text-muted-foreground">{user?.email || 'utilisateur@example.com'}</p>
                </div>
                <div className="p-1">
                  <button
                    onClick={() => navigate('/settings')}
                    className="w-full text-left px-3 py-2 hover:bg-muted rounded-md flex items-center"
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    Paramètres
                  </button>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-3 py-2 hover:bg-muted rounded-md flex items-center text-destructive"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    Déconnexion
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>
      
      <div className="flex flex-1">
        {/* Sidebar navigation - Mobile */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-40 lg:hidden">
            <div className="fixed inset-0 bg-background/80 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)}></div>
            <nav className="fixed top-0 left-0 bottom-0 w-3/4 max-w-xs bg-sidebar border-r border-sidebar-border p-4 overflow-y-auto z-50">
              <div className="flex items-center mb-8">
                <img src={logo} alt="CommunityAI Logo" className="h-8 w-8" />
                <span className="ml-2 text-lg font-semibold">CommunityAI</span>
                <button
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="ml-auto p-2 rounded-md hover:bg-sidebar-accent"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              
              <div className="space-y-1">
                {navItems.map((item, index) => (
                  item.children ? (
                    <div key={index} className="mb-2">
                      <div className="flex items-center px-3 py-2 text-sidebar-foreground">
                        {item.icon}
                        <span className="ml-3">{item.label}</span>
                      </div>
                      <div className="ml-6 mt-1 space-y-1">
                        {item.children.map((child, childIndex) => (
                          <NavLink
                            key={childIndex}
                            to={child.path}
                            className={({ isActive }) =>
                              `block px-3 py-2 rounded-md ${
                                isActive
                                  ? 'bg-sidebar-primary text-sidebar-primary-foreground'
                                  : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                              }`
                            }
                          >
                            {child.label}
                          </NavLink>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <NavLink
                      key={index}
                      to={item.path}
                      className={({ isActive }) =>
                        `flex items-center px-3 py-2 rounded-md ${
                          isActive
                            ? 'bg-sidebar-primary text-sidebar-primary-foreground'
                            : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                        }`
                      }
                    >
                      {item.icon}
                      <span className="ml-3">{item.label}</span>
                    </NavLink>
                  )
                ))}
              </div>
            </nav>
          </div>
        )}
        
        {/* Sidebar navigation - Desktop */}
        <nav className="hidden lg:block w-64 bg-sidebar border-r border-sidebar-border p-4">
          <div className="space-y-1">
            {navItems.map((item, index) => (
              item.children ? (
                <div key={index} className="mb-2">
                  <div className="flex items-center px-3 py-2 text-sidebar-foreground">
                    {item.icon}
                    <span className="ml-3">{item.label}</span>
                  </div>
                  <div className="ml-6 mt-1 space-y-1">
                    {item.children.map((child, childIndex) => (
                      <NavLink
                        key={childIndex}
                        to={child.path}
                        className={({ isActive }) =>
                          `block px-3 py-2 rounded-md ${
                            isActive
                              ? 'bg-sidebar-primary text-sidebar-primary-foreground'
                              : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                          }`
                        }
                      >
                        {child.label}
                      </NavLink>
                    ))}
                  </div>
                </div>
              ) : (
                <NavLink
                  key={index}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center px-3 py-2 rounded-md ${
                      isActive
                        ? 'bg-sidebar-primary text-sidebar-primary-foreground'
                        : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                    }`
                  }
                >
                  {item.icon}
                  <span className="ml-3">{item.label}</span>
                </NavLink>
              )
            ))}
          </div>
        </nav>
        
        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout

