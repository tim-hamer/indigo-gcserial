#! /usr/bin/env python # -*- coding: utf-8 -*-
####################

from itach import *
from struct import *
import binascii

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

    def parseResponse(self, devicetype, response):
        if devicetype == "receiver":
            self.parseReceiverResponse(response)
        elif devicetype == "tv":
            self.parseTVResponse(response)
        elif devicetype == "elan":
            self.parseElanResponse(response)

    def parseReceiverResponse(self,response):
        if response.startswith('VOL'):
            volume = response[3:]
            self.debugLog(u"Volume: " + volume)
            volumeVar = indigo.variables[417571981]
            indigo.variable.updateValue(volumeVar, volume)
        elif response.startswith('MUT0'):
            self.debugLog(u"Mute On")
            volumeVar = indigo.variables[417571981]
            indigo.variable.updateValue(volumeVar, 'MUTE')

    def parseTVResponse(self, response):
        # TODO: Figure out pioneer responses
        self.debugLog(u"TV response not implemented yet")

    def parseElanResponse(self, response):
        data = unpack_from('!cccccccccccccccccccccccccccccccccccc', response[11:])
        self.debugLog(data)
        zone1 = data[0:5]
        zone2 = data[6:11]
        zone3 = data[12:17]
        self.debugLog(zone1)
        zone1Pwr = zone1[0]
        self.debugLog(zone1Pwr)
        zone1Bin = bin(int(zone1Pwr, base=16))
        self.debugLog(zone1Bin)

    def prepCommand(self, devicetype, cmd):
        if devicetype == "tv":
            return '\x02' + cmd + '\x03'
        return cmd

    def sendCommand(self, action, device):
        try:
            ip = device.pluginProps['ipaddress']
            port = device.pluginProps['port']
            devicetype = device.pluginProps['devicetype']
            cmd = action.props['command']

            command = self.prepCommand(devicetype, cmd)
            itach = iTach(ip, port)
            response = itach.raw_command(command)
            self.debugLog(u"GC plugin response: " + response)
            self.parseResponse(devicetype, response)
        except:
            self.debugLog(u"Caught Exception")
            self.debugLog(sys.exc_info()[0])
