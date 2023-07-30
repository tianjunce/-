import pandas as pd
import numpy as np

def data_load(path = 'excess-mortality-raw-death-count.csv'):
    data = pd.read_csv(path)
    mask = data['deaths_2017_all_ages'].notna()
    return data[mask]


a1 = ['Albania', 'Andorra', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 'Canada', 'Cape Verde', 'Chile', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'England & Wales', 'Estonia', 'Faroe Islands', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Georgia', 'Germany', 'Gibraltar', 'Greece', 'Greenland', 'Guadeloupe', 'Guatemala', 'Hong Kong', 'Hungary', 'Iceland', 'Iran', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Malaysia', 'Maldives', 'Malta', 'Martinique', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'North Macedonia', 'Northern Ireland', 'Norway', 'Oman', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Saint Kitts and Nevis', 'Saint Vincent and the Grenadines', 'San Marino', 'Scotland', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Thailand', 'Transnistria', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan']
b1 = ['阿尔巴尼亚', '安道尔', '安提瓜和巴布达', '阿根廷', '亚美尼亚', '阿鲁巴', '澳大利亚', '奥地利', '阿塞拜疆', '巴哈马', '巴巴多斯', '白俄罗斯', '比利时', '伯利兹', '百慕大', '玻利维亚', '波斯尼亚和黑塞哥维那', '巴西', '文莱', '保加利亚', '加拿大', '佛得角', '智利', '哥伦比亚', '哥斯达黎加', '克罗地亚', '古巴', '塞浦路斯', '捷克', '丹麦', '多米尼加共和国', '厄瓜多尔', '埃及', '萨尔瓦多', '英格兰和威尔士', '爱沙尼亚', '法罗群岛', '芬兰', '法国', '法属圭亚那', '法属波利尼西亚', '格鲁吉亚', '德国', '直布罗陀', '希腊', '格陵兰', '瓜德罗普', '危地马拉', '香港', '匈牙利', '冰岛', '伊朗', '爱尔兰', '以色列', '意大利', '牙买加', '日本', '约旦', '哈萨克斯坦', '科索沃', '科威特', '吉尔吉斯斯坦', '拉脱维亚', '黎巴嫩', '列支敦士登', '立陶宛', '卢森堡', '澳门', '马来西亚', '马尔代夫', '马耳他', '马提尼克', '毛里求斯', '马约特', '墨西哥', '摩尔多瓦', '摩纳哥', '蒙古', '黑山', '荷兰', '新喀里多尼亚', '新西兰', '尼加拉瓜', '北马其顿', '北爱尔兰', '挪威', '阿曼', '巴拿马', '巴拉圭', '秘鲁', '菲律宾', '波兰', '葡萄牙', '波多黎各', '卡塔尔', '留尼汪', '罗马尼亚', '俄罗斯', '圣基茨和尼维斯', '圣文森特和格林纳丁斯', '圣马力诺', '苏格兰', '塞尔维亚', '塞舌尔', '新加坡', '斯洛伐克', '斯洛文尼亚', '南非', '韩国', '西班牙', '苏里南', '瑞典', '瑞士', '台湾', '塔吉克斯坦', '泰国', '德涅斯特河沿岸', '突尼斯', '土耳其', '乌克兰', '阿拉伯联合酋长国', '英国', '美国', '乌拉圭', '乌兹别克斯坦']

code_dict = dict(zip(b1,a1))


def data_gen(data, country, thisyear=2023, pp=0, web=1):
    if country not in code_dict:
        raise ValueError(f'{country}没有数据')
    code = code_dict[country]
    years = [*map(str,range(2015,thisyear+1))]
    year_all = [*range(2015,thisyear+1)]
    yy = [f'deaths_{x}_all_ages' for x in years]
    data1 = data[data['Entity']==code]
    data_code = data1[yy]
    if data_code.iloc[:,1].isna().sum()>0:
        mask = data_code.iloc[:,1].isna()
        data_code.iloc[:,1] = data_code.iloc[:,2:5].mean(axis=1)
    if data_code.iloc[:,0].isna().sum()>0:
        mask = data_code.iloc[:,0].isna()
        if mask.sum()==1:
            data_code.iloc[0,0] = data_code.iloc[0,1:5].mean()
        else:
            data_code.iloc[:,0] = data_code.iloc[:,1:5].mean(axis=1)

    data_o = data_code.iloc[:,:5]
    data_oy = data_o.sum()/10000
    data_om = data_o.mean(axis=1)/10000

    x_list = list(range(2015,2020))
    y_list = data_oy
    #多项式拟合公式
    z1 = np.polyfit(x_list, y_list, 1) #用1次多项式拟合，输出系数从高到0
    z2 = np.polyfit(x_list, y_list, 2) #用2次多项式拟合，输出系数从高到0
    p1 = np.poly1d(z1) #多项式公式
    p2 = np.poly1d(z2)
    #如果p1、p2差异巨大，以高的为主
    # if abs((p1(thisyear)-p2(thisyear))/np.mean(y_list)) > 0.15:
    #     if p1(thisyear)>p2(thisyear):p3 = 0.95*p1+0.05*p2
    #     else: p3 = 0.95*p2+0.05*p1

    if abs((p1(2022)-p2(2022))/np.mean(y_list)) > 0.1:
        p3 = 0.9*p1+0.1*p2
        # if p1(thisyear)>p2(thisyear):p3 = 0.9*p1+0.1*p2
        # else: p3 = 0.9*p2+0.1*p1
        
    elif abs((p1(2022)-p2(2022))/np.mean(y_list)) > 0.05:
        p3 = 0.75*p1+0.25*p2
        # if p1(thisyear)>p2(thisyear):p3 = 0.75*p1+0.25*p2
        # else: p3 = 0.75*p2+0.25*p1
    else:
        p3 = 0.6*p1+0.4*p2
        # if p1(thisyear)>p2(thisyear):p3 = 0.6*p1+0.4*p2
        # else: p3 = 0.6*p2+0.4*p1
    if pp==1: p3=p1
    
    data_p = [p1(year_all).tolist(),p2(year_all).tolist(),p3(year_all).tolist()]                                    #拟合方程，1次，2次，（1次+2次） 
    y_rate = [p3(x)/np.mean(y_list) for x in year_all[5:] ] #2020年之后与拟合死亡总人数的比例

    data_all, data_all_p = [],[]
    for i in range(len(years[5:])):
        data_all+=[data_code.iloc[:,i+5].to_list()]
        data_all_p += [list(data_om*y_rate[i])]

    data_all, data_all_p =np.array(data_all), np.array(data_all_p)*10000
    

    def cum(data):
        a=0
        res=[]
        for x in data:
            a=a+x
            res+=[a]
        return np.array(res)

    def remna(data):
        return data[~np.isnan(data)]
    

    data_all1 = cum(data_all.reshape(-1))
    data_all_p1=cum(data_all_p.reshape(-1))
    em_cum = data_all1-data_all_p1
    em_rate = (data_all1-data_all_p1)/data_all_p1*100

    days = [x[5:] for x in data1.Day.to_list()]
    day_all =[year+'-'+day for year in years[5:] for day in days]

    labels, df_em, em_data, fig4y = [],[country],[],[]
    for i in range(len(data_all)):
        em1=(cum(data_all[i])-cum(data_all_p[i]))/cum(data_all_p[i])*100
        em_data+=[em1]
        em1=remna(em1)
        fig4y+=[em1.tolist()]
        labels+=[f'202{i}年的超额死亡率为{em1[-1]:.1f}%']
        df_em += [round(em1[-1],1)]

    df_em += [round(remna(em_cum)[-1]/10000,3)]
    df_em += [round(remna(em_rate)[-1],1)]
    df_em += [np.array(day_all)[~np.isnan(em_cum)][-1]]


    if not web:
        return (x_list, data_oy, data_code.sum()/10000),(year_all, data_p), (day_all, em_cum, em_rate), (days, em_data, labels), df_em  
    
    # else:
    #     webdata = {'fig1x':year_all,
    #                'fig1y1':(data_code.sum()/10000).to_list(),
    #                'fig1y2':data_p,
    #                'fig2x':day_all,
    #                'fig2y1':em_cum,
    #                'fig2y2':em_rate,
    #                'fig3x':days,
    #                'fig3y':em_data,
    #                'fig3label':labels}
    #     return webdata
    else:
        em_cum = remna(em_cum).tolist()
        em_rate = remna(em_rate).tolist()
        em_rate = [*map(lambda x: round(x,2),em_rate)]
        #em_data = remna(em_data).tolist()

        webdata = {'fig1x':year_all,
                   'fig1y1':(data_code.sum()/10000).to_list(),
                   'fig1y2':data_p,
                   'fig2x':day_all,
                   'fig2y':[*map(int,em_cum)],
                   'fig3y':em_rate,
                   'fig4x':days,
                   'fig4y':fig4y,
                   'fig4l':labels,
                   'last':[[*map(int,em_cum)][-1],em_rate[-1]]
                   }
        return webdata
