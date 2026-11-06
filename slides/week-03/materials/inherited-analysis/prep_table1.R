# table 1 for the sleep paper
# (written by the RA who left; runs, but nobody has checked it since)
library(readr)
library(dplyr)

d <- read_csv("survey.csv", show_col_types = FALSE)
d <- na.omit(d)
d <- d %>% filter(age >= 18)
d$depressed <- ifelse(d$phq9 >= 10, 1, 0)

tab <- d %>% summarise(
  n = n(),
  age = round(mean(age), 1),
  female_pct = round(100 * mean(sex == "F"), 1),
  phq9 = round(mean(phq9), 2),
  depressed_pct = round(100 * mean(depressed), 1),
  sleep_hours = round(mean(sleep_hours), 2)
)
print(as.data.frame(tab))
write_csv(tab, "table1.csv")
