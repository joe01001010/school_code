# a)	load Auto.csv file in a variable called Auto. 
Auto = read.csv("Auto.csv")
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
# [1] 397   9



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
breaks_in_mpg = seq(min(Auto$mpg), max(Auto$mpg), length.out = 11)
#

hist(Auto$mpg, breaks = breaks_in_mpg,
     col="green",
     xlab = "mpg",
     ylab = "occurences",
     main = "Histogram of MPG")
# **plot of graph is the output**



# i)	Use the pairs() function in R to  generate a plot matrix, 
# consisting of scatterplots for each variable-combination of 
# “mpg”, “displacement”, “horsepower”, “weight”, and “acceleration” 
# fields in Auto variable.
Auto$horsepower <- as.numeric(Auto$horsepower)
#

Auto_clean <- na.omit(Auto)
#

selected_vars <- Auto_clean[, c("mpg",
                                "displacement",
                                "horsepower",
                                "weight",
                                "acceleration")]
#

pairs(selected_vars)
# **plot of graph is the output**