// javascript/builtin_object.js
function arrayExam() {
    // 배열 생성
    let arr = [1, 2, 3, 4, "바나나", "귤", true];
    console.log(arr);
    console.log("배열 크기 : " + arr.length);
    //배열.length -> 정수(원소 개수.)
    
    // 삭제 + 조회
    let v1 = arr.pop(); //마지막 index 원소
    let v2 = arr.shift();// 첫번째 index 원소
    console.log(v1, v2);
    console.log(arr);

    
    let v3 = arr.splice(1, 2);  // index , 개수 -> 삭제하면서 조회
    console.log(`splice(1,2): ${v3}`);
    console.log(arr);

    
    arr.push("마지막값");  // 마지막 index에 추가 (pop() 반대)
    console.log(arr);
    arr.unshift("첫번째 값"); // 첫번째 index에 삽입. (shift() 반대)
    console.log(arr);

    
    arr.splice(2, 0, "삽입할 값", 1, 2, 3, 4, 5); 
    //중간 삽입 (start_idx, 삭제할개수, [...대체할값들])
    console.log(arr);
    
    // 두개 배열을 합치기. (합친 새로운 배열을 반환.)
    arr2 = arr.concat(['가', '나', '다'])
    console.log(arr2)

    s = arr2.join(', ') // 배열의 원소들을 합쳐서 하나의 문자열로 반환.
    console.log(s)
    
}
function arrayExam2() {
    let arr = ["a", "b", "c", "d", "e"];
    //          0    1    2    3    4  (양수 index만 있음.)
    // 개별 원소조회: indexing - 배열[index] 
    // (slicing X  - 배열.slice(시작index, 끝index)) (끝 index는 포함안함.)
    console.log(arr[0], arr[2]);
    console.log(arr.slice(1, 3)) //index 1 ~ 3-1
    console.log(arr)

    // index의 값을 변경. 배열[index] = 변경할 값
    arr[1] = "가";
    console.log(arr);
    arr[7] = "나";
    console.log(arr);

    console.log(arr[6]);
    //배열의 모든 원소들을 일괄처리(조회) 
    console.log("첫번째")
    // 변수  i -> index 변수
    for (i = 0; i < arr.length; i++) {
        console.log(arr[i]);
    }
    console.log("for in 문")
    for (i in arr) { // index를 반환(값이 아님.)
        console.log(i, arr[i]);
    }
    
}

function dateExam() {
    let today = new Date(); // 실행시점의 일시
    console.log(today);
    // 년, 월(0 ~ 11), 일
    // 월 설정: 월-1, 월 조회: 월+1
    console.log(new Date(2010,5,7))   // 2010/6/7
    console.log(new Date(0,0,0,10,10))// 시, 분, (초)
    console.log(new Date(2020, 11, 20, 18, 22, 32))

    let str = dateToString(today);
    console.log(str);
    
}

function dateToString(dt) {
    let year = dt.getFullYear(); // 년도 4자리.

    let month = dt.getMonth() + 1;//월 ( 0 ~ 11)
    if (month < 10) month = "0" + month;                

    let date = dt.getDate(); // 일(1 ~ 31)
    if (date < 10) date = "0" + date;

    let hour = dt.getHours(); // 시간(0 ~ 23)
    if (hour < 10) hour = "0" + hour;

    let minute = dt.getMinutes(); //분(0 ~ 59)
    if (minute < 10) minute = "0" + minute;

    let second = dt.getSeconds(); //초(0 ~59)
    if (second < 10) second = "0" + second;

    return `${year}/${month}/${date} ${hour}:${minute}:${second}`;
}