library(arules)
library(arulesViz)
library(caret)

teamplays<-read.csv("allfactors team plays.csv", header = T)

dat <- data.frame(lapply(teamplays, function(x) as.factor(as.character(x))))


#association mining rules for games resulting in a loss
rules<-apriori((dat), appearance=list(rhs= c("Win=0"), default="lhs"))
summary(rules)

#sort by count/support
rules_count<-sort(rules, by='count', decreasing = T)
inspect(rules_count[1:10])
#sort by lift
rules_lift<-sort(rules, by='lift', decreasing = T)
inspect(rules_lift[1:10])

#games resulting in a win
rules1<-apriori((dat), appearance=list(rhs= c("Win=1"), default="lhs"))
rules_1count <- sort(rules1, by='count', decreasing = TRUE)
rules_1lift <- sort(rules1, by='lift', decreasing = TRUE)
summary(rules1)
inspect(rules_1count[1:10])
inspect(rules_1lift[1:10])

topRules_count<-rules_count[1:25]
topRules_1count<-rules_1count[1:25]

plot(topRules_count, method="graph")
plot(topRules_1count, method="graph")

df<-as(topRules_count, 'data.frame')
write.csv(df, file = 'association.team.csv')
