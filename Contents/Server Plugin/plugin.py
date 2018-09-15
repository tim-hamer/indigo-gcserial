#! /usr/bin/env python # -*- coding: utf-8 -*-
####################

from itach import *

class Plugin(indigo.PluginBase):

############## --- Indigo Plugin Methods --- ##############

    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"GC Serial Plugin Started")

	def shutdown(self):
		self.debugLog(u"GC Serial Plugin Stopping...")

############## --- Action Methods --- ##############

    def sendCommand(self, action, device):
        ip = device.pluginProps['ipaddress']
        itach = iTach(ip)
        cmd = action.props['command']
        response = itach.raw_command(cmd)
        self.debugLog(u"GC plugin response: " + response)
