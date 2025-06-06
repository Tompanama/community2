import { useState } from 'react'

// Import UI components
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'

// Import icons
import { Calendar as CalendarIcon, List, Grid3X3, Plus, ChevronLeft, ChevronRight } from 'lucide-react'

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [view, setView] = useState('month')
  
  // Mock data for scheduled posts
  const scheduledPosts = [
    {
      id: 1,
      title: 'Lancement de notre nouvelle collection',
      platform: 'Instagram',
      scheduledFor: new Date(2025, 5, 8, 14, 30), // June 8, 2025, 14:30
      status: 'scheduled',
      content: 'Découvrez notre nouvelle collection printemps-été ! #NouvelleCollection'
    },
    {
      id: 2,
      title: 'Conseils pour optimiser votre présence en ligne',
      platform: 'LinkedIn',
      scheduledFor: new Date(2025, 5, 10, 10, 0), // June 10, 2025, 10:00
      status: 'scheduled',
      content: '5 conseils pour améliorer votre présence sur les réseaux sociaux professionnels'
    },
    {
      id: 3,
      title: 'Tutoriel vidéo : comment utiliser notre application',
      platform: 'YouTube',
      scheduledFor: new Date(2025, 5, 15, 16, 0), // June 15, 2025, 16:00
      status: 'draft',
      content: 'Tutoriel complet sur l\'utilisation de notre application'
    },
    {
      id: 4,
      title: 'Offre spéciale weekend',
      platform: 'Facebook',
      scheduledFor: new Date(2025, 5, 20, 9, 0), // June 20, 2025, 9:00
      status: 'scheduled',
      content: 'Profitez de notre offre spéciale ce weekend : -20% sur tout le site !'
    }
  ]
  
  // Get month name
  const getMonthName = (date) => {
    return date.toLocaleString('fr-FR', { month: 'long' })
  }
  
  // Get year
  const getYear = (date) => {
    return date.getFullYear()
  }
  
  // Navigate to previous month
  const previousMonth = () => {
    const newDate = new Date(currentDate)
    newDate.setMonth(newDate.getMonth() - 1)
    setCurrentDate(newDate)
  }
  
  // Navigate to next month
  const nextMonth = () => {
    const newDate = new Date(currentDate)
    newDate.setMonth(newDate.getMonth() + 1)
    setCurrentDate(newDate)
  }
  
  // Get days in month
  const getDaysInMonth = (date) => {
    const year = date.getFullYear()
    const month = date.getMonth()
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    
    const days = []
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i))
    }
    
    return days
  }
  
  // Get day of week (0 = Sunday, 1 = Monday, etc.)
  const getDayOfWeek = (date) => {
    return date.getDay()
  }
  
  // Get posts for a specific day
  const getPostsForDay = (day) => {
    return scheduledPosts.filter(post => {
      const postDate = new Date(post.scheduledFor)
      return (
        postDate.getDate() === day.getDate() &&
        postDate.getMonth() === day.getMonth() &&
        postDate.getFullYear() === day.getFullYear()
      )
    })
  }
  
  // Format time
  const formatTime = (date) => {
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  // Get platform color
  const getPlatformColor = (platform) => {
    switch (platform.toLowerCase()) {
      case 'instagram':
        return 'bg-purple-100 text-purple-800'
      case 'facebook':
        return 'bg-blue-100 text-blue-800'
      case 'linkedin':
        return 'bg-sky-100 text-sky-800'
      case 'twitter':
        return 'bg-blue-100 text-blue-800'
      case 'youtube':
        return 'bg-red-100 text-red-800'
      case 'tiktok':
        return 'bg-black text-white'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }
  
  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'bg-green-100 text-green-800'
      case 'draft':
        return 'bg-amber-100 text-amber-800'
      case 'published':
        return 'bg-blue-100 text-blue-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }
  
  // Render month view
  const renderMonthView = () => {
    const days = getDaysInMonth(currentDate)
    const firstDayOfMonth = getDayOfWeek(days[0])
    
    // Create array for calendar grid (6 rows x 7 columns)
    const calendarGrid = []
    let dayIndex = 0
    
    // Day names
    const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
    
    return (
      <div className="space-y-4">
        {/* Day names */}
        <div className="grid grid-cols-7 gap-1">
          {dayNames.map((day, index) => (
            <div key={index} className="text-center text-sm font-medium py-2">
              {day}
            </div>
          ))}
        </div>
        
        {/* Calendar grid */}
        <div className="grid grid-cols-7 gap-1">
          {/* Empty cells for days before the first day of the month */}
          {Array.from({ length: firstDayOfMonth }).map((_, index) => (
            <div key={`empty-${index}`} className="h-24 border border-border rounded-md bg-muted/30"></div>
          ))}
          
          {/* Days of the month */}
          {days.map((day, index) => {
            const postsForDay = getPostsForDay(day)
            const isToday = day.toDateString() === new Date().toDateString()
            
            return (
              <div
                key={index}
                className={`h-24 border border-border rounded-md p-1 overflow-hidden ${
                  isToday ? 'bg-primary/10 border-primary' : 'hover:bg-muted/50'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className={`text-sm font-medium ${isToday ? 'text-primary' : ''}`}>
                    {day.getDate()}
                  </span>
                  {postsForDay.length > 0 && (
                    <span className="text-xs bg-primary/20 text-primary px-1 rounded-full">
                      {postsForDay.length}
                    </span>
                  )}
                </div>
                
                <div className="space-y-1">
                  {postsForDay.slice(0, 2).map((post) => (
                    <div
                      key={post.id}
                      className="text-xs truncate p-1 rounded bg-card cursor-pointer hover:bg-muted"
                      title={post.title}
                    >
                      <div className="flex items-center">
                        <span className={`w-2 h-2 rounded-full mr-1 ${getPlatformColor(post.platform).split(' ')[0]}`}></span>
                        <span>{formatTime(post.scheduledFor)}</span>
                      </div>
                      <div className="truncate">{post.title}</div>
                    </div>
                  ))}
                  
                  {postsForDay.length > 2 && (
                    <div className="text-xs text-muted-foreground text-center">
                      +{postsForDay.length - 2} autres
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }
  
  // Render list view
  const renderListView = () => {
    // Sort posts by date
    const sortedPosts = [...scheduledPosts].sort((a, b) => a.scheduledFor - b.scheduledFor)
    
    return (
      <div className="space-y-4">
        {sortedPosts.map((post) => (
          <Card key={post.id} className="cursor-pointer hover:border-primary transition-colors">
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <div className="font-medium">{post.title}</div>
                  <div className="text-sm text-muted-foreground truncate max-w-md">
                    {post.content}
                  </div>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${getPlatformColor(post.platform)}`}>
                      {post.platform}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${getStatusColor(post.status)}`}>
                      {post.status === 'scheduled' ? 'Programmé' : post.status === 'draft' ? 'Brouillon' : post.status}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium">
                    {post.scheduledFor.toLocaleDateString('fr-FR', {
                      day: 'numeric',
                      month: 'long'
                    })}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {formatTime(post.scheduledFor)}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Calendrier</h1>
          <p className="text-muted-foreground">
            Planifiez et gérez vos publications sur les réseaux sociaux
          </p>
        </div>
        <Button className="flex items-center">
          <Plus className="h-4 w-4 mr-2" />
          Nouvelle publication
        </Button>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="outline" size="icon" onClick={previousMonth}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <h2 className="text-xl font-semibold">
            {getMonthName(currentDate)} {getYear(currentDate)}
          </h2>
          <Button variant="outline" size="icon" onClick={nextMonth}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
        
        <Tabs value={view} onValueChange={setView} className="w-auto">
          <TabsList>
            <TabsTrigger value="month" className="flex items-center">
              <Grid3X3 className="h-4 w-4 mr-2" />
              Mois
            </TabsTrigger>
            <TabsTrigger value="list" className="flex items-center">
              <List className="h-4 w-4 mr-2" />
              Liste
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>
      
      {view === 'month' ? renderMonthView() : renderListView()}
    </div>
  )
}

export default Calendar

