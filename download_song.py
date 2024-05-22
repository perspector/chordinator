import scraper


song_name = "Shake It Off"

with open("downloaded_song.txt", "w") as offline_song_file:
	for chord in scraper.get_chords(song_name):
		offline_song_file.write(chord + "\n")
