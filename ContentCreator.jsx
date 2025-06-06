import { useState } from 'react'

// Import UI components
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import { Input } from '../../components/ui/input'
import { Textarea } from '../../components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'

// Import icons
import {
  MessageSquareText,
  Image,
  Video,
  LayoutGrid,
  Calendar,
  Send,
  Sparkles,
  Loader2,
  Plus,
  Hash,
  Clock
} from 'lucide-react'

const ContentCreator = () => {
  const [contentType, setContentType] = useState('text')
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [platform, setPlatform] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [isScheduling, setIsScheduling] = useState(false)
  const [hashtags, setHashtags] = useState([])
  const [newHashtag, setNewHashtag] = useState('')
  
  // Mock platforms
  const platforms = [
    { id: 'instagram', name: 'Instagram' },
    { id: 'facebook', name: 'Facebook' },
    { id: 'linkedin', name: 'LinkedIn' },
    { id: 'twitter', name: 'Twitter' },
    { id: 'youtube', name: 'YouTube' },
    { id: 'tiktok', name: 'TikTok' }
  ]
  
  // Mock AI suggestions
  const aiSuggestions = [
    {
      id: 1,
      title: 'Annonce de produit',
      description: 'Présentation d\'un nouveau produit ou service',
      prompt: 'Créez un post annonçant le lancement de notre nouveau produit [nom du produit]'
    },
    {
      id: 2,
      title: 'Contenu éducatif',
      description: 'Partage de connaissances sur votre domaine',
      prompt: 'Rédigez un post éducatif sur [sujet] pour notre audience'
    },
    {
      id: 3,
      title: 'Témoignage client',
      description: 'Mise en avant d\'un avis client',
      prompt: 'Créez un post mettant en valeur ce témoignage client : [témoignage]'
    },
    {
      id: 4,
      title: 'Promotion',
      description: 'Annonce d\'une offre spéciale',
      prompt: 'Rédigez un post promotionnel pour notre offre [détails de l\'offre]'
    }
  ]
  
  // Handle AI generation
  const handleGenerate = async () => {
    if (!platform || !title) return
    
    setIsGenerating(true)
    
    try {
      // In a real app, we would send a request to the backend
      // For now, we'll just simulate a delay and response
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock AI generated content
      let generatedContent = ''
      
      switch (contentType) {
        case 'text':
          generatedContent = `✨ ${title} ✨\n\nNous sommes ravis de partager avec vous cette actualité importante ! Notre équipe a travaillé sans relâche pour vous offrir la meilleure expérience possible.\n\nQu'en pensez-vous ? Partagez votre avis en commentaire ! 👇`
          setHashtags(['#CommunityAI', '#ContentCreation', '#SocialMedia'])
          break
        case 'image':
          generatedContent = `Découvrez notre nouvelle création visuelle ! Cette image représente parfaitement notre vision et nos valeurs.\n\nQu'est-ce qui vous inspire le plus dans cette image ?`
          setHashtags(['#DesignInspiration', '#VisualContent', '#CreativeMinds'])
          break
        case 'video':
          generatedContent = `🎬 Nouvelle vidéo ! 🎬\n\nNous avons préparé ce contenu spécialement pour vous. Regardez jusqu'à la fin pour une surprise !\n\nN'oubliez pas de liker et partager si vous avez apprécié !`
          setHashtags(['#VideoContent', '#WatchNow', '#NewRelease'])
          break
        case 'carousel':
          generatedContent = `📱 Faites défiler pour découvrir nos conseils exclusifs ! 📱\n\n1️⃣ Premier conseil important\n2️⃣ Deuxième astuce à ne pas manquer\n3️⃣ Troisième secret pour réussir\n\nEnregistrez ce post pour y revenir plus tard !`
          setHashtags(['#SwipeRight', '#TipsAndTricks', '#SaveThisPost'])
          break
        default:
          generatedContent = `Contenu généré pour ${title}`
      }
      
      setContent(generatedContent)
    } catch (error) {
      console.error('Error generating content:', error)
    } finally {
      setIsGenerating(false)
    }
  }
  
  // Handle scheduling
  const handleSchedule = async () => {
    if (!platform || !title || !content) return
    
    setIsScheduling(true)
    
    try {
      // In a real app, we would send a request to the backend
      // For now, we'll just simulate a delay
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Reset form
      setTitle('')
      setContent('')
      setPlatform('')
      setHashtags([])
      setContentType('text')
      
      // Show success message (in a real app)
      alert('Publication programmée avec succès !')
    } catch (error) {
      console.error('Error scheduling post:', error)
    } finally {
      setIsScheduling(false)
    }
  }
  
  // Handle adding hashtag
  const handleAddHashtag = () => {
    if (!newHashtag.trim()) return
    
    // Add # if not present
    let tag = newHashtag.trim()
    if (!tag.startsWith('#')) {
      tag = `#${tag}`
    }
    
    // Remove spaces
    tag = tag.replace(/\s+/g, '')
    
    setHashtags([...hashtags, tag])
    setNewHashtag('')
  }
  
  // Handle removing hashtag
  const handleRemoveHashtag = (index) => {
    const newHashtags = [...hashtags]
    newHashtags.splice(index, 1)
    setHashtags(newHashtags)
  }
  
  // Handle AI suggestion click
  const handleSuggestionClick = (suggestion) => {
    setTitle(suggestion.title)
    setContent(suggestion.prompt)
  }
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Créateur de contenu</h1>
        <p className="text-muted-foreground">
          Créez et planifiez du contenu pour vos réseaux sociaux
        </p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Nouveau contenu</CardTitle>
              <CardDescription>
                Créez votre publication pour les réseaux sociaux
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Tabs value={contentType} onValueChange={setContentType} className="w-full">
                <TabsList className="grid grid-cols-4 mb-4">
                  <TabsTrigger value="text" className="flex items-center">
                    <MessageSquareText className="h-4 w-4 mr-2" />
                    Texte
                  </TabsTrigger>
                  <TabsTrigger value="image" className="flex items-center">
                    <Image className="h-4 w-4 mr-2" />
                    Image
                  </TabsTrigger>
                  <TabsTrigger value="video" className="flex items-center">
                    <Video className="h-4 w-4 mr-2" />
                    Vidéo
                  </TabsTrigger>
                  <TabsTrigger value="carousel" className="flex items-center">
                    <LayoutGrid className="h-4 w-4 mr-2" />
                    Carrousel
                  </TabsTrigger>
                </TabsList>
                
                <div className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <label htmlFor="platform" className="text-sm font-medium">
                        Plateforme
                      </label>
                      <Select value={platform} onValueChange={setPlatform}>
                        <SelectTrigger>
                          <SelectValue placeholder="Sélectionnez une plateforme" />
                        </SelectTrigger>
                        <SelectContent>
                          {platforms.map((p) => (
                            <SelectItem key={p.id} value={p.id}>
                              {p.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="space-y-2">
                      <label htmlFor="title" className="text-sm font-medium">
                        Titre
                      </label>
                      <Input
                        id="title"
                        placeholder="Titre de votre publication"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <label htmlFor="content" className="text-sm font-medium">
                      Contenu
                    </label>
                    <Textarea
                      id="content"
                      placeholder="Rédigez votre contenu ici..."
                      rows={6}
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                    />
                  </div>
                  
                  {contentType === 'image' && (
                    <div className="border-2 border-dashed border-border rounded-md p-6 text-center">
                      <Image className="h-8 w-8 mx-auto text-muted-foreground" />
                      <p className="mt-2 text-sm text-muted-foreground">
                        Glissez-déposez une image ou cliquez pour télécharger
                      </p>
                      <Button variant="outline" className="mt-4">
                        Télécharger une image
                      </Button>
                    </div>
                  )}
                  
                  {contentType === 'video' && (
                    <div className="border-2 border-dashed border-border rounded-md p-6 text-center">
                      <Video className="h-8 w-8 mx-auto text-muted-foreground" />
                      <p className="mt-2 text-sm text-muted-foreground">
                        Glissez-déposez une vidéo ou cliquez pour télécharger
                      </p>
                      <Button variant="outline" className="mt-4">
                        Télécharger une vidéo
                      </Button>
                    </div>
                  )}
                  
                  {contentType === 'carousel' && (
                    <div className="border-2 border-dashed border-border rounded-md p-6 text-center">
                      <LayoutGrid className="h-8 w-8 mx-auto text-muted-foreground" />
                      <p className="mt-2 text-sm text-muted-foreground">
                        Ajoutez plusieurs images pour créer un carrousel
                      </p>
                      <Button variant="outline" className="mt-4">
                        Ajouter des images
                      </Button>
                    </div>
                  )}
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Hashtags</label>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {hashtags.map((tag, index) => (
                        <div
                          key={index}
                          className="bg-primary/10 text-primary px-2 py-1 rounded-full text-sm flex items-center"
                        >
                          {tag}
                          <button
                            onClick={() => handleRemoveHashtag(index)}
                            className="ml-1 hover:text-destructive"
                          >
                            &times;
                          </button>
                        </div>
                      ))}
                    </div>
                    <div className="flex space-x-2">
                      <Input
                        placeholder="Ajouter un hashtag"
                        value={newHashtag}
                        onChange={(e) => setNewHashtag(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault()
                            handleAddHashtag()
                          }
                        }}
                      />
                      <Button variant="outline" onClick={handleAddHashtag}>
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </Tabs>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline" onClick={handleGenerate} disabled={isGenerating || !platform || !title}>
                {isGenerating ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4 mr-2" />
                    Générer avec l'IA
                  </>
                )}
              </Button>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Calendar className="h-4 w-4 mr-2" />
                  Enregistrer comme brouillon
                </Button>
                <Button onClick={handleSchedule} disabled={isScheduling || !platform || !title || !content}>
                  {isScheduling ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Programmation...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Programmer
                    </>
                  )}
                </Button>
              </div>
            </CardFooter>
          </Card>
        </div>
        
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Suggestions de l'IA</CardTitle>
              <CardDescription>
                Idées de contenu générées par l'IA
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {aiSuggestions.map((suggestion) => (
                <div
                  key={suggestion.id}
                  className="p-3 border border-border rounded-md cursor-pointer hover:border-primary hover:bg-primary/5 transition-colors"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  <h3 className="font-medium">{suggestion.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {suggestion.description}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Meilleurs moments pour publier</CardTitle>
              <CardDescription>
                Basé sur l'engagement de votre audience
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>Instagram</span>
                  </div>
                  <span className="text-sm font-medium">Jeudi 18h-20h</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>Facebook</span>
                  </div>
                  <span className="text-sm font-medium">Mercredi 12h-14h</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>LinkedIn</span>
                  </div>
                  <span className="text-sm font-medium">Mardi 8h-10h</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>Twitter</span>
                  </div>
                  <span className="text-sm font-medium">Lundi 12h-13h</span>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Hashtags populaires</CardTitle>
              <CardDescription>
                Hashtags tendance dans votre secteur
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                <Button variant="outline" size="sm" className="flex items-center" onClick={() => setHashtags([...hashtags, '#MarketingDigital'])}>
                  <Hash className="h-3 w-3 mr-1" />
                  MarketingDigital
                </Button>
                <Button variant="outline" size="sm" className="flex items-center" onClick={() => setHashtags([...hashtags, '#ContentCreation'])}>
                  <Hash className="h-3 w-3 mr-1" />
                  ContentCreation
                </Button>
                <Button variant="outline" size="sm" className="flex items-center" onClick={() => setHashtags([...hashtags, '#SocialMedia'])}>
                  <Hash className="h-3 w-3 mr-1" />
                  SocialMedia
                </Button>
                <Button variant="outline" size="sm" className="flex items-center" onClick={() => setHashtags([...hashtags, '#DigitalStrategy'])}>
                  <Hash className="h-3 w-3 mr-1" />
                  DigitalStrategy
                </Button>
                <Button variant="outline" size="sm" className="flex items-center" onClick={() => setHashtags([...hashtags, '#CommunityManagement'])}>
                  <Hash className="h-3 w-3 mr-1" />
                  CommunityManagement
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default ContentCreator

