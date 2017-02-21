# Use a fluid Bootstrap layout
fluidPage(    
  
  # Give the page a title
  titlePanel("Job skills by state"),
  
  # Generate a row with a sidebar
  sidebarLayout(
    sidebarPanel(
      
      selectInput("skill", "Choose a skill:",
                  choices = skill),
      
      selectInput("state", "Choose a state:",
                  choices=state),
    
      helpText("The two sidebar will control the two barplot separatly")
    ),
    # Create a spot for the barplot
    mainPanel(
      plotOutput("statePlot",width = "100%",height = "20%"),
      plotOutput("skillPlot",width = "100%",height = "20%")
    )
  )
)