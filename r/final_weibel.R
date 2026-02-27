<<<<<<< HEAD
##############################################
# Q1)
##############################################

alzheimer_data = read.csv('Alzheimer.csv')


# a.1)
a1_table = table(alzheimer_data$DrugType, alzheimer_data$Gender)
chisq_test_a1 = chisq.test(a1_table)

print(chisq_test_a1)
#Pearson's Chi-squared test
#
#data:  a1_table
#X-squared = 47.8, df = 2, p-value = 4.171e-11

chisq_test_a1$observed
#f   m
#A  40 103
#B  49  26
#C  46  17

#chisq_test_a1$expected
#f        m
#A 68.70107 74.29893
#B 36.03203 38.96797
#C 30.26690 32.7331

# This test shows that the p value is significantly less than 0.05
# This test also shows that there was a disproportionate amount of some drugs
# given to one gender and a disproportionate amount of another drug given to a
# different gender. For examople, the drug that is being tested was given 
# more to men than women and women received a lot more of the arthritis drug

min(chisq_test_a1$expected)
#[1] 30.2669
print(chisq_test_a1$expected)
#f        m
#A 68.70107 74.29893
#B 36.03203 38.96797
#C 30.26690 32.73310

# This is my check to ensure my assumption is met, all values should be 
# greater than 5 telling me that the sample size is large enough to use the
# chi-squared test for approximation.




# a.2)
effectiveness_scale = aov(EffectivenessScale ~ DrugType, data = alzheimer_data)
summary(effectiveness_scale)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType      2   4.75  2.3769   3.991 0.0196 *
#  Residuals   278 165.59  0.5956                 
#---
#  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# This test uses a one way analysis of variance between effectiveness of each
# drug and compares them with eachother. Since the P value is less than 0.05 I
# am able to reject the null hypothesis and I can say there is a difference
# in the average of effectiveness of the drugs. The original null hypothesis
# was that there was no difference between the average effectiveness of the 
# different drugs

shapiro.test(resid(effectiveness_scale))
#Shapiro-Wilk normality test
#
#data:  resid(effectiveness_scale)
#W = 0.9921, p-value = 0.1395

# This is a check of the normality of the data ensuring the data is normal
# for the aov test I did prior. Since the p value is greater than 0.05 I 
# can confidently use this test.




# a.3)
gender_t_test = t.test(EffectivenessScale ~ Gender, data = alzheimer_data)
print(gender_t_test)
#Welch Two Sample t-test
#
#data:  EffectivenessScale by Gender
#t = -1.8365, df = 253.18, p-value = 0.06746
#alternative hypothesis: true difference in means between group f and group m is not equal to 0
#95 percent confidence interval:
#  -0.35629603  0.01244215
#sample estimates:
#  mean in group f mean in group m 
#-0.3946667      -0.2227397

# This is the two sample t test that is testing the difference between 
# effectiveness of the drugs like that aov test but this one will compare
# the effectiveness between the different drugs between the genders.
# The null hypothesis would be that there is no difference between the average
# effectiveness of the drugs between the genders with the alternate hypothesis
# suggesting there is a difference. Since the p value is 0.06 and is greater
# than 0.05 I do not reject the null hypothesis. This is pretty close to making
# me want to reject the null hypothesis so I would do some further tests on
# this subject

shapiro_female = shapiro.test(alzheimer_data$EffectivenessScale[alzheimer_data$Gender == 'f'])
shapiro_male = shapiro.test(alzheimer_data$EffectivenessScale[alzheimer_data$Gender == 'm'])

print(shapiro_female)
#Shapiro-Wilk normality test
#
#data:  alzheimer_data$EffectivenessScale[alzheimer_data$Gender == "f"]
#W = 0.98311, p-value = 0.09339

print(shapiro_male)
#Shapiro-Wilk normality test
#
#data:  alzheimer_data$EffectivenessScale[alzheimer_data$Gender == "m"]
#W = 0.98118, p-value = 0.04248

