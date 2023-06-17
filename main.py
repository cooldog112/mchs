import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(
    page_title="매천고 프로그램",
    page_icon="🏫",

)

st.header('봉사활동 기간 체크 프로그램')

uploaded_file = st.file_uploader("엑셀파일을 올려주세요")

중복여부 = False
if uploaded_file:

    data = pd.read_excel(uploaded_file)
    data = data.sort_values(by=['학년','반','번호'])

    명렬 = data[['학년','반','번호','이름']]
    명렬 = 명렬.drop_duplicates()

    인원 = '총 인원 : ' + str(len(명렬)) + '명'
    st.subheader(인원)

    check = data[['학년','반','번호','이름','활동시기','활동내용 (실제 생기부에 기재되는 내용)']]
    test = check.duplicated(['학년','반','번호','이름','활동시기'])

    st.subheader(':red[중복 데이터]')
    c1,c2,c3,c4,c5,c6 = st.columns([1,1,1,2,4,6])
    with c1:
        st.write('학년')
    with c2:
        st.write('반')
    with c3:
        st.write('번호')
    with c4:
        st.write('이름')
    with c5:
        st.write('활동시기')
    with c6:
        st.write('내용')


    cnt = 0
    for i, value in enumerate(test):
        if value:
            중복여부 = True

            temp = check.iloc[i]['활동시기']
            start, end = map(str, check.iloc[i]['활동시기'].split('-'))


            년,월,일,t = map(str, end.split('.'))

            날짜 = datetime.datetime(int(년), int(월), int(일))

            날짜 = 날짜 - datetime.timedelta(days=1)

            st.write()
            indexKey = data.loc[
                         (data['학년'] == check.iloc[i]['학년']) &
                         (data['반'] == check.iloc[i]['반']) &
                         (data['번호'] == check.iloc[i]['번호']) &
                         (data['이름'] == check.iloc[i]['이름']) &
                         (data['활동내용 (실제 생기부에 기재되는 내용)'] == check.iloc[i]['활동내용 (실제 생기부에 기재되는 내용)'])
                     ].index
            년 = str(날짜.year)
            월 = 날짜.month
            일 = 날짜.day

            if 월<10:
                월 = '0'+str(월)
            else:
                월 = str(월)
            if 일<10:
                일 = '0'+str(일)
            else:
                일 = str(일)

            data.loc[indexKey, '활동시기'] = start+'-'+년+'.'+월+'.'+일+'.'

            with c1:
                st.write(check.iloc[i]['학년'])
            with c2:
                st.write(check.iloc[i]['반'])
            with c3:
                st.write(check.iloc[i]['번호'])
            with c4:
                st.write(check.iloc[i]['이름'])
            with c5:
                st.write(check.iloc[i]['활동시기'])
            with c6:
                st.write(check.iloc[i]['활동내용 (실제 생기부에 기재되는 내용)'])


    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Sheet', index=False)
        writer.close()

        st.download_button(
            label = 'Download Excel',
            data = buffer,
            file_name = '매천고 봉사활동 수정 파일.xlsx',
            mime = 'application/vnd.ms-excel'
        )


if 중복여부 == False:
    st.subheader(':blue[중복없음]')



