import telebot
from telebot import types
import re
import requests
import time
import json
import logging
import html
from config import API_TOKEN
from config import HEADER
from consts import START_MESSAGE

bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO)

query = {}

options = ['Chart', 'Headlines', 'Description']

markup = types.InlineKeyboardMarkup()
markup.add(*[types.InlineKeyboardButton(text=option, callback_data=option) for option in options])

language = "en"


def search_organization(organization_name):
    r = requests.post(
        url="http://api.trkd.thomsonreuters.com/api/Search/Search.svc/REST/Organisation_1/GetOrganisation_1",
        data=json.dumps({
            "GetOrganisation_Request_1": {
                "QueryHeader": {
                    "MaxCount": 1,
                    "Pivot": 0,
                    "Timeout": 0,
                    "Spellcheck": "On"
                },
                "Query": [
                    {
                        "Search": {
                            "Include": True,
                            "StringValue": [
                                {
                                    "Value": organization_name
                                }
                            ]
                        },
                        "Name": {
                            "Include": True
                        },
                        "PrimaryRIC": {
                            "Include": True
                        }
                    }
                ]
            }
        }),
        headers=HEADER)
    logging.info('REQUEST' + str(r.json()))
    return r


def organization_chart(organization_ric):
    r = requests.post(
        headers=HEADER,
        data=json.dumps(
            {
                "GetChart_Request_2": {
                    "chartRequest": {
                        "TimeSeries": {
                            "TimeSeriesRequest_typehint": [
                                "TimeSeriesRequest"
                            ],
                            "TimeSeriesRequest": [
                                {
                                    "Symbol": str(organization_ric),
                                    "Reference": "d1"
                                }
                            ]
                        },
                        "Analyses": {
                            "Analysis_typehint": [
                                "Analysis",
                                "Analysis"
                            ],
                            "Analysis": [
                                {
                                    "Reference": "a1",
                                    "OHLC": {
                                        "Instrument1": {
                                            "Reference": "d1"
                                        }
                                    }
                                },
                                {
                                    "Reference": "a2",
                                    "Vol": {
                                        "Instrument1": {
                                            "Reference": "d1"
                                        }
                                    }
                                }
                            ]
                        },
                        "StandardTemplate": {
                            "Title": {
                                "Caption": {
                                    "Visible": True,
                                    "Customized": False
                                },
                                "Range": {
                                    "Visible": True
                                }
                            },
                            "Legend": {
                                "Visible": True,
                                "Information": "Long",
                                "Layout": "MultiLine",
                                "Position": "Overlaid"
                            },
                            "Instrument": "Symbol",
                            "Delimiter": "%",
                            "GridLines": "None",
                            "YAxisMarkers": "None",
                            "Interval": {
                                "CommonType": "Days",
                                "Multiplier": "1"
                            },
                            "ShowNonTradedPeriods": False,
                            "ShowHolidays": False,
                            "ShowGaps": True,
                            "XAxis": {
                                "Visible": True,
                                "Position": "Bottom",
                                "Range": {
                                    "Fixed": {
                                        "First": "2016-12-02T00:00:00",
                                        "Last": "2017-12-02T00:00:00"
                                    }
                                }
                            },
                            "Subchart": [
                                {
                                    "Weight": 5.0,
                                    "YAxis": [
                                        {
                                            "Visible": True,
                                            "Position": "Right",
                                            "Invert": False,
                                            "Logarithmic": False,
                                            "Display": {
                                                "Mode": "Automatic"
                                            },
                                            "Range": {
                                                "Automatic": ""
                                            },
                                            "Analysis": [
                                                {
                                                    "Reference": "a1"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Weight": 2.0,
                                    "YAxis": [
                                        {
                                            "Visible": True,
                                            "Position": "Right",
                                            "Invert": False,
                                            "Logarithmic": False,
                                            "Display": {
                                                "Mode": "Automatic"
                                            },
                                            "Range": {
                                                "Automatic": ""
                                            },
                                            "Analysis": [
                                                {
                                                    "Reference": "a2"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "YAxisTitles": "All",
                            "Brand": "None"
                        },
                        "Scheme": {
                            "Background": {
                                "BackgroundMode": "Solid",
                                "StartColor": {
                                    "Named": "White"
                                },
                                "EndColor": {
                                    "Named": "White"
                                },
                                "HatchStyle": "LargeGrid",
                                "GradientMode": "ForwardDiagonal",
                                "ImageMode": "Centered"
                            },
                            "Border": {
                                "Color": {
                                    "RGB": "139;139;155"
                                },
                                "DashStyle": "Solid",
                                "Width": 1.0
                            },
                            "GridLines": {
                                "Color": {
                                    "RGB": "139;139;155"
                                },
                                "DashStyle": "Dot",
                                "Width": 1.0
                            },
                            "Title": {
                                "Caption": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 12.0
                                },
                                "Range": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "Legend": {
                                "Color": {
                                    "Named": "Black"
                                },
                                "Family": "Arial",
                                "Style": "Regular",
                                "Size": 8.25
                            },
                            "XAxis": {
                                "Major": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 9.75
                                },
                                "Minor": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "YAxis": {
                                "Major": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 9.75
                                },
                                "Minor": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                },
                                "Title": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "Series": [
                                {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "Named": "Black"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "Named": "Red"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "Named": "Red"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "62;169;0"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "62;169;0"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "156;38;115"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "156;38;115"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "255;120;0"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "255;120;0"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "25;108;229"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "25;108;229"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "60;117;28"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "60;117;28"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "230;176;18"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "230;176;18"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "0;186;193"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "0;186;193"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "255;178;127"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "255;178;127"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "100;79;190"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "100;79;190"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "209;36;33"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "209;36;33"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "38;87;135"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "38;87;135"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "94;176;176"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "94;176;176"
                                    },
                                    "FillStyle": "Percent20"
                                }
                            ],
                            "LevelLine": [
                                {
                                    "Color": {
                                        "RGB": "0;0;153"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 1.0
                                },
                                {
                                    "Color": {
                                        "RGB": "120;120;120"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 1.0
                                }
                            ]
                        },
                        "ImageType": "PNG",
                        "Width": 500,
                        "Height": 400,
                        "Culture": "en-US",
                        "ReturnPrivateNetworkURL": False
                    }
                }
            }
        ),
        url="http://api.trkd.thomsonreuters.com/api/Charts/Charts.svc/REST/Charts_1/GetChart_2"
    )
    return r


def organization_headlines(organization_ric):
    r = requests.post(
        headers=HEADER,
        data=json.dumps({
            "RetrieveHeadlineML_Request_1": {
                "HeadlineMLRequest": {
                    "MaxCount": 5,
                    "Direction": "Newer",
                    "Filter": [
                        {
                            "And": {
                                "MetaDataConstraint_typehint": [
                                    "MetaDataConstraint",
                                    "MetaDataConstraint"
                                ],
                                "MetaDataConstraint": [
                                    {
                                        "Value": {
                                            "Text": language
                                        },
                                        "class": "Language"
                                    },
                                    {
                                        "Value": {
                                            "Text": organization_ric
                                        },
                                        "class": "Companies"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }),
        url="http://api.trkd.thomsonreuters.com/api/News/News.svc/REST/News_1/RetrieveHeadlineML_1"
    )
    logging.info(r.json())
    return r


def organization_general_info(organization_ric):
    r = requests.post(
        headers=HEADER,
        data=json.dumps(
            {
                "GetGeneralInformation_Request_1": {
                    "companyId": organization_ric,
                    "companyIdType": "RIC",
                    "ShowReferenceInformation": False
                }
            }
        ),
        url="http://api.trkd.thomsonreuters.com/api/Fundamentals/Fundamentals.svc/REST/Fundamentals_1/GetGeneralInformation_1",
    )
    logging.info(r.json())
    return r


def organization_vs(d1, d2):
    r = requests.post(
        headers=HEADER,
        data=json.dumps(
            {
                "GetChart_Request_2": {
                    "chartRequest": {
                        "TimeSeries": {
                            "TimeSeriesRequest_typehint": [
                                "TimeSeriesRequest",
                                "TimeSeriesRequest"
                            ],
                            "TimeSeriesRequest": [
                                {
                                    "Symbol": d1,
                                    "Reference": "d1"
                                },
                                {
                                    "Symbol": d2,
                                    "Reference": "d2"
                                }
                            ]
                        },
                        "Analyses": {
                            "Analysis_typehint": [
                                "Analysis",
                                "Analysis"
                            ],
                            "Analysis": [
                                {
                                    "Reference": "a1",
                                    "PctCng": {
                                        "Instrument1": {
                                            "Reference": "d1"
                                        },
                                        "SpecifiedDate": "0001-01-01T00:00:00"
                                    }
                                },
                                {
                                    "Reference": "a2",
                                    "PctCng": {
                                        "Instrument1": {
                                            "Reference": "d2"
                                        },
                                        "SpecifiedDate": "0001-01-01T00:00:00"
                                    }
                                }
                            ]
                        },
                        "StandardTemplate": {
                            "Title": {
                                "Caption": {
                                    "Visible": True,
                                    "Customized": False
                                },
                                "Range": {
                                    "Visible": True
                                }
                            },
                            "Legend": {
                                "Visible": True,
                                "Information": "Long",
                                "Layout": "MultiLine",
                                "Position": "Overlaid"
                            },
                            "Instrument": "Symbol",
                            "Delimiter": "%",
                            "GridLines": "None",
                            "YAxisMarkers": "None",
                            "Interval": {
                                "CommonType": "Days",
                                "Multiplier": "1"
                            },
                            "ShowNonTradedPeriods": False,
                            "ShowHolidays": False,
                            "ShowGaps": True,
                            "XAxis": {
                                "Visible": True,
                                "Position": "Bottom",
                                "Range": {
                                    "Fixed": {
                                        "First": "2016-12-02T00:00:00",
                                        "Last": "2017-12-02T00:00:00"
                                    }
                                }
                            },
                            "Subchart": [
                                {
                                    "Weight": 5.0,
                                    "YAxis": [
                                        {
                                            "Visible": True,
                                            "Position": "Right",
                                            "Invert": False,
                                            "Logarithmic": False,
                                            "Display": {
                                                "Mode": "Automatic"
                                            },
                                            "Range": {
                                                "Automatic": ""
                                            },
                                            "Analysis": [
                                                {
                                                    "Reference": "a1"
                                                },
                                                {
                                                    "Reference": "a2"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "YAxisTitles": "",
                            "Brand": "None"
                        },
                        "Scheme": {
                            "Background": {
                                "BackgroundMode": "Solid",
                                "StartColor": {
                                    "Named": "White"
                                },
                                "EndColor": {
                                    "Named": "White"
                                },
                                "HatchStyle": "LargeGrid",
                                "GradientMode": "ForwardDiagonal",
                                "ImageMode": "Centered"
                            },
                            "Border": {
                                "Color": {
                                    "RGB": "139;139;155"
                                },
                                "DashStyle": "Solid",
                                "Width": 1.0
                            },
                            "GridLines": {
                                "Color": {
                                    "RGB": "139;139;155"
                                },
                                "DashStyle": "Dot",
                                "Width": 1.0
                            },
                            "Title": {
                                "Caption": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 12.0
                                },
                                "Range": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "Legend": {
                                "Color": {
                                    "Named": "Black"
                                },
                                "Family": "Arial",
                                "Style": "Regular",
                                "Size": 8.25
                            },
                            "XAxis": {
                                "Major": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 9.75
                                },
                                "Minor": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "YAxis": {
                                "Major": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Bold",
                                    "Size": 9.75
                                },
                                "Minor": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                },
                                "Title": {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "Family": "Arial",
                                    "Style": "Regular",
                                    "Size": 8.25
                                }
                            },
                            "Series": [
                                {
                                    "Color": {
                                        "Named": "Black"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "Named": "Black"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "Named": "Red"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "Named": "Red"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "62;169;0"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "62;169;0"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "156;38;115"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "156;38;115"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "255;120;0"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "255;120;0"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "25;108;229"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "25;108;229"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "60;117;28"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "60;117;28"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "230;176;18"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "230;176;18"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "0;186;193"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "0;186;193"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "255;178;127"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "255;178;127"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "100;79;190"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "100;79;190"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "209;36;33"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "209;36;33"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "38;87;135"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "38;87;135"
                                    },
                                    "FillStyle": "Percent20"
                                },
                                {
                                    "Color": {
                                        "RGB": "94;176;176"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 0.0,
                                    "FillColor": {
                                        "RGB": "94;176;176"
                                    },
                                    "FillStyle": "Percent20"
                                }
                            ],
                            "LevelLine": [
                                {
                                    "Color": {
                                        "RGB": "0;0;153"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 1.0
                                },
                                {
                                    "Color": {
                                        "RGB": "120;120;120"
                                    },
                                    "DashStyle": "Solid",
                                    "Width": 1.0
                                }
                            ]
                        },
                        "ImageType": "PNG",
                        "Width": 500,
                        "Height": 400,
                        "Culture": "en-US",
                        "ReturnPrivateNetworkURL": False
                    }
                }
            }
        ),
        url="http://api.trkd.thomsonreuters.com/api/Charts/Charts.svc/REST/Charts_1/GetChart_2",
    )
    logging.info(r)
    return r


def news():
    r = requests.post(
        headers=HEADER,
        data=json.dumps({"GetHeadlines_Request_2": {"Topic": "OLUSBUS"}}),
        url="http://api.trkd.thomsonreuters.com/api/OnlineReports/OnlineReports.svc/REST/OnlineReports_1/GetHeadlines_2",
    )
    logging.info(r.json())
    return r


@bot.message_handler(commands=['start', 'help'])
def send(message):
    bot.send_message(message.chat.id, text=START_MESSAGE)


@bot.message_handler(commands=['news'])
def send(message):
    news_ = json.loads(news().text)["GetHeadlines_Response_2"]["Story"]
    bot.send_message(message.chat.id, text='📰' + '📰 '.join([n["HL"]["T"][0] + '\n' for n in news_]))


@bot.message_handler(commands=['org'])
def send(message):
    organization_name_requested = message.text[5:]
    search_organization_output = search_organization(organization_name_requested)
    # logging.info(search_organization_output)
    print(json.loads(search_organization_output.text))

    organization_name = \
        json.loads(search_organization_output.text)['GetOrganisation_Response_1']['Result']['Hit'][0]['DocumentTitle'][
            0]['SubjectName']
    ric = json.loads(search_organization_output.text)['GetOrganisation_Response_1']['Result']['Hit'][0]['PrimaryRIC']

    query['ric'], query['name'], query['ginfo'] = ric, organization_name, organization_general_info(ric)

    g_info = query['ginfo']

    general_info = '''
📛Company Name: {company_name}
\t#️RIC: {ric}
\t👨‍💼Employees: {employees_number} on {employees_date}
\t🗺️Address: {address}
    '''.format(
        company_name=json.loads(g_info.text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["CompanyName"][
            "Value"],
        ric=ric,
        employees_number=
        json.loads(g_info.text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["CompanyGeneralInfo"][
            "Employees"]["Value"],
        employees_date=
        json.loads(g_info.text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["CompanyGeneralInfo"][
            "Employees"]["LastUpdated"],
        address=
        json.loads(g_info.text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["ContactInfo"]["Address"][
            "City"] + ', ' +
        json.loads(g_info.text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["ContactInfo"]["Address"][
            "StreetAddress"][0]["Value"]
        )

    bot.send_message(message.chat.id,
                     text=general_info + 'You have chosen {0} (it\'s RIC is {1}). Which information do you want to get?'.format(
                         organization_name,
                         ric),

                     reply_markup=markup,
                     )


@bot.message_handler(commands=['vs'])
def send(message):

    try:
        d1, d2 = message.text[4:].split()
        d1 = json.loads(search_organization(d1).text)['GetOrganisation_Response_1']['Result']['Hit'][0]['PrimaryRIC']
        d2 = json.loads(search_organization(d2).text)['GetOrganisation_Response_1']['Result']['Hit'][0]['PrimaryRIC']
        print(d1 + d2)
        logging.info("d1 = " + d1 + " d2=" + d2)
        vs = organization_vs(d1, d2)
        url_file = json.loads(vs.text)['GetChart_Response_2']['ChartImageResult']['Url']
        with open("{0}_vs_{1}.png".format(d1, d2), "wb") as f:
            f.write(requests.get(url_file).content)
        bot.send_photo(message.chat.id, open("{0}_vs_{1}.png".format(d1, d2), 'rb'))
    except:
        bot.send_message(message.chat.id, text="Please, check organizations' names!")


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'Chart':
        org_chart = organization_chart(query['ric'])
        logging.info(org_chart.json())
        url_file = json.loads(org_chart.text)['GetChart_Response_2']['ChartImageResult']['Url']
        with open("{0}.png".format(query['ric']), "wb") as f:
            f.write(requests.get(url_file).content)
        bot.send_photo(c.message.chat.id, open("{0}.png".format(query['ric']), 'rb'))

    elif c.data == 'Headlines':
        headlines_r = organization_headlines(query['ric'])
        headlines = json.loads(headlines_r.text)["RetrieveHeadlineML_Response_1"]["HeadlineMLResponse"]["HEADLINEML"]["HL"]
        bot.send_message(c.message.chat.id, text=html.unescape(
            ''.join(['❗' + headline['HT'].split('<')[0] + '\n' for headline in headlines])))

    elif c.data == 'Description':
        bot.send_message(c.message.chat.id, text=
        json.loads(query['ginfo'].text)["GetGeneralInformation_Response_1"]["GeneralInformation"]["TextInfo"]["Text"][0]["Value"])


# polling cycle
if __name__ == '__main__':
    while True:
        logging.info('The polling cycle has started!')
        try:
            bot.polling(none_stop=True)
        except requests.exceptions.ConnectionError as e:
            logging.warning('There was requests.exceptions.ConnectionError')
            time.sleep(15)
