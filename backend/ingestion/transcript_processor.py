
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """Clean unnecessary whitespace from transcript text."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_transcript(
    segments: list,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list:
    """
    Clean transcript, create overlapping chunks,
    and preserve their approximate video timestamps.
    """

    if not segments:
        raise ValueError("Transcript is empty.")

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative and smaller than chunk size."
        )

    cleaned_segments = []
    full_text_parts = []
    current_position = 0

    # Step 1: Clean text and track character positions
    for segment in segments:
        text = clean_text(segment["text"])

        if not text:
            continue

        if full_text_parts:
            current_position += 1  # Space between segments

        char_start = current_position
        char_end = char_start + len(text)

        start_time = float(segment["start"])
        end_time = start_time + float(segment["duration"])

        cleaned_segments.append({
            "text": text,
            "start": start_time,
            "end": end_time,
            "char_start": char_start,
            "char_end": char_end
        })

        full_text_parts.append(text)
        current_position = char_end

    if not cleaned_segments:
        raise ValueError("No usable transcript text found.")

    full_text = " ".join(full_text_parts)

    # Step 2: Create overlapping text chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "। ", ". ", " ", ""],
        add_start_index=True
    )

    documents = splitter.create_documents([full_text])

    # Step 3: Match chunks with original transcript timestamps
    chunks = []

    for index, document in enumerate(documents):
        chunk_text = document.page_content
        chunk_start = document.metadata["start_index"]
        chunk_end = chunk_start + len(chunk_text)

        matched_segments = [
            segment for segment in cleaned_segments
            if (
                segment["char_start"] < chunk_end
                and segment["char_end"] > chunk_start
            )
        ]

        if not matched_segments:
            continue

        chunks.append({
            "chunk_id": index,
            "text": chunk_text,
            "start_time": matched_segments[0]["start"],
            "end_time": matched_segments[-1]["end"]
        })

    return chunks
