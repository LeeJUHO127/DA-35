def greet(name):
    print(f"{name}님 안녕하세요")

def get_greet(name):
    return f"{name}님 안녕하세요"

class Hello:

    def __init__(self, name):
        self.name = name

    def eng_greet(self):
        return f"Hello {self.name}."

    def kor_greet(self):
        return f"안녕하세요 {self.name}님."

print(__name__)
if __name__ == "__main__":
    greet("홍길동")
    t = get_greet("이순신")
    print(t)




        