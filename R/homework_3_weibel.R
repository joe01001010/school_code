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
