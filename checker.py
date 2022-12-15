from answers import bad_words


class Checker:

    @staticmethod
    def check_bad_words(text: str) -> bool:
        for w in bad_words:
            if w in text:
                return True

        return False