# This check is to ensure the data is normalised so I can use the welch two
# sample t test. Since the female data is normally distributed but the male
# p value is less than 0.05 we can say the male data is not normally distributed
# Since I am using the welch two sample t test this is acceptable for unequal variances






# bonus)
# c.1)
two_way_anova = aov(EffectivenessScale ~ DrugType + Gender, data = alzheimer_data)
summary(two_way_anova)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType      2   4.75  2.3769   3.985 0.0197 *
#  Gender        1   0.36  0.3632   0.609 0.4359  
#Residuals   277 165.22  0.5965                 
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# Since the p value for drug type is less than 0.05 I can confidently say 
# The kind of drug given has a significant impact on effectiveness of the drug.
# Since the p value for gender is over 0.05 I can confidently say the gender
# does not play a significant role in effectiveness of the drug.





# c.2)
two_way_anova_combined = aov(EffectivenessScale ~ DrugType * Gender, data = alzheimer_data)
summary(two_way_anova_combined)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType          2   4.75  2.3769   4.046 0.0185 *
#  Gender            1   0.36  0.3632   0.618 0.4324  
#DrugType:Gender   2   3.68  1.8391   3.131 0.0452 *
#  Residuals       275 161.55  0.5874                 
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# the drug type and gender p values back up the results from c.1 but the 
# DrugType:Gender p value shows that the gender combined with drug type can show
# the gender can have a variance between effectiveness of each drug.






##############################################################
#Q2)
##############################################################


# a)
# I would use a two sample t test because I am comparing the averages of two 
# separate groups being the group that was taught traditionally and the 
# group that was taught using a technology enhanced approach

# b)
# (H0) There is no significant difference between the average scores of the 
# students who were taught by traditional lectures compared to the students 
# who were taught with a more interactive approach
#
# (H1) There is a significant difference between the average scores of the 
# students who were taught by traditional lectures compared to the students 
# who were taught with a more interactive approach

# c)
Scores_Group_A = c(78, 85, 92, 88, 76, 80, 85, 84, 89, 91)
Scores_Group_B = c(85, 89, 94, 91, 87, 90, 93, 88, 90, 92)
t_test_result = t.test(Scores_Group_A, Scores_Group_B)
print(t_test_result)
#Welch Two Sample t-test
#
#data:  Scores_Group_A and Scores_Group_B
#t = -2.6454, df = 13.375, p-value = 0.0198
#alternative hypothesis: true difference in means is not equal to 0
#95 percent confidence interval:
#  -9.2530613 -0.9469387
#sample estimates:
#  mean of x mean of y 
#84.8      89.9

# This shows the p value is less than 0.05 so I am rejecting the null hypothesis
# This means that the students who were taught with the more interactive
# methods and technology based approach had a higher average score than the other
# group of students. For the teaching methods if we want students to have higher
# scores most students will benefit from interactie teaching plans as opposed to 
# lectures

# d)
# The first assumption is that the groups are not influenced by eachother.
# From the explanation of the question I can safely assume the two group's scores
# are separate and not influencing eachother
#
#
# The second assumption is that the scores in the groups are normally distributed
# I can use a shapiro test to see if they are normally distributed.
shapiro.test(Scores_Group_A)
#Shapiro-Wilk normality test
#
#data:  Scores_Group_A
#W = 0.94902, p-value = 0.6569
shapiro.test(Scores_Group_B)
#Shapiro-Wilk normality test
#
#data:  Scores_Group_B
#W = 0.98551, p-value = 0.9878
#
# Since the p value is greather than 0.05 the data is normal
#
#
# The third assumption is that the variances between the two groups should be equal
# I can use levenes test to check the variance equality. Since this is a small
# Test with only 10 scores from each group I can see that the groups are 
# evenly represented in the test.
=======
##############################################
# Q1)
##############################################

alzheimer_data = read.csv('Alzheimer.csv')


