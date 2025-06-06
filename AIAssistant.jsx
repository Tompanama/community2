import { useState, useRef, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'

// Import UI components
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'

// Import icons
import {
  Send,
  MessageSquareText,
  Image,
  Calendar,
  Hash,
  Sparkles,
  Bot,
  Loader2,
  ChevronRight
} from 'lucide-react'

const AIAssistant = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('chat')
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: `Bonjour ${user?.name || 'Utilisateur'} ! Je suis votre assistant IA pour le community management. Comment puis-je vous aider aujourd'hui ?`,
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Suggestions for quick prompts
  const suggestions = [
    {
      id: 1,
      text: 'Génère une idée de post pour Instagram',
      icon: <MessageSquareText className="h-4 w-4" />
    },
    {
      id: 2,
      text: 'Suggère des hashtags pour mon secteur',
      icon: <Hash className="h-4 w-4" />
    },
    {
      id: 3,
      text: 'Quel est le meilleur moment pour publier ?',
      icon: <Calendar className="h-4 w-4" />
    },
    {
      id: 4,
      text: 'Crée une description pour ma photo',
      icon: <Image className="h-4 w-4" />
    }
  ]

  // Content generation templates
  const contentTemplates = [
    {
      id: 1,
      title: 'Post promotionnel',
      description: 'Annonce d\'une offre ou promotion',
      prompt: 'Génère un post promotionnel pour [produit/service] avec une offre de [détails]'
    },
    {
      id: 2,
      title: 'Contenu éducatif',
      description: 'Article ou post informatif sur votre domaine',
      prompt: 'Crée un contenu éducatif sur [sujet] pour mon audience de [description]'
    },
    {
      id: 3,
      title: 'Témoignage client',
      description: 'Mise en avant d\'un avis client',
      prompt: 'Rédige un post mettant en avant ce témoignage client : [témoignage]'
    },
    {
      id: 4,
      title: 'Question engageante',
      description: 'Question pour stimuler l\'engagement',
      prompt: 'Propose une question engageante sur [sujet] pour augmenter les commentaires'
    }
  ]

  // Image generation templates
  const imageTemplates = [
    {
      id: 1,
      title: 'Produit en situation',
      description: 'Visualisation de votre produit en contexte',
      prompt: 'Génère une image de [produit] utilisé dans [contexte]'
    },
    {
      id: 2,
      title: 'Citation inspirante',
      description: 'Citation sur fond visuel attractif',
      prompt: 'Crée une image avec la citation "[citation]" sur un fond [style]'
    },
    {
      id: 3,
      title: 'Infographie simple',
      description: 'Visualisation de données ou concepts',
      prompt: 'Crée une infographie simple sur [sujet] avec [nombre] points clés'
    },
    {
      id: 4,
      title: 'Bannière promotionnelle',
      description: 'Visuel pour une offre spéciale',
      prompt: 'Génère une bannière promotionnelle pour [événement/offre] dans un style [style]'
    }
  ]

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: input,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // In a real app, we would send a request to the backend
      // For now, we'll just simulate a delay and response
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock AI response based on user input
      let response = ''
      
      if (input.toLowerCase().includes('bonjour') || input.toLowerCase().includes('salut')) {
        response = `Bonjour ! Comment puis-je vous aider avec votre stratégie de community management aujourd'hui ?`
      } else if (input.toLowerCase().includes('idée') || input.toLowerCase().includes('post') || input.toLowerCase().includes('contenu')) {
        response = `Voici quelques idées de contenu pour dynamiser votre présence sur les réseaux sociaux :
        
1. Partagez les coulisses de votre entreprise pour humaniser votre marque
2. Créez un sondage pour engager votre communauté et recueillir des insights
3. Publiez un tutoriel ou un guide pratique lié à votre secteur d'activité
4. Mettez en avant un témoignage client pour renforcer votre crédibilité`
      } else if (input.toLowerCase().includes('hashtag')) {
        response = `Voici quelques hashtags populaires qui pourraient convenir à votre secteur :
        
#CommunityManagement #StratégieDigitale #MarketingDeContenu #EngagementCommunautaire #SocialMediaTips`
      } else if (input.toLowerCase().includes('performance') || input.toLowerCase().includes('statistique') || input.toLowerCase().includes('analytics')) {
        response = `Basé sur vos dernières publications, voici quelques insights :
        
- Vos posts avec images obtiennent 43% plus d'engagement
- Le meilleur moment pour publier semble être le jeudi entre 18h et 20h
- Les contenus sur le thème de l'innovation génèrent le plus de partages
- Essayez d'utiliser plus de questions dans vos légendes pour augmenter les commentaires`
      } else if (input.toLowerCase().includes('calendrier') || input.toLowerCase().includes('planification') || input.toLowerCase().includes('planning')) {
        response = `Pour optimiser votre calendrier de publication, je vous suggère :
        
- Maintenir une fréquence de 3-4 posts par semaine pour une présence régulière
- Alterner entre contenus promotionnels (20%) et contenus à valeur ajoutée (80%)
- Planifier vos publications importantes 2 semaines à l'avance
- Réserver les lundis matin pour l'analyse des performances de la semaine précédente`
      } else {
        response = `Je comprends votre question sur "${input}". Voici ce que je peux vous proposer :
        
1. Générer du contenu adapté à votre audience
2. Analyser les tendances de votre secteur
3. Optimiser votre stratégie de publication
4. Suggérer des améliorations pour vos posts existants

Pourriez-vous me donner plus de détails sur ce que vous recherchez exactement ?`
      }

      // Add AI response
      const assistantMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: response,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Add error message
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: 'Désolé, une erreur est survenue. Veuillez réessayer.',
        timestamp: new Date(),
        isError: true
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // Handle suggestion click
  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion.text)
  }

  // Handle template click
  const handleTemplateClick = (template) => {
    setInput(template.prompt)
  }

  // Format timestamp
  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Assistant IA</h1>
        <p className="text-muted-foreground">
          Votre assistant personnel pour optimiser votre stratégie de community management
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-3 mb-4">
          <TabsTrigger value="chat" className="flex items-center">
            <Bot className="h-4 w-4 mr-2" />
            Chat
          </TabsTrigger>
          <TabsTrigger value="content" className="flex items-center">
            <MessageSquareText className="h-4 w-4 mr-2" />
            Contenu
          </TabsTrigger>
          <TabsTrigger value="images" className="flex items-center">
            <Image className="h-4 w-4 mr-2" />
            Images
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="chat" className="space-y-4">
          {/* Chat interface */}
          <Card className="border-border">
            <CardContent className="p-0">
              <div className="h-[500px] flex flex-col">
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          message.role === 'user'
                            ? 'bg-primary text-primary-foreground'
                            : message.isError
                            ? 'bg-destructive/10 text-destructive'
                            : 'bg-muted'
                        }`}
                      >
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        <div
                          className={`text-xs mt-1 ${
                            message.role === 'user'
                              ? 'text-primary-foreground/70'
                              : 'text-muted-foreground'
                          }`}
                        >
                          {formatTimestamp(message.timestamp)}
                        </div>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
                
                <div className="border-t border-border p-4">
                  <form onSubmit={handleSubmit} className="flex space-x-2">
                    <Input
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Posez une question ou demandez de l'aide..."
                      disabled={isLoading}
                      className="flex-1"
                    />
                    <Button type="submit" size="icon" disabled={isLoading || !input.trim()}>
                      {isLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Send className="h-4 w-4" />
                      )}
                    </Button>
                  </form>
                  
                  <div className="mt-4">
                    <p className="text-sm text-muted-foreground mb-2">Suggestions :</p>
                    <div className="flex flex-wrap gap-2">
                      {suggestions.map((suggestion) => (
                        <Button
                          key={suggestion.id}
                          variant="outline"
                          size="sm"
                          onClick={() => handleSuggestionClick(suggestion)}
                          disabled={isLoading}
                          className="flex items-center"
                        >
                          {suggestion.icon}
                          <span className="ml-1">{suggestion.text}</span>
                        </Button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="content" className="space-y-4">
          {/* Content generation templates */}
          <div className="grid gap-4 md:grid-cols-2">
            {contentTemplates.map((template) => (
              <Card key={template.id} className="cursor-pointer hover:border-primary transition-colors">
                <CardHeader>
                  <CardTitle>{template.title}</CardTitle>
                  <CardDescription>{template.description}</CardDescription>
                </CardHeader>
                <CardFooter>
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => {
                      handleTemplateClick(template)
                      setActiveTab('chat')
                    }}
                  >
                    <Sparkles className="h-4 w-4 mr-2" />
                    Utiliser ce template
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
          
          <Card>
            <CardHeader>
              <CardTitle>Créer un template personnalisé</CardTitle>
              <CardDescription>
                Définissez votre propre template pour générer du contenu
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">
                <Sparkles className="h-4 w-4 mr-2" />
                Créer un nouveau template
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="images" className="space-y-4">
          {/* Image generation templates */}
          <div className="grid gap-4 md:grid-cols-2">
            {imageTemplates.map((template) => (
              <Card key={template.id} className="cursor-pointer hover:border-primary transition-colors">
                <CardHeader>
                  <CardTitle>{template.title}</CardTitle>
                  <CardDescription>{template.description}</CardDescription>
                </CardHeader>
                <CardFooter>
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => {
                      handleTemplateClick(template)
                      setActiveTab('chat')
                    }}
                  >
                    <Image className="h-4 w-4 mr-2" />
                    Utiliser ce template
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
          
          <Card>
            <CardHeader>
              <CardTitle>Créer une image personnalisée</CardTitle>
              <CardDescription>
                Décrivez l'image que vous souhaitez générer
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">
                <Image className="h-4 w-4 mr-2" />
                Créer une nouvelle image
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AIAssistant

