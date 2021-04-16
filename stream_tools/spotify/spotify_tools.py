import logging
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth


logger = logging.getLogger(__name__)


def login(
    client_id: str, client_secret: str, redirect_uri: str, scope: str
) -> spotipy.Spotify:
    api = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
        )
    )

    me = api.me()
    logger.info(f"Logged in as: {me['display_name']}")
    return api


def get_current_track(
    api: spotipy.Spotify,
    track_msg: str = "{track_name} by {artist_name}",
    no_track_msg: str = "No Track Playing",
    market: str = "US",
) -> str:
    current_track = api.current_playback(market=market)

    msg = no_track_msg
    if current_track is not None:
        item = current_track["item"]
        artists_obj = item["artists"]

        artists: List[str] = []
        for artist_obj in artists_obj:
            artists.append(artist_obj["name"])

        # Exposed Variables to Templates
        artist_name = ", ".join(artists)
        album_name = item["album"]["name"]
        track_name = item["name"]

        msg = track_msg.format(
            **{
                "track_name": track_name,
                "album_name": album_name,
                "artist_name": artist_name,
            }
        )
    return msg
