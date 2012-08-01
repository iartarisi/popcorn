# Makefile.am for popcorn/src

yncludedir = @yncludedir@/popcorn

client_DATA =			\
	popcorn.ycp		\
	popcorn_auto.ycp	\
	popcorn_proposal.ycp

ynclude_DATA =			\
	helps.ycp		\
	wizards.ycp		\
	dialogs.ycp		\
	complex.ycp

desktop_DATA =			\
	popcorn.desktop

module_DATA =			\
	Popcorn.ycp		\
	Popcorn2.pm		\
	Popcorn3.py

# create a symlink for local build, #145327
popcorn:
	ln -sf . $@
ycpchook = popcorn

EXTRA_DIST = $(client_DATA) $(ynclude_DATA) $(module_DATA) $(desktop_DATA)

include $(top_srcdir)/Makefile.am.common
