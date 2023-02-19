"""
utility functions for playlist organizer script
"""

# return tuple for primary, secondary, tertiary key to sort based on
def sortby_artist(t):
    return (t['artist'], t['date'], t['track_num'])

def sortby_era(t):
    return (t['date'], t['track_num'])

# convert 'item' to 'track' and extract id + sorting key attributes
def exTRACKt(item):
    track = item['track']
    return {
        'id': track['id'],
        'artist': track['artists'][0]['name'].lower(),
        'date': track['album']['release_date'],
        'track_num': track['track_number']
    }

