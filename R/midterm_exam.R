install.packages("nycflights13")
install.packages("dplyr")
library(nycflights13)
library(dplyr)
data(flights)



delayed_flights = flights %>%
  filter(dep_delay >= 720, arr_delay >= 1080)

print(delayed_flights)
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay carrier flight tailnum origin
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl> <chr>    <int> <chr>   <chr> 
# 1  2013     1     9      641            900      1301     1242           1530      1272 HA          51 N384HA  JFK   
# 2  2013     1    10     1121           1635      1126     1239           1810      1109 MQ        3695 N517MQ  EWR   
# 3  2013     6    15     1432           1935      1137     1607           2120      1127 MQ        3535 N504MQ  JFK   
# ℹ 6 more variables: dest <chr>, air_time <dbl>, distance <dbl>, hour <dbl>, minute <dbl>, time_hour <dttm>







flight_from_jetblue_in_summer_to_mia_or_bqn <- flights %>%
  filter(month %in% c(7, 8, 9),
         carrier == "B6",
         origin == "JFK",
         dest %in% c("MIA", "BQN"))
print(flight_from_jetblue_in_summer_to_mia_or_bqn)
# A tibble: 156 × 19
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay carrier flight tailnum origin
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl> <chr>    <int> <chr>   <chr> 
#  1  2013     7     1      111           2359        72      448            340        68 B6         839 N608JB  JFK   
#2  2013     7     1      543            545        -2      932            921        11 B6         939 N708JB  JFK   
#3  2013     7     2      123           2359        84      511            340        91 B6         839 N599JB  JFK   
#4  2013     7     2      545            545         0      926            921         5 B6         939 N554JB  JFK   
#5  2013     7     3       44           2359        45      428            340        48 B6         839 N760JB  JFK   
#6  2013     7     3      540            545        -5      933            921        12 B6         939 N547JB  JFK   
#7  2013     7     4       11           2359        12      400            340        20 B6         839 N563JB  JFK   
#8  2013     7     4      539            545        -6      918            921        -3 B6         939 N657JB  JFK   
#9  2013     7     5      542            545        -3      954            921        33 B6         939 N591JB  JFK   
#10  2013     7     5     2353           2359        -6      331            340        -9 B6         839 N661JB  JFK   
# ℹ 146 more rows
# ℹ 6 more variables: dest <chr>, air_time <dbl>, distance <dbl>, hour <dbl>, minute <dbl>, time_hour <dttm>
# ℹ Use `print(n = ...)` to see more rows









exclusive_data = flights %>%
  select(-distance, -hour, -minute, -time_hour)
print(exclusive_data)
# A tibble: 336,776 × 15
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay carrier flight tailnum origin
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl> <chr>    <int> <chr>   <chr> 
#  1  2013     1     1      517            515         2      830            819        11 UA        1545 N14228  EWR   
#2  2013     1     1      533            529         4      850            830        20 UA        1714 N24211  LGA   
#3  2013     1     1      542            540         2      923            850        33 AA        1141 N619AA  JFK   
#4  2013     1     1      544            545        -1     1004           1022       -18 B6         725 N804JB  JFK   
#5  2013     1     1      554            600        -6      812            837       -25 DL         461 N668DN  LGA   
#6  2013     1     1      554            558        -4      740            728        12 UA        1696 N39463  EWR   
#7  2013     1     1      555            600        -5      913            854        19 B6         507 N516JB  EWR   
#8  2013     1     1      557            600        -3      709            723       -14 EV        5708 N829AS  LGA   
#9  2013     1     1      557            600        -3      838            846        -8 B6          79 N593JB  JFK   
#10  2013     1     1      558            600        -2      753            745         8 AA         301 N3ALAA  LGA   
# ℹ 336,766 more rows
# ℹ 2 more variables: dest <chr>, air_time <dbl>
# ℹ Use `print(n = ...)` to see more rows










flight_operation_cost = flights %>%
  mutate(flight_operation_cost =round(((air_time / 60) * 5) + (distance * 3), digits=2))
