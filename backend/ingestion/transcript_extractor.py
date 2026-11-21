
import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extract and validate the YouTube video ID.
    Supports regular videos, Shorts, embeds and youtu.be links.
    """

    parsed_url = urlparse(url.strip())
    hostname = (parsed_url.hostname or "").lower()

    allowed_domains = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "www.youtu.be",
    }

    if hostname not in allowed_domains:
        raise ValueError(f"Invalid YouTube URL: {url}")

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed_url.path.strip("/").split("/")[0]

    elif parsed_url.path == "/watch":
        video_id = parse_qs(parsed_url.query).get("v", [""])[0]

    elif parsed_url.path.startswith(("/shorts/", "/embed/", "/live/")):
        parts = parsed_url.path.strip("/").split("/")
        video_id = parts[1] if len(parts) >= 2 else ""

    else:
        raise ValueError(f"Invalid YouTube URL: {url}")

    if not re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        raise ValueError(f"Invalid YouTube video ID: {video_id}")

    return video_id


def fetch_transcript(url: str, language: str = "en") -> dict:
    """
    Fetch the YouTube transcript and preserve timestamps.
    """

    video_id = extract_video_id(url)

    youtube_api = YouTubeTranscriptApi()

    transcript = youtube_api.fetch(
        video_id,
        languages=[language]
    )

    segments = transcript.to_raw_data()

    return {
        "video_id": video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "segments": segments
    }

import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extract and validate the YouTube video ID.
    Supports regular videos, Shorts, embeds and youtu.be links.
    """

    parsed_url = urlparse(url.strip())
    hostname = (parsed_url.hostname or "").lower()

    allowed_domains = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "www.youtu.be",
    }

    if hostname not in allowed_domains:
        raise ValueError(f"Invalid YouTube URL: {url}")

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed_url.path.strip("/").split("/")[0]

    elif parsed_url.path == "/watch":
        video_id = parse_qs(parsed_url.query).get("v", [""])[0]

    elif parsed_url.path.startswith(("/shorts/", "/embed/", "/live/")):
        parts = parsed_url.path.strip("/").split("/")
        video_id = parts[1] if len(parts) >= 2 else ""

    else:
        raise ValueError(f"Invalid YouTube URL: {url}")

    if not re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        raise ValueError(f"Invalid YouTube video ID: {video_id}")

    return video_id


def fetch_transcript(url: str, language: str = "en") -> dict:
    """
    Fetch the YouTube transcript and preserve timestamps.
    """

    video_id = extract_video_id(url)

    youtube_api = YouTubeTranscriptApi()

    transcript = youtube_api.fetch(
        video_id,
        languages=[language]
    )

    segments = transcript.to_raw_data()

    return {
        "video_id": video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "segments": segments
    }
