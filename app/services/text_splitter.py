import re


class TextSplitter:

    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> list[str]:

        # Step 1: Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return []

        # Step 2: Split text into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunks = []
        current_chunk = []

        current_length = 0

        # Step 3: Build chunks sentence by sentence
        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_length = len(sentence)

            # If adding this sentence exceeds chunk size
            if (
                current_length + sentence_length + 1
                > self.chunk_size
                and current_chunk
            ):

                # Save current chunk
                chunk = " ".join(current_chunk)
                chunks.append(chunk)

                # Step 4: Create overlap
                overlap_chunk = []
                overlap_length = 0

                for previous_sentence in reversed(current_chunk):

                    if overlap_length + len(previous_sentence) > self.overlap:
                        break

                    overlap_chunk.insert(0, previous_sentence)
                    overlap_length += len(previous_sentence) + 1

                current_chunk = overlap_chunk
                current_length = overlap_length

            # Add new sentence
            current_chunk.append(sentence)
            current_length += sentence_length + 1

        # Step 5: Add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks