import pyecharts.options as opts
from pyecharts.charts import Line, Page

from utils import file_utils

from constant import constants

import os


def createItem(timeArr, dictData, titleText, needMax):
    c = (
        Line()
            .add_xaxis(timeArr)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=titleText + " : "),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),

        )
    )

    for key in dictData.keys():
        if needMax:
            c.add_yaxis(
                series_name=key,
                y_axis=dictData[key],
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="max"),
                        opts.MarkPointItem(type_="min", name="min"),
                    ]
                ),
            )
        else:
            c.add_yaxis(
                series_name=key,
                y_axis=dictData[key],
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False,
            )
    return c


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
            )
        )

        list.append(c)

    files = os.listdir(constants.PATH_PID)
    files.sort()
    pidDict = {}
    timeArr = []
    index = 0

    for file in files:
        index = index + 1
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_PID + file)
        contentLineArr = content.splitlines()
        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            if index == 1:
                timeArr.append(arr[0])
            if processName not in pidDict.keys():
                pidDict[processName] = []
            pidDict[processName].append(int(arr[1]))

    timeArr = [d.replace("2020/", "") for d in timeArr]

    c = createItem(timeArr, pidDict, "PID", False)

    list.append(c)

    files = os.listdir(constants.PATH_FD)
    files.sort()
    fdDict = {}
    timeArr = []
    index = 0

    for file in files:
        index = index + 1
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_FD + file)
        contentLineArr = content.splitlines()
        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            if index == 1:
                timeArr.append(arr[0])
            if processName not in fdDict.keys():
                fdDict[processName] = []
            fdDict[processName].append(int(arr[1]))

    timeArr = [d.replace("2020/", "") for d in timeArr]

    c = createItem(timeArr, fdDict, "fd_count", True)

    list.append(c)

    files = os.listdir(constants.PATH_THREAD)
    files.sort()
    threadDict = {}
    timeArr = []
    index = 0

    for file in files:
        index = index + 1
        processName = file.split("_")[0]
        content = file_utils.readFile(constants.PATH_THREAD + file)
        contentLineArr = content.splitlines()
        for i in range(len(contentLineArr)):
            arr = contentLineArr[i].split("|")
            if index == 1:
                timeArr.append(arr[0])
            if processName not in threadDict.keys():
                threadDict[processName] = []
            threadDict[processName].append(int(arr[1]))

    timeArr = [d.replace("2020/", "") for d in timeArr]

    c = createItem(timeArr, threadDict, "thread_count", True)

    list.append(c)

    page = Page()
    for item in list:
        page.add(item)
    page.render(constants.PATH_CHARS)
