#!/usr/bin/env Rscript
library(ggplot2)

argv <- commandArgs(trailingOnly = T)
f_name <- if (length(argv) == 1) argv[1] else "poly.csv"

d  <- read.csv(f_name)

p <- ggplot(mapping=aes(y=y, x=steps)) +
	geom_line(data=subset(d, n!="best"), aes(group=n), alpha=0.1) +
	geom_line(data=subset(d, n=="best"), color="red") +
	scale_y_log10()

ggsave(paste(f_name, "pdf", sep="."), p)

