class MusicBrainzMeta(dict):
	def __init__(self, *args, **kwargs):
		self.isMusicBrainz = False

		super(MusicBrainzMeta, self).__init__(*args, **kwargs)
		self['musicBrainz_AlbumArtistId'] = None
		self['musicBrainz_AlbumId'] = None
		self['musicBrainz_ArtistId'] = None
		self['musicBrainz_TrackId'] = None

		self['discnumber'] = None
		self['totaldiscs'] = None
		self['tracknumber'] = None
		self['tracktotal'] = None
		self['date'] = None
		self['album'] = None
		self['albumartist'] = None
		self['title'] = None
		self['artist'] = None
