#!/usr/bin/env Rscript
library(ggplot2)

argv <- commandArgs(trailingOnly = T)

if (length(argv) == 1) {
	f_name <- argv[1]
} else {
	f_name <- "sf6.csv"
}

d  <- read.csv(f_name)
mins <- read.csv("f6_mins.csv")

p <- ggplot(mapping=aes(y=y, x=steps)) +
	geom_line(data=subset(d, n!="best"), aes(group=n), alpha=0.1) +
	geom_line(data=subset(d, n=="best"), color="red") +
	scale_y_log10() +
	geom_hline(aes(yintercept=y), mins, alpha=0.3, color="blue")

ggsave(paste(f_name, "pdf", sep="."), p)
