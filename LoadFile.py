import os
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen
import string
from MusicBrainzMeta import MusicBrainzMeta

class LoadFile(MusicBrainzMeta):
	def __init__(self, fileName):
		super(LoadFile, self).__init__()
		self.fileName = fileName
		t, self.extension = os.path.splitext(fileName)
	
		self.__f = mutagen.File(fileName)
		if self.__f is None:
#			print "Unknown file type: ", fileName
			return

		if 'audio/x-flac' in self.__f.mime:
			### FLAC file
			self.extension = '.flac'
			self.__flac()
		elif 'audio/mp3' in self.__f.mime:
			### MP3
			self.extension = '.mp3'
			self.__mp3()
		elif 'audio/vorbis' in self.__f.mime:
			### Ogg
			self.extension = '.ogg'
			self.__ogg()
		elif 'audio/x-mpc' in self.__f.mime:
			### Musepack
			print 'MPC filem', fileName
			self.extension = '.mpc'
#			self.__mpc()
		elif 'audio/mp4' in self.__f.mime:
			### MP4
			self.extension = '.mp4'
			print "MP4", fileName
#			print f
#			return False
		elif 'audio/ape' in self.__f.mime:
			### APE
			print "APE", fileName
#			print f
#			return False
		else:
			print "Unknown file ", fileName, " type: ", self.__f.mime
			#print "Unknown file type: ", self.__f.mime

	def __ogg(self):
		# mapping of names
		nmap = {
				'musicbrainz_albumid': 'musicBrainz_AlbumId',
				'musicbrainz_albumartistid': 'musicBrainz_AlbumArtistId',
				'musicbrainz_artistid': 'musicBrainz_ArtistId',
				'musicbrainz_trackid': 'musicBrainz_TrackId', 
				'artist': 'artist',
				'albumartist': 'albumartist',
				'album': 'album',
				'title': 'title',
				'date': 'date',
				'totaldiscs': 'totaldiscs',
				'discnumber': 'discnumber',
				'tracknumber': 'tracknumber',
				'tracktotal': 'tracktotal',
				}
		# now parse
#		print 'Parsing ogg file ', self.fileName
		for k, v in self.__f.iteritems():
			try:
				target = nmap[k]
				value = unicode(v[0])
				if len(value) == 0:
					self[target] = None
				else:
					self[target] = value
			except:
				continue
#				print 'Unknown key: ', k, '--->', v

		self.isMusicBrainz = ( (not (self['musicBrainz_AlbumId'] is None)) and
				(not (self['musicBrainz_AlbumArtistId'] is None)) and
				(not (self['musicBrainz_ArtistId'] is None)) and
				(not (self['musicBrainz_TrackId'] is None)) )

#		for k, v in self.iteritems():
#			print k, '-->', v

	def __mp3(self):
		# mapping of names
		nmap = {
				'TXXX:MusicBrainz Album Id': 'musicBrainz_AlbumId',
				'TXXX:MusicBrainz Album Artist Id': 'musicBrainz_AlbumArtistId',
				'TXXX:MusicBrainz Artist Id': 'musicBrainz_ArtistId',
				'TXXX:MusicBrainz Track Id': 'musicBrainz_TrackId', 
				'TPE1': 'artist',
				'TPE2': 'albumartist',
				'TALB': 'album',
				'TIT2': 'title',
				'TDRC': 'date',
				}
		# now parse
		for k,v in self.__f.iteritems():
#			print k, '--->', v
			# more complicate to parse tags
			if k == 'UFID:http://musicbrainz.org':
				trackId = unicode(v).partition(',')
				trackId = trackId[2].partition('=')
				self['musicBrainz_TrackId'] = trackId[2][1:-2]
			elif k == 'TRCK':
				## parse track number
				curr, sep, tot = unicode(v).partition('/')
				self['tracknumber'] = curr
				if sep != '':
					self['tracktotal'] = tot
			elif k == 'TPOS':
				## parse media set number
				curr, sep, tot = unicode(v).partition('/')
				self['discnumber'] = curr
				if sep != '' and len(tot) > 0:
					self['totaldiscs'] = tot
			else:
				# simple to parse tags
				try:
					target = nmap[k]
					self[target] = unicode(v)
#					print k, ' (', target, ') ---> ', v
				except:
					continue
			
		self.isMusicBrainz = ( (not (self['musicBrainz_AlbumId'] is None)) and
				(not (self['musicBrainz_AlbumArtistId'] is None)) and
				(not (self['musicBrainz_ArtistId'] is None)) and
				(not (self['musicBrainz_TrackId'] is None)) )
	
	def __flac(self):
		# mapping of names
		nmap = {
				'musicbrainz_albumid': 'musicBrainz_AlbumId',
				'musicbrainz_albumartistid': 'musicBrainz_AlbumArtistId',
				'musicbrainz_artistid': 'musicBrainz_ArtistId',
				'musicbrainz_trackid': 'musicBrainz_TrackId', 
				'artist': 'artist',
				'albumartist': 'albumartist',
				'album': 'album',
				'title': 'title',
				'date': 'date',
				'totaldiscs': 'totaldiscs',
				'discnumber': 'discnumber',
				'tracknumber': 'tracknumber',
				'tracktotal': 'tracktotal',
				}
		# now parse
#		print 'Parsing flac file ', self.fileName
		for k, v in self.__f.iteritems():
			value = unicode(v[0])
			try:
				target = nmap[k]
				if len(value) == 0:
					self[target] = None
				else:
					self[target] = value
			except:
				continue

		self.isMusicBrainz = ( (not (self['musicBrainz_AlbumId'] is None)) and
				(not (self['musicBrainz_AlbumArtistId'] is None)) and
				(not (self['musicBrainz_ArtistId'] is None)) and
				(not (self['musicBrainz_TrackId'] is None)) )

#		print '---------- Parsed ----------'
#		print 'Is music brainzed ', self.isMusicBrainz
#		for k, v in self.iteritems():
#			print k, '-->', v
	
	def __mpc(self):
		# mapping of names
		nmap = {
				'musicbrainz_albumid': 'musicBrainz_AlbumId',
				'musicbrainz_albumartistid': 'musicBrainz_AlbumArtistId',
				'musicbrainz_artistid': 'musicBrainz_ArtistId',
				'musicbrainz_trackid': 'musicBrainz_TrackId', 
				'artist': 'artist',
				'albumartist': 'albumartist',
				'album': 'album',
				'title': 'title',
				'date': 'date',
				'totaldiscs': 'totaldiscs',
				'discnumber': 'discnumber',
				'tracknumber': 'tracknumber',
				'tracktotal': 'tracktotal',
				}
		# now parse
		print 'Parsing mpc file ', self.fileName
		for k, v in self.__f.iteritems():
			print k, '-->', v
			try:
				target = nmap[k]
				self[target] = unicode(v)
			except:
				continue
#				print 'Unknown key: ', k, '--->', v

		self.isMusicBrainz = ( (not (self['musicBrainz_AlbumId'] is None)) and
				(not (self['musicBrainz_AlbumArtistId'] is None)) and
				(not (self['musicBrainz_ArtistId'] is None)) and
				(not (self['musicBrainz_TrackId'] is None)) )

		print '---------- Parsed ----------'
		print 'Is music brainzed ', self.isMusicBrainz
		for k, v in self.iteritems():
			print k, '-->', v
