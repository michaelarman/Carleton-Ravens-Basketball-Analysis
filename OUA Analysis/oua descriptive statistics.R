oua<-read.csv("oua.csv", header = T)
oua
library(ggplot2)
library(ggcorrplot)
plot(oua$NAME,oua$FG.)

#scatterplot between FG% and PTs. An obvious positive correlation
gg <- ggplot(oua, aes(x=oua$PTS, y=oua$FG.)) + 
  geom_point(aes(col=oua$NAME, size=oua$WIN.RATIO)) + 
  #geom_smooth(method="loess", se=F) + 
  labs(subtitle="PTs Vs FG", 
       y="FG", 
       x="Points", 
       title="Scatterplot", 
       caption = "Source: OUA")

plot(gg)

#correlogram
oua1<-oua[c(5,7,9:20)]
cor(oua1)
corr<-round(cor(oua1), 1)

ggcorrplot(corr, hc.order = TRUE, 
           type = "lower", 
           lab = TRUE, 
           lab_size = 3, 
           method="circle", 
           colors = c("tomato2", "white", "springgreen3"), 
           title="Correlogram of Offensive Statistics", 
           ggtheme=theme_bw)

#Deviance of Points
theme_set(theme_bw())  

# Data Prep
oua$PTS_z <- round((oua$PTS - mean(oua$PTS))/sd(oua$PTS), 2)  # compute normalized PTS
oua$PTS_type <- ifelse(oua$PTS_z< 0, "below", "above")  # above / below avg flag
oua <- oua[order(oua$PTS_z), ]  # sort
#oua$`NAME` <- factor(oua$`NAME`, levels = oua$`NAME`)  # convert to factor to retain sorted order in plot.

# Diverging Barcharts
ggplot(oua, aes(x=oua$NAME, y=oua$PTS_z, label=oua$PTS_z)) + 
  geom_bar(stat='identity', aes(fill=oua$PTS_type), width=.5)  +
  scale_fill_manual(name="Points", 
                    labels = c("Above Average", "Below Average"), 
                    values = c("above"="#00ba38", "below"="#f8766d")) + 
  labs(subtitle="Normalised Points from 'oua'", 
       title= "Diverging Bars") + 
  coord_flip()





#oua Defense statistics. An obvious negative correlation
oua_d<-read.csv('oua_defense.csv', header = T)

#scatterplot between FG% and PTs. An obvious positive correlation
gg1 <- ggplot(oua_d, aes(x=oua_d$PTS, y=oua_d$FG.)) + 
  geom_point(aes(col=oua_d$NAME, size=-oua_d$RK)) + 
  #geom_smooth(method="loess", se=F) + 
  labs(subtitle="PTs Vs FG", 
       y="FG", 
       x="Points", 
       title="Scatterplot", 
       caption = "Source: OUA")

plot(gg1)

#correlogram
oua2<-oua_d[c(5,7:18)]
cor(oua2)
corr<-round(cor(oua2), 1)


ggcorrplot(corr, hc.order = TRUE, 
           type = "lower", 
           lab = TRUE, 
           lab_size = 3, 
           method="circle", 
           colors = c("tomato2", "white", "springgreen3"), 
           title="Correlogram of Offensive Statistics", 
           ggtheme=theme_bw)



#Deviance of Points
theme_set(theme_bw())  

# Data Prep
oua_d$PTS_z <- round((oua_d$PTS - mean(oua_d$PTS))/sd(oua_d$PTS), 2)  # compute normalized PTS
oua_d$PTS_type <- ifelse(oua_d$PTS_z< 0, "above", "below")  # above / below avg flag
oua_d <- oua_d[order(oua_d$PTS_z), ]  # sort
#oua_d$`NAME` <- factor(oua_d$`NAME`, levels = oua_d$`NAME`)  # convert to factor to retain sorted order in plot.

# Diverging Barcharts
ggplot(oua_d, aes(x=oua_d$NAME, y=oua_d$PTS_z, label=oua_d$PTS_z)) + 
  geom_bar(stat='identity', aes(fill=oua_d$PTS_type), width=.5)  +
  scale_fill_manual(name="Points", 
                    labels = c("Above Average", "Below Average"), 
                    values = c("above"="#00ba38", "below"="#f8766d")) + 
  labs(subtitle="Normalised Points from 'oua_d'", 
       title= "Diverging Bars") + 
  coord_flip()





