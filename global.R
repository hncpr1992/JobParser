library(ggplot2)
library(scales)
library(Hmisc)
jobData = read.csv("data/jobFrame.csv",header = T)
names(jobData)[2] = "c++"
state = levels(jobData$state)
skill = names(jobData)[-1]
