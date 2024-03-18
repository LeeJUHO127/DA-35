import os
def my_memo():
    save_dir = "save_files"
    os.makedirs(save_dir, exist_ok=True)
    
    # 파일명 입력 받기
    print("저장할 파일의 이름을 입력하세요")
    file_name = input("파일명: ")
    file_path = os.path.join(save_dir, file_name)
    
    # 파일과 연결해서 출력 작업 
    ##  표준입력(input) -> p/g -> 파일에 출력
    print(file_path, "에 작성합니다.")
    with open(file_path, "wt", encoding="utf-8") as fw:
        print("파일에 저장할 내용을 한줄씩 입력하세요.")
        while  True:
            # 입력
            txt = input(">>>")
            # !q 의 경우 종료
            if txt == "!q":
                break
            fw.write(txt+"\n")
            
    print("종료")

if __name__ == "__main__":
    my_memo()
