from kink import di
from elreda_v2 import Container

if __name__ == '__main__':
    di["dburl"] = "elreda.db"
    container = Container()
    container.init()
    container.run()