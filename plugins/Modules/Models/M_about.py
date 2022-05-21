class Address():
    """
    DATA MODEL REPRESENTING A About type
    """
    About = '\\datas\\About.txt'
    FAQ = '\\datas\\FAQ.txt'
    History = '\\datas\\History.txt'

class About():
    """
    DATA MODEL REPRESENTING A About text
    """
    Type = 0
    Text = None
    def __init__(self,
        Type : int
        )->None:
        self.Type = Type
