from backend.ingestion.transcript_extractor import fetch_transcript

def main():

    print("*"*50)
    print("     Youtube - Transcript Extractor")
    print("*"*50)

    video_url = input("Enter the YouTube video URL: ")

    try:
        result = fetch_transcript(video_url, language="hi")

        print("\nVideo ID:", result["video_id"])
        print("Language:", result["language"])
        print("Language Code:", result["language_code"])
        print("Auto Generated:", result["is_generated"])

        print("\nTranscript Preview:\n")

        for segment in result["segments"][:10]:
            print(f"[{segment['start']:.2f}s] {segment['text']}")

        print("\nTotal Transcript Segments:", len(result["segments"]))
        print("\nTranscript extraction completed successfully.")

    except Exception as e:
        print("\nTranscript extraction failed:!")
        print("Reason:", e)

if __name__ == "__main__":
    main()