normal.a = rnorm( n=1000, mean=0, sd=1 )
print(normal.a)
hist(normal.a)
normal.b = rnorm(n=1000)
normal.c = rnorm(n=1000)
chi.sq.3 = (normal.a)^2 + (normal.b)^2 + (normal.c)^2
hist(chi.sq.3)
scaled.chi.sq.3 = chi.sq.3 / 3
normal.d = rnorm(n=1000)
t.3 = normal.d / sqrt(scaled.chi.sq.3)
hist(t.3)
chi.sq.20 = rchisq(1000,20)
scaled.chi.sq.20 = chi.sq.20 / 20
F.3.20 = scaled.chi.sq.3 / scaled.chi.sq.20
hist(F.3.20)