# a.1)
alzheimer_data$GenderNumeric = ifelse(alzheimer_data$Gender == 'm', 1, 0)
a1_aov = aov(GenderNumeric ~ DrugType, data = alzheimer_data)
summary(a1_aov)
#Df Sum Sq Mean Sq F value   Pr(>F)    
#DrugType      2  11.93   5.966   28.49 5.55e-12 ***
#  Residuals   278  58.21   0.209                     
#---
#  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

print(a1_aov)
#Call:
#  aov(formula = GenderNumeric ~ DrugType, data = alzheimer_data)
#
#Terms:
#  DrugType Residuals
#Sum of Squares  11.93179  58.21055
#Deg. of Freedom        2       278
#
#Residual standard error: 0.457592
#Estimated effects may be unbalanced

#This test shows a p value lower than 0.05 so its oklay to say that the proportion
# of males to females differs significantly across the different types of drugs

shapiro.test(resid(a1_aov))
#Shapiro-Wilk normality test
#
#data:  resid(a1_aov)
#W = 0.88364, p-value = 8.114e-14

install.packages('car')
library(car)
leveneTest(GenderNumeric ~ DrugType, data = alzheimer_data)
#Levene's Test for Homogeneity of Variance (center = median)
#       Df F value Pr(>F)
#group   2  0.6529 0.5213
#      278

oneway.test(GenderNumeric ~ DrugType, data = alzheimer_data)
#One-way analysis of means (not assuming equal variances)
#
#data:  GenderNumeric and DrugType
#F = 28.742, num df = 2.0, denom df = 141.7, p-value = 3.329e-11

# These are my tests to ensure the data is valid so I can trust the results
# from the aov I did on the data. The shapiro test is to ensure normality
# of the data. The levene test is to ensure homogeneity of the data, or to make
# sure the average is actually the average. The oneway test is just not assuming
# equal variances.




# a.2)
effectiveness_scale = aov(EffectivenessScale ~ DrugType, data = alzheimer_data)
summary(effectiveness_scale)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType      2   4.75  2.3769   3.991 0.0196 *
#  Residuals   278 165.59  0.5956                 
#---
#  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# This test uses a one way analysis of variance between effectiveness of each
# drug and compares them with eachother. Since the P value is less than 0.05 I
# am able to reject the null hypothesis and I can say there is a difference
# in the average of effectiveness of the drugs. The original null hypothesis
# was that there was no difference between the average effectiveness of the 
# different drugs

shapiro.test(resid(effectiveness_scale))
#Shapiro-Wilk normality test
#
#data:  resid(effectiveness_scale)
#W = 0.9921, p-value = 0.1395

# This is a check of the normality of the data ensuring the data is normal
# for the aov test I did prior. Since the p value is greater than 0.05 I 
# can confidently use this test.








# a.3)
gender_aov = aov(EffectivenessScale ~ Gender, data = alzheimer_data)
print(gender_aov)
#Call:
#  aov(formula = EffectivenessScale ~ Gender, data = alzheimer_data)
#
#Terms:
#  Gender Residuals
#Sum of Squares    2.07333 168.26866
#Deg. of Freedom         1       279
#
#Residual standard error: 0.7766038
#Estimated effects may be unbalanced

# This is the aov test that is testing the difference between 
# effectiveness of the drugs like that aov test but this one will compare
# the effectiveness between the different drugs between the genders.
# The null hypothesis would be that there is no difference between the average
# effectiveness of the drugs between the genders with the alternate hypothesis
# suggesting there is a difference. Since the p value is 0.06 and is greater
# than 0.05 I do not reject the null hypothesis. This is pretty close to making
# me want to reject the null hypothesis so I would do some further tests on
# this subject

shapiro.test(resid(gender_aov))
#Shapiro-Wilk normality test
#
#data:  resid(gender_aov)
#W = 0.9908, p-value = 0.07489

# This check is to ensure the data is normalised so I can use the welch two
# sample t test. Since the female data is normally distributed but the male
# p value is less than 0.05 we can say the male data is not normally distributed
# Since I am using the welch two sample t test this is acceptable for unequal variances

