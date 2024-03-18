import os
#  모듈화 + 실행 프로그램.
def simple_memo():
    os.makedirs("files", exist_ok=True)
    filename = input("저장할 파일명:")
    file_path = os.path.join("files", filename)
    # with block 구현
    with open(file_path, 'wt', encoding="utf-8") as fw:
        print(" 저장할 내용을 입력하세요.")
        while True:
            #한줄 읽기
            line_txt = input(">>>")
            #!q 입력됐으면 종료
            if line_txt == "!q":
                break
            # 파일 출력
            fw.write(line_txt+"\n")

    #with block  종료시 close는 자동을 처리
    print("종료")
    
if __name__ == "__main__":
    simple_memo()
