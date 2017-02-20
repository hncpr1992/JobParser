# Define a server for the Shiny app
function(input, output) {
  data = reactive({
      count = sort(colSums(jobData[jobData$state == input$state,-1]))
      data = data.frame(
        "count"=as.integer(as.vector(count)),
        "skill"=names(count))
  })
  # Fill in the spot we created for a plot
  output$jobPlot <- renderPlot({
    
    # Render a barplot
    
    ggplot(data(), aes(x=reorder(skill,-count), y=count)) + 
      geom_bar(stat="identity", fill="lightblue", colour="black") + 
      coord_cartesian(ylim=c(0,max(data()$count)+5)) +
      scale_y_continuous(breaks= pretty_breaks()) +
      theme(axis.text.x = element_text(angle = 70, hjust = 1,size = 15)) 
  })
}