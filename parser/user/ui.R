# Use a fluid Bootstrap layout
fluidPage(    
  
  # Give the page a title
  titlePanel("Job skills by state"),
  
  # Generate a row with a sidebar
  sidebarLayout(

    # Define the sidebar with one input
    sidebarPanel(
      selectInput("state", "State:",
                  choices=state),
      hr(),
      helpText("Data from Indeed website")
    ),
  # selectInput("State", "Choose a State:", 
  #             choices=state),
  # 
  # selectInput("dataset", "Choose a dataset:", 
  #             choices = c("rock", "pressure", "cars")),
  # 
  # helpText("Note: while the data view will show only the specified",
  #          "number of observations, the summary will still be based",
  #          "on the full dataset."),
  # 
  # submitButton("Update View")
    # Create a spot for the barplot
    mainPanel(
      plotOutput("jobPlot")  
    )
    
  )
)