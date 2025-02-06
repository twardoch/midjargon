import itertools


def generate_phrases(options: list[str]) -> list[str]:
    results = []
    for option in options:
        # Previously the phrase was constructed via:
        # phrase = f"a {option} bird"
        # This would yield "a  bird" when option == "" or contains only whitespace.
        #
        # Updated code: strip whitespace from each word and filter out empty strings.
        phrase = " ".join(
            word.strip() for word in ["a", option, "bird"] if word.strip()
        )
        results.append(phrase)
    return results


def generate_permutations(parts: list[str]) -> list[str]:
    phrases = []
    # Assuming 'parts' is a list of lists representing optional parts
    for permutation in itertools.product(*parts):
        # Modify the line below to filter out empty strings
        phrase = " ".join(part for part in permutation if part)
        phrases.append(phrase)
    return phrases
