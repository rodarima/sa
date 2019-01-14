all: README.pdf

README.pdf: README.md fig/*
	pandoc $< -o $@
