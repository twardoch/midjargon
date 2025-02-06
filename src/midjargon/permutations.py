def generate_phrases(options: list[str]) -> list[str]:
    results = []
    for option in options:
        # Previously the phrase was constructed via:
        # phrase = f"a {option} bird"
        # This would yield "a  bird" when option == "" or contains only whitespace.
        #
        # Updated code: strip whitespace from each word and filter out empty strings.
        phrase = " ".join(word.strip() for word in ["a", option, "bird"] if word.strip())
        results.append(phrase)
    return results 