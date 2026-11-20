# WALK-G pilot: primary analysis
# Written by a co-author before the code review. Run: Rscript analysis_v1.R
library(dplyr)

readings <- read.csv("data/readings.csv")
participants <- read.csv("data/participants.csv")

# drop meter errors
readings <- readings %>% filter(glucose != 999)

# add arm and covariates to every reading
d <- left_join(readings, participants, by = "subject")

# primary outcome: post-meal glucose at visit 2
v2 <- d %>% filter(visit == 2, time_of_day == "post_meal")

cat("Readings analysed:", nrow(v2), "\n")
print(v2 %>% group_by(arm) %>% summarise(n = n(), mean = mean(glucose), sd = sd(glucose)))

res <- t.test(glucose ~ arm, data = v2)
print(res)
diff <- unname(res$estimate[2] - res$estimate[1])
cat(sprintf("Walking minus usual: %.1f mg/dL (95%% CI %.1f to %.1f), p = %.2g\n",
            diff, -res$conf.int[2], -res$conf.int[1], res$p.value))
