# coding:utf-8import pandas as pdimport numpy as npimport inoutimport initailimport countingfrom datetime import datetime,date,timedeltaimport timetopic_dic ={        '02-03': '疫情对你的工作生活产生了哪些问题和挑战？',        '02-04': '疫情期间，我该如何合理规划开工节奏？',        '02-05': '实体受困，如何单点破局实现业务转型？',        '02-06': '哪些有意义的事情，让你打破了对疫情的焦虑？',        '02-07': '零售等实体生意越来越难做，该怎么经营下去？',        '02-08': '单点破局 | 疫情之后，职场人该如何提升核心能力？',        '02-09': '困难时期，作为管理者的我，最应该做哪几件事？',        '02-10': '自媒体时代，我们普通人如何打造个人超级IP?',        '02-11': '2020年，中小企业如何找到新的增长点？',        '02-12': '黑天鹅到来，如何从现有业务分形创新出新业务？',        '02-13': '重口碑的教育培训行业，如何做营销才有效？',        '02-14': '疫情之下，如何管理“个人现金流”？',        '02-15': '如何利用深度思考解决复杂问题？',        '02-16': '如果未来我们不属于任何一家公司，该如何做准备？',        '02-17': '借鉴非典，零售人如何逆势增长？',        '02-18': '特殊时期，品牌如何加强与用户的情感链接？',        '02-19': '行业格局加速调整，你所在的企业如何突出重围？',        '02-20': '高手是如何用OKR实现目标的？',        '02-21': '怎样通过用户行为习惯读懂用户需求变化？',        '02-22': '疫情影响下，如何用创新思维模型找到增长破局？',        '02-23': '企业面临现金流大考，如何行动才能转危为安？',        '02-24': '中美贸易战，对我们普通人有什么影响？',        '02-25': '线上教育备受关注，如何借力新势能设计爆品课程？',        '02-26': '疫情期间，企业如何挖掘颠覆创新的机会？',        '02-27': '没有经验，怎样快速上手做短视频营销？',        '02-28': '疫情过后，哪些方向更值得投资？',        '02-29': '零售行业如何在疫情中寻找突破？',        '03-01': '零售行业如何把握疫情后的先机？',        '03-02': '直播带货成为生存之策，李佳琦的成功我能否复制？',        '03-03': '疫情波及投资，如何理性评估当下的风险和收益？',        '03-04': '至暗时刻，企业如何借机自我突破，实现转型升级？',        '03-05': '线上流量激增，怎样有效留存“看不见的消费者”？',        '03-06': '面对突发事件的创业者，如何提高决策正确率？',        '03-07': '后隔离时代，如何用场景化思维创新产品和服务？',        '03-08': '疫情之下，酒旅业如何扛过艰难期？',        '03-09': '“灵活用工“加速普及，企业如何行动才能把握新商机？',        '03-10': '你用过哪些值得推荐的读书方法？',        '03-11': '行业倒逼企业转型，如何转变，才能让组织心智由掣肘变动力？',        '03-12': '95后成为消费主力，品牌如何“取悦”年轻人？',        '03-13': '',        '03-14': '裁还是不裁，疫情考验组织优化能力，企业如何应答？',        '03-15': '新基建兴起，制造业如何抓住信息化转型机会，借势腾飞？',        '03-16': '如何通过探索个人使命，获得直面疫情挑战的笃定力量？',        '03-17': '危机当前，如何塑造制胜团队？',        '03-18': '行业头部涌现，如何找到适合自己的细分赛道？',        '03-19': '如何建立升级与成长思维，打造不一样的你？',        '03-20': 'vuca时代，如何“活着”—聊聊化解财富管理风险',        '03-21': '“新基建”窗口期，企业如何拥抱工业互联网？',        '03-22': '一切都是文娱业—文娱行业如何改变商业',        '03-23': '经济危机离我们普通人有多远？ 该如何应对？',        '03-24': '保持安全距离成为居民基本素养，我如何搭上非接触商业的顺风车？'    }keep_days = 5start_date = '2020-02-03'end_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期#更新跳失人数# inout.initData(start_date,end_date,topic_dic)# #更新围观用户，上座用户# initail.initData(start_date,end_date,topic_dic)# #延迟2s为了让前面的文件处理完成time.sleep(2)# #计算综合数据counting.initData(start_date,end_date,keep_days,topic_dic)