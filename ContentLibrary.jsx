import { useState } from 'react'

// Import UI components
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import { Input } from '../../components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'

// Import icons
import {
  Image,
  Video,
  FileText,
  LayoutTemplate,
  Search,
  Plus,
  MoreHorizontal,
  Filter,
  Grid3X3,
  List
} from 'lucide-react'

const ContentLibrary = () => {
  const [view, setView] = useState('grid')
  const [activeTab, setActiveTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('date')
  
  // Mock media assets
  const mediaAssets = [
    {
      id: 1,
      type: 'image',
      title: 'Logo principal',
      url: '/assets/logo.png',
      thumbnail: '/assets/logo.png',
      createdAt: new Date(2025, 5, 1),
      tags: ['logo', 'branding']
    },
    {
      id: 2,
      type: 'image',
      title: 'Photo produit A',
      url: '/assets/product-a.jpg',
      thumbnail: '/assets/product-a-thumb.jpg',
      createdAt: new Date(2025, 5, 3),
      tags: ['produit', 'catalogue']
    },
    {
      id: 3,
      type: 'video',
      title: 'Tutoriel application',
      url: '/assets/tutorial.mp4',
      thumbnail: '/assets/tutorial-thumb.jpg',
      createdAt: new Date(2025, 5, 5),
      tags: ['tutoriel', 'formation']
    },
    {
      id: 4,
      type: 'document',
      title: 'Présentation entreprise',
      url: '/assets/presentation.pdf',
      thumbnail: '/assets/presentation-thumb.jpg',
      createdAt: new Date(2025, 5, 7),
      tags: ['présentation', 'entreprise']
    },
    {
      id: 5,
      type: 'template',
      title: 'Template post Instagram',
      url: '/assets/instagram-template.psd',
      thumbnail: '/assets/instagram-template-thumb.jpg',
      createdAt: new Date(2025, 5, 9),
      tags: ['template', 'instagram']
    },
    {
      id: 6,
      type: 'image',
      title: 'Bannière site web',
      url: '/assets/banner.jpg',
      thumbnail: '/assets/banner-thumb.jpg',
      createdAt: new Date(2025, 5, 11),
      tags: ['bannière', 'site web']
    },
    {
      id: 7,
      type: 'video',
      title: 'Témoignage client',
      url: '/assets/testimonial.mp4',
      thumbnail: '/assets/testimonial-thumb.jpg',
      createdAt: new Date(2025, 5, 13),
      tags: ['témoignage', 'client']
    },
    {
      id: 8,
      type: 'document',
      title: 'Guide utilisateur',
      url: '/assets/user-guide.pdf',
      thumbnail: '/assets/user-guide-thumb.jpg',
      createdAt: new Date(2025, 5, 15),
      tags: ['guide', 'documentation']
    }
  ]
  
  // Filter assets by type and search query
  const filteredAssets = mediaAssets.filter(asset => {
    // Filter by type
    if (activeTab !== 'all' && asset.type !== activeTab) {
      return false
    }
    
    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      return (
        asset.title.toLowerCase().includes(query) ||
        asset.tags.some(tag => tag.toLowerCase().includes(query))
      )
    }
    
    return true
  })
  
  // Sort assets
  const sortedAssets = [...filteredAssets].sort((a, b) => {
    if (sortBy === 'date') {
      return b.createdAt - a.createdAt
    } else if (sortBy === 'name') {
      return a.title.localeCompare(b.title)
    } else if (sortBy === 'type') {
      return a.type.localeCompare(b.type)
    }
    return 0
  })
  
  // Format date
  const formatDate = (date) => {
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }
  
  // Get icon by type
  const getIconByType = (type) => {
    switch (type) {
      case 'image':
        return <Image className="h-5 w-5" />
      case 'video':
        return <Video className="h-5 w-5" />
      case 'document':
        return <FileText className="h-5 w-5" />
      case 'template':
        return <LayoutTemplate className="h-5 w-5" />
      default:
        return <FileText className="h-5 w-5" />
    }
  }
  
  // Get color by type
  const getColorByType = (type) => {
    switch (type) {
      case 'image':
        return 'bg-blue-100 text-blue-800'
      case 'video':
        return 'bg-red-100 text-red-800'
      case 'document':
        return 'bg-green-100 text-green-800'
      case 'template':
        return 'bg-purple-100 text-purple-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }
  
  // Render grid view
  const renderGridView = () => {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {sortedAssets.map((asset) => (
          <Card key={asset.id} className="cursor-pointer hover:border-primary transition-colors">
            <div className="aspect-square relative overflow-hidden bg-muted">
              <div className="absolute top-2 right-2 z-10">
                <Button variant="ghost" size="icon" className="h-8 w-8 bg-background/80 backdrop-blur-sm">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
              <div className="absolute top-2 left-2 z-10">
                <span className={`text-xs px-2 py-1 rounded-full ${getColorByType(asset.type)}`}>
                  {asset.type}
                </span>
              </div>
              <div className="h-full w-full flex items-center justify-center">
                {getIconByType(asset.type)}
              </div>
            </div>
            <CardContent className="p-4">
              <h3 className="font-medium truncate">{asset.title}</h3>
              <p className="text-xs text-muted-foreground">
                {formatDate(asset.createdAt)}
              </p>
              <div className="flex flex-wrap gap-1 mt-2">
                {asset.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="text-xs bg-muted px-1.5 py-0.5 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }
  
  // Render list view
  const renderListView = () => {
    return (
      <div className="space-y-2">
        {sortedAssets.map((asset) => (
          <Card key={asset.id} className="cursor-pointer hover:border-primary transition-colors">
            <CardContent className="p-4">
              <div className="flex items-center space-x-4">
                <div className="h-12 w-12 rounded bg-muted flex items-center justify-center">
                  {getIconByType(asset.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium truncate">{asset.title}</h3>
                  <div className="flex items-center text-sm text-muted-foreground">
                    <span className={`text-xs px-1.5 py-0.5 rounded-full mr-2 ${getColorByType(asset.type)}`}>
                      {asset.type}
                    </span>
                    <span>{formatDate(asset.createdAt)}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="flex flex-wrap gap-1">
                    {asset.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="text-xs bg-muted px-1.5 py-0.5 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <Button variant="ghost" size="icon">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
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
          <h1 className="text-3xl font-bold tracking-tight">Bibliothèque de contenu</h1>
          <p className="text-muted-foreground">
            Gérez vos ressources médias et templates
          </p>
        </div>
        <Button className="flex items-center">
          <Plus className="h-4 w-4 mr-2" />
          Ajouter un média
        </Button>
      </div>
      
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full md:w-auto">
          <TabsList>
            <TabsTrigger value="all">Tous</TabsTrigger>
            <TabsTrigger value="image">Images</TabsTrigger>
            <TabsTrigger value="video">Vidéos</TabsTrigger>
            <TabsTrigger value="document">Documents</TabsTrigger>
            <TabsTrigger value="template">Templates</TabsTrigger>
          </TabsList>
        </Tabs>
        
        <div className="flex items-center space-x-2">
          <div className="relative w-full md:w-auto">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Rechercher..."
              className="pl-8 w-full md:w-[200px]"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-[180px]">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Trier par" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="date">Date (récent d'abord)</SelectItem>
              <SelectItem value="name">Nom (A-Z)</SelectItem>
              <SelectItem value="type">Type</SelectItem>
            </SelectContent>
          </Select>
          
          <div className="flex items-center border rounded-md">
            <Button
              variant={view === 'grid' ? 'default' : 'ghost'}
              size="icon"
              className="h-9 w-9 rounded-none rounded-l-md"
              onClick={() => setView('grid')}
            >
              <Grid3X3 className="h-4 w-4" />
            </Button>
            <Button
              variant={view === 'list' ? 'default' : 'ghost'}
              size="icon"
              className="h-9 w-9 rounded-none rounded-r-md"
              onClick={() => setView('list')}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
      
      {sortedAssets.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center mb-4">
            <Search className="h-6 w-6 text-muted-foreground" />
          </div>
          <h3 className="font-medium text-lg">Aucun résultat trouvé</h3>
          <p className="text-muted-foreground mt-1">
            Essayez de modifier vos filtres ou votre recherche
          </p>
        </div>
      ) : (
        view === 'grid' ? renderGridView() : renderListView()
      )}
    </div>
  )
}

export default ContentLibrary

