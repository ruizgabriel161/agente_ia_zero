from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int

    if __name__ == "__main__":
        p1 = Person()
