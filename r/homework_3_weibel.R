voters = matrix(
  c(4084,2391,2433,7062,3207,1468),
  nrow = 2,
  byrow = TRUE,
  dimnames = list(
    Gender = c("Female", "Male"),
    Party = c("Democrat", "Independent", "Republican"
    )
  )
)
voters
#Party
#Gender   Democrat Independent Republican
#Female     4084        2391       2433
#Male       7062        3207       1468


X2stat = chisq.test(voters)
X2stat
#Pearson's Chi-squared test
#
#data:  voters
#X-squared = 780.32, df = 2, p-value < 2.2e-16

X2stat$statistic
#X-squared 
#780.3173

X2stat$parameter
#df 
#2

X2stat$p.value
#[1] 3.599613e-170

X2stat$observed
#Party
#Gender   Democrat Independent Republican
#Female     4084        2391       2433
#Male       7062        3207       1468

X2stat$expected
#Party
#Gender   Democrat Independent Republican
#Female 4809.328    2415.451   1683.222
#Male   6336.672    3182.549   2217.778

X2stat$residuals
#Party
#Gender     Democrat Independent Republican
#Female -10.459045  -0.4975032   18.27521
#Male     9.111787   0.4334185  -15.92113

X2stat$stdres
#Party
#Gender    Democrat Independent Republican
#Female -20.44982  -0.7728714   26.91343
#Male    20.44982   0.7728714  -26.91343