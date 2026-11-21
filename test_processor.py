
from backend.ingestion.transcript_extractor import fetch_transcript
from backend.ingestion.transcript_processor import process_transcript


# YouTube video URL
video_url = "https://youtu.be/O_ewDn_vVz8"

print("Fetching YouTube transcript...")

# Step 1: Extract transcript
transcript = fetch_transcript(video_url, language="hi")

print("Transcript fetched successfully!")

# Step 2: Process transcript
print("\nCleaning and splitting transcript...")

chunks = process_transcript(
    transcript["segments"],
    chunk_size=1000,
    chunk_overlap=200
)

# Step 3: Display results
print("\nTranscript Processing Completed!")
print("Total transcript segments:", len(transcript["segments"]))
print("Total chunks created:", len(chunks))

print("\nFirst 3 chunks:\n")

for chunk in chunks[:3]:
    print("-" * 60)
    print("Chunk ID:", chunk["chunk_id"])
    print("Start Time:", chunk["start_time"])
    print("End Time:", chunk["end_time"])
    print("Text:", chunk["text"][:300])
