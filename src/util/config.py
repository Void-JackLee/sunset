import os

lbs_config = {
    "use": os.getenv("LBS_USE"),
    "baidu": {
        "url": os.getenv("LBS_BAIDU_URL"),
        "ak": os.getenv("LBS_BAIDU_AK")
    },
    "tencent": {
        "url": os.getenv("LBS_TENCENT_URL"),
        "key": os.getenv("LBS_TENCENT_KEY")
    }
}
print(f'Use lbs backbone={lbs_config["use"]}')
