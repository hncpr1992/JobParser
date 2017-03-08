# Define a server for the Shiny app
function(input, output) {
  dataState = reactive({
      count = sort(colSums(jobData[jobData$state == input$state,-1]))
      data = data.frame(
        "count"=as.integer(as.vector(count)),
        "skill"=names(count))
  })
  
  dataSkill = reactive({
    name = input$skill
    skill = jobData[,c("state",name)]
    agg = aggregate(skill[,name]~skill[,"state"],data=skill,sum)
    names(agg) = c("state","count")
    data = agg
  })
  # Fill in the spot we created for a plot
  output$skillPlot <- renderPlot({
    
    output$statePlot <- renderPlot({
      
      # Render a barplot
      ggplot(dataSkill(), aes(x=reorder(state,-count), y=count)) + 
        geom_bar(stat="identity", fill="lightblue", colour="black") +
        coord_cartesian(ylim=c(0,max(dataSkill()$count)+5)) +
        theme(axis.title = element_text(size = 15),
              axis.text.x = element_text(size = 10),
              plot.title = element_text(size=22,hjust = 0.5)) +
        scale_y_continuous(breaks= pretty_breaks()) +
        xlab("State") + 
        ylab("Count") +
        ggtitle(paste(capitalize(input$skill),"counts in states"))
    },height = 220)
    
    # Render a barplot
    ggplot(dataState(), aes(x=reorder(skill,-count), y=count)) + 
      geom_bar(stat="identity", fill="lightblue", colour="black") + 
      coord_cartesian(ylim=c(0,max(dataState()$count)+5)) +
      scale_y_continuous(breaks= pretty_breaks()) +
      theme(axis.text.x = element_text(angle = 70, hjust = 1,size = 15),
            axis.title= element_text(size = 15),
            plot.title = element_text(size=22,hjust = 0.5)) +
      xlab("Skill") + 
      ylab("Count")+
      ggtitle(paste("Skills at",input$state))
  }, height = 270)
  
}