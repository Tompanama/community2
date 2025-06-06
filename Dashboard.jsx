import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

// Import UI components
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card'

// Import icons
import {
  BarChart3,
  Calendar,
  MessageSquareText,
  PenSquare,
  Share2,
  TrendingUp,
  Users,
  Clock,
  AlertCircle
} from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    postsScheduled: 0,
    postsPublished: 0,
    totalEngagement: 0,
    totalFollowers: 0
  })
  const [isLoading, setIsLoading] = useState(true)

  // Mock data for upcoming posts
  const upcomingPosts = [
    {
      id: 1,
      title: 'Lancement de notre nouvelle collection',
      platform: 'Instagram',
      scheduledFor: new Date(Date.now() + 3600000), // 1 hour from now
      status: 'scheduled'
    },
    {
      id: 2,
      title: 'Conseils pour optimiser votre présence en ligne',
      platform: 'LinkedIn',
      scheduledFor: new Date(Date.now() + 7200000), // 2 hours from now
      status: 'scheduled'
    },
    {
      id: 3,
      title: 'Tutoriel vidéo : comment utiliser notre application',
      platform: 'YouTube',
      scheduledFor: new Date(Date.now() + 86400000), // 24 hours from now
      status: 'draft'
    }
  ]

  // Mock data for recent activities
  const recentActivities = [
    {
      id: 1,
      type: 'comment',
      platform: 'Instagram',
      content: 'Marie a commenté votre publication',
      time: '2 min'
    },
    {
      id: 2,
      type: 'like',
      platform: 'Facebook',
      content: '15 personnes ont aimé votre publication',
      time: '30 min'
    },
    {
      id: 3,
      type: 'share',
      platform: 'LinkedIn',
      content: 'Thomas a partagé votre article',
      time: '1h'
    },
    {
      id: 4,
      type: 'message',
      platform: 'Instagram',
      content: 'Nouveau message de Sophie',
      time: '3h'
    }
  ]

  // Mock data for AI suggestions
  const aiSuggestions = [
    {
      id: 1,
      title: 'Optimisez vos hashtags',
      description: 'Utilisez ces hashtags pour augmenter votre visibilité',
      action: 'Voir les suggestions'
    },
    {
      id: 2,
      title: 'Meilleur moment pour publier',
      description: 'Jeudi 18h-20h est le moment optimal pour votre audience',
      action: 'Planifier un post'
    },
    {
      id: 3,
      title: 'Idées de contenu',
      description: '3 nouvelles idées basées sur vos performances récentes',
      action: 'Explorer les idées'
    }
  ]

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // In a real app, we would fetch data from the API
        // For now, we'll just simulate a delay and use mock data
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        setStats({
          postsScheduled: 5,
          postsPublished: 28,
          totalEngagement: 1243,
          totalFollowers: 5280
        })
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  // Format date for upcoming posts
  const formatScheduledTime = (date) => {
    return new Date(date).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // Format date for upcoming posts (day)
  const formatScheduledDay = (date) => {
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    
    if (date.toDateString() === today.toDateString()) {
      return "Aujourd'hui"
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return "Demain"
    } else {
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long'
      })
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Bienvenue, {user?.name || 'Utilisateur'} ! Voici un aperçu de votre activité.
        </p>
      </div>

      {/* Stats cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Posts programmés</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{isLoading ? '...' : stats.postsScheduled}</div>
            <p className="text-xs text-muted-foreground">
              +2 depuis la semaine dernière
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Posts publiés</CardTitle>
            <PenSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{isLoading ? '...' : stats.postsPublished}</div>
            <p className="text-xs text-muted-foreground">
              +8 depuis le mois dernier
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Engagement total</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{isLoading ? '...' : stats.totalEngagement}</div>
            <p className="text-xs text-muted-foreground">
              +19% depuis le mois dernier
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Abonnés</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{isLoading ? '...' : stats.totalFollowers}</div>
            <p className="text-xs text-muted-foreground">
              +7% depuis le mois dernier
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Upcoming posts */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Posts à venir</CardTitle>
            <CardDescription>
              Vos prochaines publications programmées
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {upcomingPosts.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-4 text-center">
                <Calendar className="h-10 w-10 text-muted-foreground mb-2" />
                <p className="text-muted-foreground">Aucun post programmé</p>
              </div>
            ) : (
              upcomingPosts.map(post => (
                <div key={post.id} className="flex items-start space-x-4">
                  <div className="min-w-10 min-h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Clock className="h-5 w-5 text-primary" />
                  </div>
                  <div className="space-y-1">
                    <p className="font-medium">{post.title}</p>
                    <div className="flex items-center text-sm">
                      <span className="text-muted-foreground">{post.platform}</span>
                      <span className="mx-2 text-muted-foreground">•</span>
                      <span className="text-muted-foreground">
                        {formatScheduledDay(post.scheduledFor)} à {formatScheduledTime(post.scheduledFor)}
                      </span>
                    </div>
                    <div className="flex items-center">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        post.status === 'scheduled' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {post.status === 'scheduled' ? 'Programmé' : 'Brouillon'}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full" asChild>
              <Link to="/calendar">Voir le calendrier</Link>
            </Button>
          </CardFooter>
        </Card>

        {/* Recent activities */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Activités récentes</CardTitle>
            <CardDescription>
              Dernières interactions sur vos réseaux sociaux
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentActivities.map(activity => (
              <div key={activity.id} className="flex items-start space-x-4">
                <div className="min-w-10 min-h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  {activity.type === 'comment' && <MessageSquareText className="h-5 w-5 text-primary" />}
                  {activity.type === 'like' && <TrendingUp className="h-5 w-5 text-primary" />}
                  {activity.type === 'share' && <Share2 className="h-5 w-5 text-primary" />}
                  {activity.type === 'message' && <MessageSquareText className="h-5 w-5 text-primary" />}
                </div>
                <div className="space-y-1">
                  <p className="font-medium">{activity.content}</p>
                  <div className="flex items-center text-sm">
                    <span className="text-muted-foreground">{activity.platform}</span>
                    <span className="mx-2 text-muted-foreground">•</span>
                    <span className="text-muted-foreground">Il y a {activity.time}</span>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full" asChild>
              <Link to="/analytics">Voir toutes les activités</Link>
            </Button>
          </CardFooter>
        </Card>

        {/* AI suggestions */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Suggestions de l'IA</CardTitle>
            <CardDescription>
              Recommandations personnalisées pour optimiser votre stratégie
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {aiSuggestions.map(suggestion => (
              <div key={suggestion.id} className="flex items-start space-x-4">
                <div className="min-w-10 min-h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <AlertCircle className="h-5 w-5 text-primary" />
                </div>
                <div className="space-y-1">
                  <p className="font-medium">{suggestion.title}</p>
                  <p className="text-sm text-muted-foreground">
                    {suggestion.description}
                  </p>
                  <Button variant="link" className="p-0 h-auto" asChild>
                    <Link to="/ai-assistant">{suggestion.action}</Link>
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full" asChild>
              <Link to="/ai-assistant">Consulter l'assistant IA</Link>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

