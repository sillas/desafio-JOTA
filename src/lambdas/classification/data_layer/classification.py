import json
from typing import Any
from load_model import LoadSpacyModel


class Classification:

    HIERARCHY_THRESHOLD = 1.4

    def __init__(self):

        model = LoadSpacyModel("sm")
        self.spacy_nlp = model.get_model()
        categories = self._load_categories()
        self.categories = categories["categories"]
        self.weights = categories["weights"]
        self.hierarchy = categories["hierarchy"]

    def _load_categories(self) -> dict[str, Any]:
        with open('categories.json', 'r', encoding='utf8') as file:
            return json.load(file)

    def _has_digit(self, text: str) -> bool:
        """Check if string contains any digit."""
        return any(t.isdigit() for t in text)

    def _token_filter(self, token) -> bool:
        """Filter tokens based on defined criteria."""
        return not (
            self._has_digit(token.text) or
            token.is_stop or
            token.is_punct or
            token.is_space or
            '\n' in token.text or
            '$' in token.text
        )

    def _remove_stopwords(self, text: str) -> list[str]:
        """Remove stopwords and apply token filtering."""
        doc = self.spacy_nlp(text)
        return [token.lemma_.lower() for token in doc if self._token_filter(token)]

    def _sum_weights(self, word: str, category_list: list[str], weight: float) -> float:
        """Calculate the sum of weights for matching words."""
        return sum([weight for w in category_list if (w in word) or (word in w)])

    def _analyze_words(self, words_list: list[str], weight: float = 1.0):
        """Analyze words and update category ranks."""

        ad_weights = self.weights["secondary"]
        keys = list(ad_weights.keys())
        last_word = None

        categories = self.categories

        for word in words_list:
            for category in categories:
                catg_keys = categories[category]
                catg_rank = 0

                for k in keys:
                    word_to_verify = word
                    if k == "combo_plus" and last_word:
                        word_to_verify = ','.join([last_word, word])
                    elif k == "combo_plus":
                        continue

                    catg_rank += self._sum_weights(
                        word=word_to_verify,
                        category_list=catg_keys[k],
                        weight=weight * ad_weights[k]
                    )

                self.categories_rank[category] += catg_rank

            last_word = word

    def _set_text(self, text: dict[str, str]) -> None:

        # Reset!
        self.categories_rank = {cat: 0.0 for cat in self.categories}

        self.title_words_list = self._remove_stopwords(text["title"])
        self.subtitle_words_list = self._remove_stopwords(text["subtitle"])
        self.article_words_list = self._remove_stopwords(text["article"])

    def process(self, text: dict[str, str]) -> str:
        """
        Process the text and determine the final category.

        Returns:
            str: The determined category
        """

        self._set_text(text)

        weight = self.weights["principal"]

        self._analyze_words(self.title_words_list, weight['title'])
        self._analyze_words(self.subtitle_words_list, weight['subtitle'])
        self._analyze_words(self.article_words_list, weight['article'])

        # Order categories by rank
        rank = self.categories_rank
        ordered_category_rank = sorted(
            rank.items(),
            key=lambda x: x[1],
            reverse=True
        )

        greatest_cat, greatest_value = ordered_category_rank[0]
        second_cat, second_value = ordered_category_rank[1]

        # Check if greatest value exceeds threshold
        if (greatest_value > self.HIERARCHY_THRESHOLD * second_value):
            return greatest_cat

        # Use hierarchy for close values
        hierarchy = self.hierarchy
        greatest_cat_index = hierarchy.index(greatest_cat)
        second_cat_index = hierarchy.index(second_cat)

        return greatest_cat if greatest_cat_index < second_cat_index else second_cat
