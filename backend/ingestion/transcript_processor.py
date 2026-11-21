
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """
    Clean unnecessary whitespace and formatting from transcript text.
    """

    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text


def process_transcript(
    segments: list,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list:
    """
    Clean transcript segments and divide them into chunks.
    Preserve timestamps for every chunk.
    """

    if not segments:
        raise ValueError("Transcript is empty.")

    # Clean individual transcript segments
    cleaned_segments = []

    for segment in segments:
        text = clean_text(segment["text"])

        if not text:
            continue

        cleaned_segments.append({
            "text": text,
            "start": float(segment["start"]),
            "end": float(segment["start"]) + float(segment["duration"])
        })

    # Combine transcript segments while retaining their time boundaries
    full_text = " ".join(
        segment["text"] for segment in cleaned_segments
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "। ", ". ", " ", ""]
    )

    text_chunks = splitter.split_text(full_text)

    # Match each chunk to its approximate timestamp range
    chunks = []
    search_position = 0

    for index, chunk_text in enumerate(text_chunks):

        chunk_start_position = full_text.find(
            chunk_text,
            max(0, search_position - chunk_overlap)
        )

        if chunk_start_position == -1:
            chunk_start_position = search_position

        chunk_end_position = chunk_start_position + len(chunk_text)

        overlapping_segments = [
            segment for segment in cleaned_segments
            if (
                segment["end"] >= 0
                and segment["start"] >= 0
            )
        ]

        # Find transcript segments overlapping this chunk's text
        current_position = 0
        matched_segments = []

        for segment in overlapping_segments:
            segment_start = current_position
            segment_end = current_position + len(segment["text"])

            if (
                segment_end >= chunk_start_position
                and segment_start <= chunk_end_position
            ):
                matched_segments.append(segment)

            current_position = segment_end + 1

        start_time = (
            matched_segments[0]["start"]
            if matched_segments else 0.0
        )

        end_time = (
            matched_segments[-1]["end"]
            if matched_segments else 0.0
        )

        chunks.append({
            "chunk_id": index,
            "text": chunk_text,
            "start_time": start_time,
            "end_time": end_time
        })

        search_position = chunk_start_position + len(chunk_text)

    return chunks
