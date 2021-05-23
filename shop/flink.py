import os, django
import sys

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic, DataStream
from pyflink.table.window import Slide

path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
# print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower.settings")  # project_name 项目名称
django.setup()

from django.shortcuts import get_object_or_404

from shop import models

from pyflink.table import EnvironmentSettings, TableEnvironment
import datetime


def main():
    # env=StreamExecutionEnvironment.get_execution_environment()
    # env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    # dataStream=DataStream
    # dataStream.assign_timestamps_and_watermarks()


    # 创建 TableEnvironment
    env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    table_env = TableEnvironment.create(env_settings)

    table_env.execute_sql("""
        CREATE TABLE datagen (
            id INT,
            data STRING
        ) WITH (
            'connector' = 'datagen',
            'fields.id.kind' = 'sequence',
            'fields.id.start' = '1',
            'fields.id.end' = '10'
        )
    """)

    # 3. 创建 sink 表
    table_env.execute_sql("""
        CREATE TABLE print (
            id INT,
            data STRING
        ) WITH (
            'connector' = 'print'
        )
    """)

    # 4. 查询 source 表，同时执行计算
    # 通过 Table API 创建一张表：
    source_table = table_env.from_path("datagen")
    # 或者通过 SQL 查询语句创建一张表：
    source_table = table_env.sql_query("SELECT * FROM datagen")

    result_table = source_table.select(source_table.id + 1, source_table.data)

    # 5. 将计算结果写入给 sink 表
    # 将 Table API 结果表数据写入 sink 表：
    result_table.execute_insert("print").wait()
    # 或者通过 SQL 查询语句来写入 sink 表：
    table_env.execute_sql("INSERT INTO print SELECT * FROM datagen").wait()

    # 方法2：基于 Table API 来聚合
    # 创建长度为 1 小时、滑动步长为 5 分钟的滑动窗口 slide_window ，并重命名为 w
    # 使用 w.start, w.end 来获得滑动窗口的开始时间与结束时间
    # slide_window = Slide.over("1.hours").every("5.minutes").on('ts').alias("w")
    # table_env.from_path('source') \
    #     .filter("action = 'click'") \
    #     .window(slide_window) \
    #     .group_by("w") \
    #     .select("getTopN(name, 10, 1) as top10, "
    #             "w.start AS start_time, "
    #             "w.end AS end_time") \
    #     .insert_into("sink")
    # table_env.execute('Top10 User Click')


    endtime = datetime.datetime.now()
    start_time = endtime + datetime.timedelta(hours=-1)

    renmings = models.Dianji.objects.filter(date__range=[start_time, endtime])
    dicts = {}
    for renm in renmings:
        if dicts.get(renm.case_item.id, '') == '':
            dicts[renm.case_item.id] = 1
        else:
            dicts[renm.case_item.id] = dicts[renm.case_item.id] + 1
    print(dicts)
    sorted(dicts.items(), key=lambda item: item[1], reverse=True)
    renming = []
    for ii in list(dicts.keys())[:5]:
        renming.append(get_object_or_404(models.Case_item, pk=ii))

    return renming

