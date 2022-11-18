import json
from datetime import datetime


class SpotifyToybox:
    def __init__(self, data_file):
        self.data_file = data_file
        with open(self.data_file, "r", encoding='utf-8') as read_file:
            self.data = json.load(read_file)

    # Returns total streaming time recorded in the file
    # convert_time converts the millisecond times to a string with Hours, Minutes, and Seconds
    # sort_desc sorts the times in descending order
    # exclude_short leaves out any track that played less than a minute
    def stream_time(self, convert_time=False, exclude_short=False,
                    start_date=None, end_date=None):
        total_time = 0
        for entry in self.data:
            playtime = entry["ms_played"]
            date_string = entry["ts"][:10]
            play_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            if exclude_short and playtime < 60000:
                continue
            if start_date and play_date < start_date:
                continue
            if end_date and play_date > end_date:
                continue
            else:
                total_time += playtime
        if convert_time:
            total_time = convert_ms(total_time)
        return total_time

    # Returns total streaming time for each artist
    # convert_time converts the millisecond times to a string with Hours, Minutes, and Seconds
    # sort_desc sorts the times in descending order
    # exclude_short leaves out any track that played less than a minute
    def artist_times(self, convert_time=False, sort_desc=False, exclude_short=False,
                     start_date=None, end_date=None):
        artists = []
        artist_times = {}
        for entry in self.data:
            artist = entry["master_metadata_album_artist_name"]
            playtime = entry["ms_played"]
            # track = entry["master_metadata_track_name"]
            date_string = entry["ts"][:10]
            podcast = entry["episode_name"]
            play_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            if exclude_short and playtime < 20000:
                continue
            if start_date and play_date < start_date:
                continue
            if end_date and play_date > end_date:
                continue
            if podcast:
                continue
            if artist not in artists:
                artists.append(artist)
                artist_times[artist] = playtime
            else:
                artist_times[artist] += playtime
        if sort_desc:
            artist_times = sort_values(artist_times)
        if convert_time:
            for time in artist_times:
                artist_times[time] = convert_ms(artist_times[time])
        return artist_times

    # Returns how many times songs by each artist have been streamed
    # sort_desc sorts the artists in descending order of streams
    # exclude_short leaves out any track that played less than a minute
    def artist_streams(self, sort_desc=False, exclude_short=False,
                       start_date=None, end_date=None):
        artists = []
        artist_streams = {}
        for entry in self.data:
            artist = entry["master_metadata_album_artist_name"]
            track = entry["master_metadata_track_name"]
            playtime = entry["ms_played"]
            date_string = entry["ts"][:10]
            podcast = entry["episode_name"]
            play_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            if exclude_short and playtime < 20000:
                continue
            if start_date and play_date < start_date:
                continue
            if end_date and play_date > end_date:
                continue
            if podcast:
                continue
            if artist not in artists:
                artists.append(artist)
                artist_streams[artist] = 1
            else:
                artist_streams[artist] += 1
        if sort_desc:
            artist_streams = sort_values(artist_streams)
        return artist_streams

    # Returns the top n (default 5) artist based on streaming time
    # top_num is the number of results to return
    # convert_time converts the millisecond times to a string with Hours, Minutes, and Seconds
    def top_artists_time(self, convert_time=False, top_num=5):
        sorted_times = self.artist_times(False, True)
        top_list = list(sorted_times.items())[:top_num]
        top_artists = dict(top_list)
        if not convert_time:
            return top_artists
        else:
            for time in top_artists:
                top_artists[time] = convert_ms(top_artists[time])
            return top_artists

    # Returns the top n (default 5) artist based on number of song streams
    # top_num is the number of results to return
    def top_artists_streams(self, top_num=5):
        sorted_streams = self.artist_streams(True, True)
        top_list = list(sorted_streams.items())[:top_num]
        top_artists = dict(top_list)
        return top_artists


# Helper method to convert millisecond time to a more readable string of Hours, Minutes, Seconds
def convert_ms(ms):
    secs = int((ms/1000) % 60)
    mins = int((ms/(1000 * 60)) % 60)
    hrs = int(ms/(1000*60*60))
    if hrs != 0:
        return "%d hours, %d minutes, %d seconds" % (hrs, mins, secs)
    else:
        return "%d minutes, %d seconds" % (mins, secs)


# Helper method to sort values in descending order
def sort_values(values):
    # This funky line of code sorts all the results in descending order based on values
    sorted_values = dict(reversed(sorted(values.items(), key=lambda kv: kv[1])))
    return sorted_values


# Takes a list of json files and combines them together into one new file
# Useful because Spotify sends data in multiple files
def combine_json(files=[], new_filename="combined.json"):
    res_file = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as addfile:
            res_file.extend(json.load(addfile))
    with open(new_filename, 'w', encoding='utf-8') as output:
        json.dump(res_file, output)


# Takes a json file and removes all data not relevant to this library
# Combined files tend to be extremely large and hard to work with
def clean_json(file, new_file="clean.json"):
    with open(file, 'r', encoding='utf-8') as readfile:
        content = json.load(readfile)
        print(content)
