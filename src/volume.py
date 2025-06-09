import json


def get_price(data):
    Open = data[0]['시가']

    high_list = []
    low_list = []
    for i in data:
        high_list.append(i['고가'])
        low_list.append(i['저가'])
    close = i['종가']
    high = max(high_list)
    low = min(low_list)
    return (Open, high, low, close)


stock_info = [
    ('053580', '웹케시'),
    ('011000', '진원생명과학'),
    ('014990', '인디에프'),
    ('032940', '원익'),
    ('089150', '케이씨티'),
]
for code, name in stock_info:
    with open(f'data/{code}.txt', 'r', encoding='utf-8') as txt:
        data: dict[str, str|int] = json.load(txt)
    Open, high, low, close = get_price(data)

    hsub = high - close
    hh, hm, hl = (round(high-hsub/4), round(high-hsub/2), round(close+hsub/4))
    lsub = close - low
    lh, lm, ll = (round(close-lsub/4), round(close-lsub/2), round(low+lsub/4))

    volume = sum([i['거래량'] for i in data])
    print()
    print(f'종목코드 : {code}')
    print(f'종목명 : {name}')
    print(f'시가 : {Open:,}원, 고가 : {high:,}원, 저가 : {low:,}원, 종가 : {close:,}원')
    print(f'전체 거래량 : {volume:,}주')
    print('\n거래량 분포')

    hh_list = []
    hm_list = []
    hl_list = []
    ch_list = []
    cl_list = []
    lh_list = []
    lm_list = []
    ll_list = []
    for i in data:
        L, H = (i['저가'], i['고가'])

        num_list = [0 for _ in range(8)]

        def get_index(p):
            if hh < p:
                return 0
            elif hm < p:
                return 1
            elif hl < p:
                return 2
            elif close < p:
                return 3
            elif lh < p:
                return 4
            elif lm < p:
                return 5
            elif ll < p:
                return 6
            return 7

        for p1, p2 in [
            (i['저가'], i['고가']),
            (i['시가'], i['종가'])
        ]:
            ind1, ind2 = (get_index(p1), get_index(p2))
            if ind1 == ind2:
                num_list[ind1] += 2
            else:
                num_list[ind1] += 1
                num_list[ind2] += 1
                for ind in range(ind2-ind1):
                    if ind2 <= ind:
                        break
                    if ind1 < ind:
                        num_list[ind] += 2

        if not any(num_list):
            print(f'{num_list=}')
            raise

        a, b, c, d, e, f, g, h = num_list
        v = i['거래량'] / sum(num_list)

        if 0 < a:
            hh_list.append(v * a)
        if 0 < b:
            hm_list.append(v * b)
        if 0 < c:
            hl_list.append(v * c)
        if 0 < d:
            ch_list.append(v * d)
        if 0 < e:
            cl_list.append(v * e)
        if 0 < f:
            lh_list.append(v * f)
        if 0 < g:
            lm_list.append(v * g)
        if 0 < h:
            ll_list.append(v * h)

    for n, l in {
        '고가 75% ~ 고가 100%': hh_list,
        '고가 50% ~ 고가 75%': hm_list,
        '고가 25% ~ 고가 50%': hl_list,
        '종가 ~ 고가 25%': ch_list,
        '저가 25% ~ 종가': cl_list,
        '저가 50% ~ 저가 25%': lh_list,
        '저가 75% ~ 저가 50%': lm_list,
        '저가 100% ~ 저가 75%': ll_list
    }.items():
        print(f'  {n}')
        s = sum([round(i) for i in l])
        print(f'    {s:,}주')
        print(f'    {round(s * 100 / volume, 2)}%')

