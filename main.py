import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="매천고 프로그램",
    page_icon="🏫",

)

st.header('봉사활동 기간 체크 프로그램')

uploaded_files = st.file_uploader("엑셀파일을 올려주세요", type=["xlsx"],  accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

    data = pd.read_excel(bytes_data)
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
        st.write('시기')
    with c6:
        st.write('내용')

    for i, value in enumerate(test):
        if value:


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







