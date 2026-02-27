Drink_sugar = c(
  9.976959, 10.012098, 9.963002, 9.998574, 10.002431, 10.036959,
  10.014752, 9.985491, 10.026681, 9.981070, 10.011058, 9.958206,
  10.047110, 9.931327, 9.980533, 9.982266, 9.956010, 9.992339,
  9.957293, 9.907988, 9.983450, 10.018341, 9.979281, 9.931443,
  10.019777
)
t_test_result = t.test(Drink_sugar, mu = 10)

print(t_test_result)
#One Sample t-test
#data:  Drink_sugar
#t = -2.0214, df = 24, p-value = 0.05452
#alternative hypothesis: true mean is not equal to 10
#95 percent confidence interval:
#  9.972065 10.000290
#sample estimates:
#  mean of x 
#9.986178