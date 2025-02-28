# a)	load Auto.csv file in a variable called Auto. 
Auto = read.csv("Auto.csv", na.strings = '?')
# 



# b)	What is the type and class of Auto variable
class(Auto)
# [1] "data.frame"

typeof(Auto)
# [1] "list"



# c)	Use a R command/function to find the dimensions of the Auto variable
dim(Auto)
# [1] 397   9



# a)	Use an R command to remove all NA’s from Auto variable. 
# redo  step (c) to report the new dimensions of Auto variable
Auto = na.omit(Auto)
#

dim(Auto)
# [1] 392   9



# e)	Use an R command to report the names of all variables in Auto
names(Auto)
# [1] "mpg" "cylinders" "displacement" "horsepower" "weight" "acceleration" "year"        
# [8] "origin"       "name"



# f)	Use attach() function to be able to directly access fields
# in Auto variable and then plot the cylinders by mpg. The axes of 
# the plot should not have “Auto$.....” string
attach(Auto)
#

plot(cylinders, mpg, xlab = "cylinders", ylab = "mpg")
# **plot of graph is the output**



# g)	Convert the “cylinders” field in auto to a factor and use the 
# plot function to generate a plot of cylinders by mpg. Make sure the 
# results are draw with green color and the y and x axis of the 
# graph has “CYLINDERS” and “MPG” respectively
Auto$cylinders = as.factor(Auto$cylinders)
#

plot(Auto$cylinders, Auto$mpg, xlab = "cylinders", ylab = "mpg", col = "green")
# **plot of graph is the output**



# h)	Draw a histogram of mpg variable in auto, using green color to 
# fill the bars. Make sure that the histogram only generate 10 bars
hist(Auto$mpg,
     breaks = seq(min(Auto$mpg), max(Auto$mpg), length.out = 11),
     col = "green")
# **plot of graph is the output**



# i)	Use the pairs() function in R to  generate a plot matrix, 
# consisting of scatterplots for each variable-combination of 
# “mpg”, “displacement”, “horsepower”, “weight”, and “acceleration” 
# fields in Auto variable.
Auto$horsepower = as.numeric(Auto$horsepower)
#

Auto_clean = na.omit(Auto)
#

selected_vars = Auto_clean[, c("mpg",
                                "displacement",
                                "horsepower",
                                "weight",
                                "acceleration")]
#

pairs(selected_vars)
# **plot of graph is the output**



# j)	Report Descriptive Statistics for all fields of Auto variable
summary(Auto_clean)
#mpg        cylinders  displacement     horsepower        weight      acceleration        year      
#Min.   : 9.00   3:  4     Min.   : 68.0   Min.   : 46.0   Min.   :1613   Min.   : 8.00   Min.   :70.00  
#1st Qu.:17.00   4:199     1st Qu.:105.0   1st Qu.: 75.0   1st Qu.:2225   1st Qu.:13.78   1st Qu.:73.00  
#Median :22.75   5:  3     Median :151.0   Median : 93.5   Median :2804   Median :15.50   Median :76.00  
#Mean   :23.45   6: 83     Mean   :194.4   Mean   :104.5   Mean   :2978   Mean   :15.54   Mean   :75.98  
#3rd Qu.:29.00   8:103     3rd Qu.:275.8   3rd Qu.:126.0   3rd Qu.:3615   3rd Qu.:17.02   3rd Qu.:79.00  
#Max.   :46.60             Max.   :455.0   Max.   :230.0   Max.   :5140   Max.   :24.80   Max.   :82.00  
#origin          name          
#Min.   :1.000   Length:392        
#1st Qu.:1.000   Class :character  
#Median :1.000   Mode  :character  
#Mean   :1.577                     
#3rd Qu.:2.000                     
#Max.   :3.000
sapply(Auto_clean[, sapply(Auto_clean, is.numeric)], sd)
#mpg displacement   horsepower       weight acceleration         year       origin 
#7.8050075  104.6440039   38.4911599  849.4025600    2.7588641    3.6837365    0.8055182
length(unique(Auto$name))
# 301