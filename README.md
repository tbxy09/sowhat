## using pandoc to create a onepage look for my vimwiki diary
I am struggling for lazy reviewing my diary quit time,finally,onepage is the most comfort way for me.

- use bash command to create a md file including all
```
cat *.md > all.md
```

- create a makefile for coveting  md to html using pandoc, run make under my folder including all the files I want to convert


```
make
```



this is what I found for the base line almost working(except some changes to the
dated option *-- smart* ) thank to
[kristopherjohnson/Makefile](https://gist.github.com/kristopherjohnson/7466917)

here is working version, print out ugly but temporally is what I need

	# Makefile
	#
	# Converts Markdown to other formats (HTML, PDF, DOCX, RTF, ODT, EPUB) using Pandoc
	# <http://johnmacfarlane.net/pandoc/>
	#
	# Run "make" (or "make all") to convert to all other formats
	#
	# Run "make clean" to delete converted files

	# Convert all files in this directory that have a .md suffix
	SOURCE_DOCS := $(wildcard *.md)

	EXPORTED_DOCS=\
	 $(SOURCE_DOCS:.md=.html) \
	 $(SOURCE_DOCS:.md=.pdf) \
	 $(SOURCE_DOCS:.md=.docx) \
	 $(SOURCE_DOCS:.md=.rtf) \
	 $(SOURCE_DOCS:.md=.odt) \
	 $(SOURCE_DOCS:.md=.epub)


	HTML_FILES=$(MD_FILES:.md=.html)
	BUILD_HTML_FILES=$(HTML_FILES:%=build/%)



	PANDOC=/usr/bin/pandoc

	PANDOC_OPTIONS=--standalone

	PANDOC_HTML_OPTIONS=--to html5
	PANDOC_PDF_OPTIONS=
	PANDOC_DOCX_OPTIONS=
	PANDOC_RTF_OPTIONS=
	PANDOC_ODT_OPTIONS=
	PANDOC_EPUB_OPTIONS=--to epub3


	# Pattern-matching Rules

	%.html : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_HTML_OPTIONS) -o $@ $<

	%.pdf : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_PDF_OPTIONS) -o $@ $<

	%.docx : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_DOCX_OPTIONS) -o $@ $<

	%.rtf : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_RTF_OPTIONS) -o $@ $<

	%.odt : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_ODT_OPTIONS) -o $@ $<

	%.epub : %.md
		$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_EPUB_OPTIONS) -o $@ $<

	# all: $(BUILD_HTML_FILES)
	all : $(EXPORTED_DOCS)

#### add the toc option

I would like have a header proposer function in my vimwiki diary,firstly I need to have a TOC, Luckly, pandoc have the option can generate a TOC, no need to include new plugin.just update the make file ,add new pandoc option.


#### setup the fab to do the manage work

fab is a python package you used to manage the web server resources, it use ssh to login and do some setup and maintenance work for the web dev project

* NOT SATISFIED

1. the traceback err report not working when running the fab,it just hang there

2. it will become a huge file, including multiple task, maybe hard debug later, how to make it able to contain multiple task, and at the same time, clear interface to make debug easier

A regular task, which sync the Makefile in its project to here, while your working project different with your publish github project

	def setup_regular_task():
		with cd(env.app_directory):
			run('cp ~/vimwiki/diary/Makefile Makefile')

so every time I want to publish it to the git, I just run the fab cli command:

	fab setup_regular_task




