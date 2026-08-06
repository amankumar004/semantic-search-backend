class TextSplitter:
    def __init__(self, chunk_size: int = 100, overlap: int = 10):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_text(self, text: str) -> list[str]:
        """
        Splits the input text into chunks of specified size with overlap.

        :param text: The input text to be split.
        :return: A list of text chunks.
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap  # Move start forward with overlap

        return chunks