print(flight_operation_cost)
# A tibble: 336,776 × 20
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay carrier flight tailnum origin
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl> <chr>    <int> <chr>   <chr> 
#  1  2013     1     1      517            515         2      830            819        11 UA        1545 N14228  EWR   
#2  2013     1     1      533            529         4      850            830        20 UA        1714 N24211  LGA   
#3  2013     1     1      542            540         2      923            850        33 AA        1141 N619AA  JFK   
#4  2013     1     1      544            545        -1     1004           1022       -18 B6         725 N804JB  JFK   
#5  2013     1     1      554            600        -6      812            837       -25 DL         461 N668DN  LGA   
#6  2013     1     1      554            558        -4      740            728        12 UA        1696 N39463  EWR   
#7  2013     1     1      555            600        -5      913            854        19 B6         507 N516JB  EWR   
#8  2013     1     1      557            600        -3      709            723       -14 EV        5708 N829AS  LGA   
#9  2013     1     1      557            600        -3      838            846        -8 B6          79 N593JB  JFK   
#10  2013     1     1      558            600        -2      753            745         8 AA         301 N3ALAA  LGA   
# ℹ 336,766 more rows
# ℹ 7 more variables: dest <chr>, air_time <dbl>, distance <dbl>, hour <dbl>, minute <dbl>, time_hour <dttm>,
#   flight_operation_cost <dbl>
# ℹ Use `print(n = ...)` to see more rows










numeric_values_in_flights = flights %>%
  select_if(is.numeric)
print(numeric_values_in_flights)
# A tibble: 336,776 × 14
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay flight air_time distance  hour
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl>  <int>    <dbl>    <dbl> <dbl>
#  1  2013     1     1      517            515         2      830            819        11   1545      227     1400     5
#2  2013     1     1      533            529         4      850            830        20   1714      227     1416     5
#3  2013     1     1      542            540         2      923            850        33   1141      160     1089     5
#4  2013     1     1      544            545        -1     1004           1022       -18    725      183     1576     5
#5  2013     1     1      554            600        -6      812            837       -25    461      116      762     6
#6  2013     1     1      554            558        -4      740            728        12   1696      150      719     5
#7  2013     1     1      555            600        -5      913            854        19    507      158     1065     6
#8  2013     1     1      557            600        -3      709            723       -14   5708       53      229     6
#9  2013     1     1      557            600        -3      838            846        -8     79      140      944     6
#10  2013     1     1      558            600        -2      753            745         8    301      138      733     6
# ℹ 336,766 more rows
# ℹ 1 more variable: minute <dbl>
# ℹ Use `print(n = ...)` to see more rows

removed_na = na.omit(numeric_values_in_flights)
print(removed_na)
# A tibble: 327,346 × 14
#year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time arr_delay flight air_time distance  hour
#<int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>     <dbl>  <int>    <dbl>    <dbl> <dbl>
#  1  2013     1     1      517            515         2      830            819        11   1545      227     1400     5
#2  2013     1     1      533            529         4      850            830        20   1714      227     1416     5
#3  2013     1     1      542            540         2      923            850        33   1141      160     1089     5
#4  2013     1     1      544            545        -1     1004           1022       -18    725      183     1576     5
#5  2013     1     1      554            600        -6      812            837       -25    461      116      762     6
#6  2013     1     1      554            558        -4      740            728        12   1696      150      719     5
#7  2013     1     1      555            600        -5      913            854        19    507      158     1065     6
#8  2013     1     1      557            600        -3      709            723       -14   5708       53      229     6
#9  2013     1     1      557            600        -3      838            846        -8     79      140      944     6
#10  2013     1     1      558            600        -2      753            745         8    301      138      733     6
# ℹ 327,336 more rows
# ℹ 1 more variable: minute <dbl>
# ℹ Use `print(n = ...)` to see more row

correlation_of_numeric_values_matrix = cor(removed_na)
print(correlation_of_numeric_values_matrix)
#year        month           day      dep_time sched_dep_time     dep_delay     arr_time sched_arr_time
#year              1           NA            NA            NA             NA            NA           NA             NA
#month            NA  1.000000000  5.035873e-03 -0.0037348950  -3.357651e-03 -0.0200547129 -0.002456554   -0.003144725
#day              NA  0.005035873  1.000000e+00 -0.0003927951   7.690158e-05  0.0005914318 -0.005404361   -0.002286339
#dep_time         NA -0.003734895 -3.927951e-04  1.0000000000   9.548269e-01  0.2596127216  0.662508996    0.784441987
#sched_dep_time   NA -0.003357651  7.690158e-05  0.9548268654   1.000000e+00  0.1989235050  0.644386773    0.780587438
#dep_delay        NA -0.020054713  5.914318e-04  0.2596127216   1.989235e-01  1.0000000000  0.029421007    0.160497236
#arr_time         NA -0.002456554 -5.404361e-03  0.6625089961   6.443868e-01  0.0294210074  1.000000000    0.790788769
#sched_arr_time   NA -0.003144725 -2.286339e-03  0.7844419868   7.805874e-01  0.1604972356  0.790788769    1.000000000
#arr_delay        NA -0.017382024 -3.191569e-04  0.2323057289   1.738962e-01  0.9148027589  0.024482143    0.133261288
#flight           NA  0.000980128 -8.489815e-04  0.0415301698   2.840127e-02  0.0539697456  0.025007401    0.013947226
#air_time         NA  0.010924168  2.236382e-03 -0.0146194770  -1.553213e-02 -0.0224050790  0.054296029    0.078918301
#distance         NA  0.020399044  3.215717e-03 -0.0141337335  -1.293250e-02 -0.0216809044  0.047189174    0.073613541
#hour             NA -0.003986499  4.093062e-05  0.9535149752   9.991490e-01  0.1982691535  0.644368444    0.780562047
#minute           NA  0.014983528  8.738999e-04  0.0914161536   8.310553e-02  0.0282513958  0.040746077    0.049435394
#arr_delay        flight     air_time     distance          hour       minute
#year                      NA            NA           NA           NA            NA           NA
#month          -0.0173820236  0.0009801280  0.010924168  0.020399044 -3.986499e-03 0.0149835282
#day            -0.0003191569 -0.0008489815  0.002236382  0.003215717  4.093062e-05 0.0008738999
#dep_time        0.2323057289  0.0415301698 -0.014619477 -0.014133734  9.535150e-01 0.0914161536
#sched_dep_time  0.1738961970  0.0284012732 -0.015532134 -0.012932501  9.991490e-01 0.0831055294
#dep_delay       0.9148027589  0.0539697456 -0.022405079 -0.021680904  1.982692e-01 0.0282513958
#arr_time        0.0244821433  0.0250074008  0.054296029  0.047189174  6.443684e-01 0.0407460773
#sched_arr_time  0.1332612876  0.0139472265  0.078918301  0.073613541  7.805620e-01 0.0494353936
#arr_delay       1.0000000000  0.0728620765 -0.035297087 -0.061867756  1.734556e-01 0.0215222141
#flight          0.0728620765  1.0000000000 -0.472838359 -0.481460178  2.778127e-02 0.0167562352
#air_time       -0.0352970874 -0.4728383590  1.000000000  0.990649647 -1.627728e-02 0.0170318224
#distance       -0.0618677561 -0.4814601784  0.990649647  1.000000000 -1.373050e-02 0.0184715855
#hour            0.1734555731  0.0277812678 -0.016277275 -0.013730504  1.000000e+00 0.0419314377
#minute          0.0215222141  0.0167562352  0.017031822  0.018471585  4.193144e-02 1.0000000000









mean_value = 1150
standard_deviation = 105
q2_a_distribution = qnorm(0.6, mean = mean_value, sd = standard_deviation)
q2_b_distribution = qnorm(0.8, mean = mean_value, sd = standard_deviation)
q2_c_distribution = qnorm(0.95, mean = mean_value, sd = standard_deviation)
q2_d_distribution = qnorm(0.99, mean = mean_value, sd = standard_deviation)
print(q2_a_distribution)
#[1] 1176.601
print(q2_b_distribution)
#[1] 1238.37
print(q2_c_distribution)
#[1] 1322.71
print(q2_d_distribution)
#[1] 1394.267





sample_mean = 105
standard_deviation = 10
q3_a_distribution = pnorm(120, mean = sample_mean, sd = standard_deviation)
q3_b_distribution = pnorm(80, mean = sample_mean, sd = standard_deviation)
q3_c_distribution = pnorm(115, mean = sample_mean, sd = standard_deviation) - pnorm(90, mean = sample_mean, sd = standard_deviation)
q3_d_distribution = pnorm(110, mean = sample_mean, sd = standard_deviation) - pnorm(75, mean = sample_mean, sd = standard_deviation)
print(q3_a_distribution)
#[1] 0.9331928
print(q3_b_distribution)
#[1] 0.006209665
print(q3_c_distribution)
#[1] 0.7745375
print(q3_d_distribution)
#[1] 0.6901126