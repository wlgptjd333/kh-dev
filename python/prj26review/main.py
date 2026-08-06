import csv


# data.csv 파일 연결 (쓰기 모드)
def f01() -> None:
    with open("data.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows([
            ["name", 2, 3],
            ["홍길동", 5, 6],
            [7, 8, 9]
        ])


# data.csv 파일 연결 (읽기 모드)
def f02() -> None:
    with open("data.csv", "r", encoding="utf-8") as f:
        data = csv.reader(f)
        for row in data:
            print(row)


# dict 기반 (write) - 나스닥 데이터 추가
def f03() -> None:
    # 나스닥 주요 기업들의 정보를 딕셔너리 리스트로 구성
    data = [
        {"ticker": "AAPL", "company": "Apple Inc.", "price": 175.50, "sector": "Technology"},
        {"ticker": "MSFT", "company": "Microsoft", "price": 330.11, "sector": "Technology"},
        {"ticker": "TSLA", "company": "Tesla", "price": 240.50, "sector": "Consumer Discretionary"},
        {"ticker": "NVDA", "company": "NVIDIA", "price": 450.25, "sector": "Technology"},
        {"ticker": "GOOGL", "company": "Alphabet", "price": 135.40, "sector": "Communication Services"}
    ]

    with open("data.csv", "w", encoding="utf-8", newline="") as f:
        # 데이터의 키(Key) 값들과 동일하게 fieldnames 설정
        fieldnames = ["ticker", "company", "price", "sector"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()  # 첫 줄에 제목(ticker, company, price, sector) 쓰기
        writer.writerows(data)  # 리스트 안의 모든 딕셔너리 데이터 쓰기

    print("나스닥 데이터가 data.csv 파일에 성공적으로 저장되었습니다!\n")


# dict 기반 (read) - 저장된 나스닥 데이터 읽어오기
def f04() -> None:
    with open(r"data.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


# 함수 실행
f03()
f04()