import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from faker import Faker
import io
import datetime


#1Все виджеты старайся выносить в боковую панель - st.sidebar
#Добавь функционал загрузки датафрейма(csv файл) и скачивания графиков
#  - st.file_uploader | st.download_button
#Задеплой приложение в облаке - Deploy your app
#Реализуй графики используя не только st.pyplot()
#Разберись с кэшированием, добавь его к функции загрузки файла - Caching
#Сделай свое веб-приложение многостраничным - Multipage app

st.title('Исследование распределения чаевых')
st.subheader('на основании данных из tips.csv')

@st.cache_data(hash_funcs={type: lambda _: None})
def load_data(file):
    return pd.read_csv(file)

uploaded_file = st.sidebar.file_uploader('Загрузите файл tips.csv из репозитория')

if uploaded_file is not None:
    tips = load_data(uploaded_file)
    fake = Faker()
    def random_date():
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 31)
        return fake.date_between(start_date= start_date, end_date= end_date)
    random_dates = [random_date() for i in range(len(tips))]
    tips['time_order']= random_dates
    st.table(tips.head(10))

    st.write('1. Динамика чаевых во времени')
    fig = plt.figure(figsize=(15, 5))
    sns.lineplot(data=tips, x= 'time_order', y= 'tip')
    st.pyplot(fig)

    def saving_img():
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig1.png",
            mime = 'image/png'
          )

    st.write('2. Гистограмма распределения total_bill')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.histplot(tips['total_bill'], ax=ax)
    st.pyplot(fig)

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig2.png",
            mime = 'image/png'
          )

    st.write('3. Cвязь между total_bill and tip c помощью scatterplot')
    st.scatter_chart(tips, x='total_bill', y='tip', color='tip')

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig3.png",
            mime = 'image/png'
          )

    st.write('4. Cвязь между total_bill, tip и size c помощью scatterplot')
    st.scatter_chart(tips, x='total_bill', y='tip', size='size', color='size')

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig4.png",
            mime = 'image/png'
          )

    st.write('5. Cвязь между днем недели и размером счета(Total_bill)')
    st.bar_chart(tips, x='day', y='total_bill')

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig5.png",
            mime = 'image/png'
          )

    st.write('6. Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу')
    st.scatter_chart(tips, x='tip', y='day', color='sex')

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig6.png",
            mime = 'image/png'
          )

    st.write('7. box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.boxplot(data=tips, x='day', y='total_bill', hue='time')
    st.pyplot(fig)

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig7.png",
            mime = 'image/png'
          )

    st.write('8. Гистограммы чаевых на обед и ланч')
    tips_lunch = tips[tips['time'] == 'Lunch']
    tips_dinner = tips[tips['time'] == 'Dinner']
    fig = plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(data= tips_dinner, x='tip')
    plt.title('dinner')
    plt.subplot(1, 2, 2)
    sns.histplot(data= tips_lunch, x='tip')
    plt.title('lunch')
    plt.tight_layout()
    st.pyplot(fig)

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig8.png",
            mime = 'image/png'
          )

    st.write('9. Cвязь размера счета и чаевых c разбивкой по курящим/некурящим')
    tips_female = tips[tips['sex'] == 'Female']
    tips_male = tips[tips['sex'] == 'Male']
    fig = plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=tips_female, x='total_bill', y='tip', hue='smoker')
    plt.title('Female')
    plt.subplot(1, 2, 2)
    sns.scatterplot(data=tips_male, x='total_bill', y='tip', hue='smoker')
    plt.title('Male')
    plt.tight_layout()
    st.pyplot(fig)

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig9.png",
            mime = 'image/png'
          )

    st.write('10. Тепловая карта зависемостей численных переменных')
    corr_matrix = tips.corr(numeric_only=bool)
    fig = plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', linewidths=1)
    plt.title('Тепловая карта зависимостей численных переменных')
    st.pyplot(fig)

    btn = st.download_button(
            label="Download image",
            data=saving_img(),
            file_name="fig10.png",
            mime = 'image/png'
          )



else:
    st.stop()

