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
refer to
[issueTracking](##issueTracking)

2. it will become a huge file, including multiple task, maybe hard debug later, how to make it able to contain multiple task, and at the same time, clear interface to make debug easier

A regular task, which sync the Makefile in its project to here, while your working project different with your publish github project

	def setup_regular_task():
		with cd(env.app_directory):
			run('cp ~/vimwiki/diary/Makefile Makefile')

so every time I want to publish it to the git, I just run the fab cli command:

	fab setup_regular_task

should add more exception handler



## host remote, db remote connection

the ongoing project is to setup a platform for quick computation, and memory,storage deploy,现在所有的计算都是一个多核的计算,多核的内存和存储管理。

the right now frame work, fab + tencent_cloud_api+aliyun_cloud_api

but keep a stable, error traceable,is the main requirement

<!-- [连接侧漏](https://github.com/alibaba/druid/wiki/%E8%BF%9E%E6%8E%A5%E6%B3%84%E6%BC%8F%E7%9B%91%E6%B5%db) -->
[连接泄露](https://github.com/alibaba/druid/wiki/连接泄露监测)

## issueTracking

using the step debugger pudb to run the *fabfile.py*, instead of run the cli *fab*

	python -m pudb fabfile.py

when running the this line

	from fabric.api import cd, lcd, env, local,serial

it hang about more than 60 seconds sometime

turns out, this line will import tons of modules including *pynacl*,then refer this issue to [pynacl #327](https://github.com/pyca/pynacl/issues/327)

this has a more detail description [libsodium-php94](https://github.com/jedisct1/libsodium-php/issues/94)

## Test the tencent_cloud_api

this command line is to pretty print the response json from tencent cloud. I am now debug the request to the cloud service,it will fetch the json data from the response mixed with other state report data, then print out in the shell

	python test_api.py|string_io 0|python -m json.tool

and if you want to print out to webpage, and you can add the following line

	python test_api.py|string_io 0|python -m json.tool|aha > ls_with_color.html

string_io is the python file put into a PATH, where you can execute without cd to the path, and add the 'python' header.


## the cloud api almost finish, I am wondering

- pretty print the info
I have two choice here, I can throw the json file to the web, or give a very pretty print in the shell

- add new ip to the policy

