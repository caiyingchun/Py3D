

##
# Simple dictionairy class that automatically initializes lists if
# they are not present in the collection yet.
##
class VectorList(dict):

    def __missing__(self, key):
        self[key] = []
        return self[key]
