library(ggplot2)
library(scales)
jobData = read.csv("./data/jobFrame.csv",header = T)
state = levels(jobData$state)

stateData = jobData[jobData$state == " CA",-1]
count = sort(colSums(stateData))
plotData = data.frame("skill"=as.vector(count),"count"=names(count))

ggplot(plotData, aes(x=count, y=skill)) + geom_bar(stat="identity")
