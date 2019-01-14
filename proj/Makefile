MODELS=vgg_19 resnet_v2_101 inception_v4

TABLES=$(addprefix csv/table/,$(addsuffix .csv,$(MODELS)))

all: README.pdf

csv/table/%.csv: $(wilcard logs/time.*.%.csv) gen.py
	python gen.py $@

fig/%: $(TABLES) plot.py
	python plot.py

README.pdf: README.md fig/efficiency_speed.png
	pandoc $< -o $@

.PHONY: figures all
