class Book(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"


# 이 파일을 직접 실행할때만 동작했으면 좋겠는 코드

if __name__ == "__main__":
    pass