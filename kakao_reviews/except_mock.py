
def connect():
    list =[ { 'ko': '곤드레나물밥',	'en': 'Gondeurenamulbap' },
        { 'ko': '굴국밥', 'en': 'Gulgukbap' },
        { 'ko': '굴밥', 'en': 'Gulbap' },
        { 'ko': '김밥', 'en': 'Gimbap' },
        { 'ko': '김치김밥', 'en': 'Kimchigimbap' },
        { 'ko': '김치볶음밥', 'en': 'Kimchibokkeumbap' },
        { 'ko': '낙지덮밥', 'en': 'Nakjideopbap' },
        { 'ko': '누룽지', 'en': 'Nurungji' },
        { 'ko': '대나무통밥', 'en': 'Daenamutongbap' },
        { 'ko': '돌솥비빔밥', 'en': 'Dolsotbibimbap' },
        { 'ko': '돼지국밥', 'en': 'Dwaejigukbap' },
        { 'ko': '따로국밥', 'en': 'Ttarogukbap' },
        { 'ko': '멍게비빔밥', 'en': 'Meonggebibimbap' },
        { 'ko': '메밀감자비빔밥', 'en': 'Memilgamjabibimbap' },
        { 'ko': '묵밥', 'en': 'Mukbap'}]

    print("\n\n\n\n\nstart")
    for i, str in enumerate(list):
        print(i, str['ko'])
        try:
            
            if i==4:
                raise Exception("Sorry, no numbers below zero")
            print(i, str['en'])
        except Exception as err:
            print("userError", err)


if __name__ == '__main__':
    connect()