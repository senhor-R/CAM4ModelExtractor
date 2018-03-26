from re import match


class Filter:
    name = ""
    title = ""
    url = ""
    country = ""
    gender = ""
    orientation = ""
    exportToCapture = False

    def __init__(self, name="-1", title=".*", url=".*", country=".*", gender=".*", orientation=".*", exportToCapture=False):
        self.name = name
        self.title = title
        self.url = url
        self.country = country
        self.gender = gender
        self.orientation = orientation
        self.exportToCapture = exportToCapture

    def __str__(self):
        return "Name:" +self.name + "\n" + \
               "Title: " + self.title + "\n" + \
               "URL: " + self.url + "\n" + \
               "Country: " + self.country + "\n" + \
               "Gender: " + self.gender + "\n" + \
               "Orientation: " + self.orientation + "\n" + \
               "exportToCapture: " + str(self.exportToCapture)

    @staticmethod
    def parseJson(json):
        return Filter(json["name"], json["title"], json["url"], json["country"], json["gender"], json["orientation"], json["exportToCapture"])


class Profile:
    title = ""
    url = ""
    country = ""
    gender = ""
    orientation = ""

    def __init__(self, title="", url="", country="N/A", gender="N/A", orientation="N/A"):
        self.title = title
        self.url = url
        self.country = country
        self.gender = gender
        self.orientation = orientation

    def filtermatch(self, Filter):
        if match(Filter.title, self.title) is None:
            return False
        if match(Filter.url, self.url) is None:
            return False
        if match(Filter.country, self.country) is None:
            return False
        if match(Filter.gender, self.gender) is None:
            return False
        if match(Filter.orientation, self.orientation) is None:
            return False
        return True

    def __str__(self):
        return "Title: " + self.title + "\n" + \
               "URL: " + self.url + "\n" + \
               "Country: " + self.country + "\n" + \
               "Gender: " + self.gender + "\n" + \
               "Orientation: " + self.orientation + "\n"

    def __repr__(self):
        return self.url