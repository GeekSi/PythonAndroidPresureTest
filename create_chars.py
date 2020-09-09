import pyecharts.options as opts
from pyecharts.charts import Line, Page

from utils import utils

from constant import constants

import os


def createChars():
    list = []

    files = os.listdir(constants.PATH_CPU)
    files.sort()
    for x in files:
        content = utils.excuteCmd("cat " + constants.PATH_CPU + x)
        pidLineArr = content.splitlines()
        timeArr = []
        processCpuArr = []
        totalCpuArr = []

        for i in range(len(pidLineArr)):
            arr = pidLineArr[i].split("|")
            timeArr.append(arr[0])
            processCpuArr.append(int(arr[1]))
            totalCpuArr.append(int(arr[2]))

        timeArr = [d.replace("2020/", "") for d in timeArr]

        c = (
            Line()
                .add_xaxis(timeArr)
                .add_yaxis(
                series_name=x,
                y_axis=processCpuArr,
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
                .add_yaxis(
                series_name="total",
                y_axis=totalCpuArr,
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
                .set_global_opts(
                title_opts=opts.TitleOpts(title="cpu"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(xaxis_index=0),
                    opts.DataZoomOpts(type_="inside", xaxis_index=0),
                ]
            )
        )

        list.append(c)

    files = os.listdir(constants.PATH_MEM)
    files.sort()
    for x in files:
        content = utils.excuteCmd("cat " + constants.PATH_MEM + x)
        pidLineArr = content.splitlines()
        timeArr = []
        javaMemArr = []
        nativeMemArr = []
        totalMemArr = []

        for i in range(len(pidLineArr)):
            arr = pidLineArr[i].split("|")
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
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False
            )
                .add_yaxis(
                series_name="native",
                y_axis=nativeMemArr,
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False
            )
                .add_yaxis(
                series_name="total",
                y_axis=totalMemArr,
                linestyle_opts=opts.LineStyleOpts(width=2), is_smooth=True, is_symbol_show=False
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="mem"),
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

    for x in files:
        print(x)
        content = utils.excuteCmd("cat " + constants.PATH_PID + x)
        pidLineArr = content.splitlines()
        timeArr = []
        pidArr = []
        for i in range(len(pidLineArr)):
            arr = pidLineArr[i].split("|")
            timeArr.append(arr[0])
            pidArr.append(int(arr[1]))

        timeArr = [d.replace("2020/", "") for d in timeArr]

        c = (
            Line()
                .add_xaxis(timeArr)
                .add_yaxis(series_name="", y_axis=pidArr, xaxis_index=0, is_smooth=True, is_symbol_show=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="pid"),
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
