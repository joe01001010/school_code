Daily_Sale_Before_Discount_Program = c(49971.98,
                                       49988.49,
                                       50077.94,
                                       50003.53,
                                       50006.46,
                                       50085.75,
                                       50023.05)
Daily_Sale_After_Discount_Program = c(50011.75,
                                      50040.66,
                                      50052.72,
                                      50136.20,
                                      50092.99,
                                      50095.04,
                                      50080.53)
# Setting paired to TRUE because the data is dependent on one another.
# As in each before value is paired with an after value in regards to
# the discount
t_test_result = t.test(Daily_Sale_Before_Discount_Program,
                       Daily_Sale_After_Discount_Program,
                       paired = TRUE)
print(t_test_result)
#Paired t-test
#data:  Daily_Sale_Before_Discount_Program and Daily_Sale_After_Discount_Program
#t = -2.6103, df = 6, p-value = 0.04011
#alternative hypothesis: true mean difference is not equal to 0
#95 percent confidence interval:
#  -97.615451  -3.153121
#sample estimates:
#  mean difference 
#-50.38429 