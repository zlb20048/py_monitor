# YApi QuickType插件生成，具体参考文档:https://plugins.jetbrains.com/plugin/18847-yapi-quicktype/documentation

from typing import List


class Element:
    elementid: str
    tag: str

    def __init__(self, elementid: str, tag: str) -> None:
        self.elementid = elementid
        self.tag = tag


class Body:
    elements: List[Element]

    def __init__(self, elements: List[Element]) -> None:
        self.elements = elements


class CardLink:
    iosurl: str
    androidurl: str
    pcurl: str
    url: str

    def __init__(self, iosurl: str, androidurl: str, pcurl: str, url: str) -> None:
        self.iosurl = iosurl
        self.androidurl = androidurl
        self.pcurl = pcurl
        self.url = url


class ColorCus0:
    lightmode: str
    darkmode: str

    def __init__(self, lightmode: str, darkmode: str) -> None:
        self.lightmode = lightmode
        self.darkmode = darkmode


class Color:
    cus0: ColorCus0

    def __init__(self, cus0: ColorCus0) -> None:
        self.cus0 = cus0


class TextSizeCus0:
    default: str
    pc: str
    mobile: str

    def __init__(self, default: str, pc: str, mobile: str) -> None:
        self.default = default
        self.pc = pc
        self.mobile = mobile


class TextSize:
    cus0: TextSizeCus0

    def __init__(self, cus0: TextSizeCus0) -> None:
        self.cus0 = cus0


class Style:
    textsize: TextSize
    color: Color

    def __init__(self, textsize: TextSize, color: Color) -> None:
        self.textsize = textsize
        self.color = color


class I18NContent:
    enus: str
    zhcn: str
    jajp: str

    def __init__(self, enus: str, zhcn: str, jajp: str) -> None:
        self.enus = enus
        self.zhcn = zhcn
        self.jajp = jajp


class Summary:
    i18ncontent: I18NContent
    content: str

    def __init__(self, i18ncontent: I18NContent, content: str) -> None:
        self.i18ncontent = i18ncontent
        self.content = content


class Config:
    summary: Summary
    enableforward: bool
    enableforwardinteraction: bool
    streamingmode: bool
    usecustomtranslation: bool
    style: Style
    updatemulti: bool
    widthmode: str

    def __init__(self, summary: Summary, enableforward: bool, enableforwardinteraction: bool, streamingmode: bool, usecustomtranslation: bool, style: Style, updatemulti: bool, widthmode: str) -> None:
        self.summary = summary
        self.enableforward = enableforward
        self.enableforwardinteraction = enableforwardinteraction
        self.streamingmode = streamingmode
        self.usecustomtranslation = usecustomtranslation
        self.style = style
        self.updatemulti = updatemulti
        self.widthmode = widthmode


class Header:
    pass

    def __init__(self, ) -> None:
        pass


class FeishuCard:
    schema: str
    cardlink: CardLink
    header: Header
    body: Body
    config: Config

    def __init__(self, schema: str, cardlink: CardLink, header: Header, body: Body, config: Config) -> None:
        self.schema = schema
        self.cardlink = cardlink
        self.header = header
        self.body = body
        self.config = config
