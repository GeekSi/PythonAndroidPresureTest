import pyecharts.options as opts
from pyecharts.charts import Line, Page

from utils import utils

from utils import file_utils

from constant import constants

import os


def createChars():
    list = []

    files = os.listdir(constants.PATH_CPU)
    files.sort()
    cpuDict = {}
    timeArr = []
    for file in files:
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_CPU + file)
        contentLineArr = content.splitlines()
        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            if processName == "device":
                timeArr.append(arr[0])
            if processName not in cpuDict.keys():
                cpuDict[processName] = []
            cpuDict[processName].append(int(arr[1]))

    timeArr = [d.replace("2020/", "") for d in timeArr]

    c = (
        Line()
            .add_xaxis(timeArr)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="CPU : "),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0),
                opts.DataZoomOpts(type_="inside", xaxis_index=0),
            ]
        )
    )

    for key in cpuDict.keys():
        c.add_yaxis(
            series_name=key,
            y_axis=cpuDict[key],
            linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="cpu_max"),
                    opts.MarkPointItem(type_="min", name="cpu_min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="cpu_avg")]
            ),
        )

    list.append(c)

    files = os.listdir(constants.PATH_MEM)
    files.sort()
    for file in files:
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_MEM + file)
        contentLineArr = content.splitlines()
        timeArr = []
        javaMemArr = []
        nativeMemArr = []
        totalMemArr = []

        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            timeArr.append(arr[0])
            javaMemArr.append(int(arr[1]))
            nativeMemArr.append(int(arr[2]))
            totalMemArr.append(int(arr[3]))

        timeArr = [d.replace("2020/", "") for d in timeArr]

        c = (
            Line()
                .add_xaxis(timeArr)
                .add_yaxis(
                series_name="java",
                y_axis=javaMemArr,
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="java_max"),
                        opts.MarkPointItem(type_="min", name="java_min"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="java_avg")]
                )
            )
                .add_yaxis(
                series_name="native",
                y_axis=nativeMemArr,
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="native_max"),
                        opts.MarkPointItem(type_="min", name="native_min"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="native_avg")]
                )
            )
                .add_yaxis(
                series_name="total",
                y_axis=totalMemArr,
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="total_max"),
                        opts.MarkPointItem(type_="min", name="total_min"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="total_avg")]
                )
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="MEM : " + processName,
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="black")),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(xaxis_index=0),
                    opts.DataZoomOpts(type_="inside", xaxis_index=0),
                ]
            )
        )

        list.append(c)

    files = os.listdir(constants.PATH_PID)
    files.sort()

    for file in files:
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_PID + file)
        contentLineArr = content.splitlines()
        timeArr = []
        pidArr = []
        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            timeArr.append(arr[0])
            pidArr.append(int(arr[1]))

        timeArr = [d.replace("2020/", "") for d in timeArr]

        c = (
            Line()
                .add_xaxis(timeArr)
                .add_yaxis(series_name="", y_axis=pidArr, xaxis_index=0, is_smooth=True, is_symbol_show=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="PID : " + processName,
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="black")),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(xaxis_index=0),
                    opts.DataZoomOpts(type_="inside", xaxis_index=0),
                ]
            )
        )

        list.append(c)

    page = Page()
    for item in list:
        page.add(item)
    page.render(constants.PATH_CHARS)

