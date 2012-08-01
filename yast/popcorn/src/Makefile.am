# Makefile.am for popcorn/src

yncludedir = @yncludedir@/popcorn

client_DATA =			\
	popcorn.ycp

ynclude_DATA =			\
	wizards.ycp		\
	dialogs.ycp

desktop_DATA =			\
	popcorn.desktop

module_DATA =			\
	Popcorn.ycp

# create a symlink for local build, #145327
popcorn:
	ln -sf . $@
ycpchook = popcorn

EXTRA_DIST = $(client_DATA) $(ynclude_DATA) $(module_DATA) $(desktop_DATA)

include $(top_srcdir)/Makefile.am.common