leveneTest(EffectivenessScale ~ Gender, data = alzheimer_data)
#Levene's Test for Homogeneity of Variance (center = median)
#       Df F value   Pr(>F)   
#group   1  10.761 0.001168 **
#      279                    
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# The shapiro test is to ensure normality of the data. The levene test is
# to ensure homogeneity of the variances between the data.






# bonus)
# c.1)
two_way_anova = aov(EffectivenessScale ~ DrugType + Gender, data = alzheimer_data)
summary(two_way_anova)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType      2   4.75  2.3769   3.985 0.0197 *
#  Gender        1   0.36  0.3632   0.609 0.4359  
#Residuals   277 165.22  0.5965                 
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# Since the p value for drug type is less than 0.05 I can confidently say 
# The kind of drug given has a significant impact on effectiveness of the drug.
# Since the p value for gender is over 0.05 I can confidently say the gender
# does not play a significant role in effectiveness of the drug.









# c.2)
two_way_anova_combined = aov(EffectivenessScale ~ DrugType * Gender, data = alzheimer_data)
summary(two_way_anova_combined)
#Df Sum Sq Mean Sq F value Pr(>F)  
#DrugType          2   4.75  2.3769   4.046 0.0185 *
#  Gender            1   0.36  0.3632   0.618 0.4324  
#DrugType:Gender   2   3.68  1.8391   3.131 0.0452 *
#  Residuals       275 161.55  0.5874                 
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# the drug type and gender p values back up the results from c.1 but the 
# DrugType:Gender p value shows that the gender combined with drug type can show
# the gender can have a variance between effectiveness of each drug.
















##############################################################
#Q2)
##############################################################


# a)
# I would use a two sample t test because I am comparing the averages of two 
# separate groups being the group that was taught traditionally and the 
# group that was taught using a technology enhanced approach

# b)
# (H0) There is no significant difference between the average scores of the 
# students who were taught by traditional lectures compared to the students 
# who were taught with a more interactive approach
#
# (H1) There is a significant difference between the average scores of the 
# students who were taught by traditional lectures compared to the students 
# who were taught with a more interactive approach

# c)
Scores_Group_A = c(78, 85, 92, 88, 76, 80, 85, 84, 89, 91)
Scores_Group_B = c(85, 89, 94, 91, 87, 90, 93, 88, 90, 92)
t_test_result = t.test(Scores_Group_A, Scores_Group_B)
print(t_test_result)
#Welch Two Sample t-test
#
#data:  Scores_Group_A and Scores_Group_B
#t = -2.6454, df = 13.375, p-value = 0.0198
#alternative hypothesis: true difference in means is not equal to 0
#95 percent confidence interval:
#  -9.2530613 -0.9469387
#sample estimates:
#  mean of x mean of y 
#84.8      89.9

# This shows the p value is less than 0.05 so I am rejecting the null hypothesis
# This means that the students who were taught with the more interactive
# methods and technology based approach had a higher average score than the other
# group of students. For the teaching methods if we want students to have higher
# scores most students will benefit from interactie teaching plans as opposed to 
# lectures

# d)
# The first assumption i can make is independence. Each group is independent of
# eachother meaning that the grades of students from group A dont influence the
# grades of the students from group B and vice versa.
#
#
# The second assumption is that the scores in the groups are normally distributed
# I can use a shapiro test to see if they are normally distributed.
shapiro.test(Scores_Group_A)
#Shapiro-Wilk normality test
#
#data:  Scores_Group_A
#W = 0.94902, p-value = 0.6569
shapiro.test(Scores_Group_B)
#Shapiro-Wilk normality test
#
#data:  Scores_Group_B
#W = 0.98551, p-value = 0.9878
#
# Since the p value is greather than 0.05 the data is normal
#
#
# The third assumption is that the variances between the two groups should be equal
# I can use levenes test to check the variance equality. Since this is a small
# Test with only 10 scores from each group I can see that the groups are 
# evenly represented in the test.
>>>>>>> af473381d1afa9b0bab7655fe2b92d356fdd900e
