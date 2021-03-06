# for localized messages
from . import _

from enigma import eServiceCenter

# Configuration
from Components.config import config

# Plugin
from EPGSearch import EPGSearch, EPGSearchEPGSelection

# Plugin definition
from Plugins.Plugin import PluginDescriptor

# Mainfunction
def main(session, *args, **kwargs):
	s = session.nav.getCurrentService()
	if s:
		info = s.info()
		event = info.getEvent(0) # 0 = now, 1 = next
		name = event and event.getEventName() or ''
	else:
		name = self.session.nav.getCurrentlyPlayingServiceReference().toString()
		name = name.split('/')
		name = name[-1]
		name = name.replace('.',' ')
		name = name.split('-')
		name = name[0]
		if name.endswith(' '):
			name = name[:-1]
	if name:
		session.open(EPGSearch, name, False)
	else:
		session.open(EPGSearch)

# Event Info
def eventinfo(session, eventName="", **kwargs):
	if not eventName:
		s = session.nav.getCurrentService()
		if s:
			info = s.info()
			event = info.getEvent(0) # 0 = now, 1 = next
			eventName = event and event.getEventName() or ''
	session.open(EPGSearch, eventName)

def seachhistory(session, *args, **kwargs):
	session.open(EPGSearch, openHistory=True)

# Movielist
def movielist(session, service, **kwargs):
	serviceHandler = eServiceCenter.getInstance()
	info = serviceHandler.info(service)
	name = info and info.getName(service) or ''
	session.open(EPGSearch, name)

pluginlist = PluginDescriptor(name = _("EPGSearch"), description = _("Search EPG"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main, needsRestart = False)

def Plugins(**kwargs):
	l = [
		PluginDescriptor(
			# TRANSLATORS: EPGSearch title in EventInfo dialog (does not require further user interaction)
			# TRANSLATORS: \0x86 is non-printing and is only used to control the sort order of these WHERE_EVENTINFO entries in Screens.ButtonSetup. Please leave it as the first character in translations.
			name = _("\x86search EPG"),
			where = PluginDescriptor.WHERE_EVENTINFO,
			fnc = eventinfo,
			needsRestart = False,
		),
		PluginDescriptor(
			# TRANSLATORS: EPGSearch search from search history in EventInfo dialog (requires the user to select a history item to search for)
			# TRANSLATORS: \0x87 is non-printing and is only used to control the sort order of these WHERE_EVENTINFO entries in Screens.ButtonSetup. Please leave it as the first character in translations.
			name = _("\x87search EPG from history..."),
			where = PluginDescriptor.WHERE_EVENTINFO,
			fnc = seachhistory,
			needsRestart = False,
		),
		PluginDescriptor(
			# TRANSLATORS: EPGSearch title in MovieList (does not require further user interaction)
			description = _("search EPG"),
			where = PluginDescriptor.WHERE_MOVIELIST,
			fnc = movielist,
			needsRestart = False,
		),
		PluginDescriptor(
			# TRANSLATORS: EPGSearch search from search history in MovieList (requires the user to select a history item to search for)
			description = _("search EPG from history..."),
			where = PluginDescriptor.WHERE_MOVIELIST,
			fnc = seachhistory,
			needsRestart = False,
		),
	]

	if config.plugins.epgsearch.showinplugins.value:
		l.append(pluginlist)

	return l
