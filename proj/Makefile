MODELS=vgg_19 resnet_v2_101 inception_v4
GPUS=1 2 4 8 16 32

TABLES=$(foreach model,$(MODELS),csv/table/$(model).csv)

OBJS=README.pdf

TIMES=$(foreach m,$(MODELS),$(foreach g,$(GPUS),csv/time/$(g).$(m).csv))
TABLES=$(foreach model,$(MODELS),csv/table/$(model).csv)

OBJS+=$(TIMES) $(TABLES)

all: $(OBJS)

csv/time/%.csv: logs/%.err measure-times.sh
	bash measure-times.sh $< > $@

csv/table/%.csv: $(foreach g,$(GPUS),csv/time/$(g).%.csv) gen.py
	python gen.py $@

fig/%.png: $(TABLES) plot.py
	python plot.py

%.pdf: %.md fig/efficiency_speed.png
	pandoc $< -o $@

#.PHONY: figures tables all
