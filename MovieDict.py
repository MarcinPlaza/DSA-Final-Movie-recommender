class MovieDict:
    def __init__(self):
        self.dict = {}

    def add_movie(self, key, movie_title):
        if key not in self.dict:
            self.dict[key] = set()
        self.dict[key].add(movie_title)

    def populate_from_dataframe(self, dataframe): # for prospective use with panda library
        for _, row in dataframe.iterrows():
            title = row['title']
            for genre in row['genres']:
                self.add_movie(genre, title)
            self.add_movie(row['director'], title)

    def find_intersection(self, keys):
        if not keys:
            return set()
        result = self.dict.get(keys[0], set())
        for key in keys[1:]:
            result &= self.dict.get(key, set())
        return result

