import asyncio
import os
import sys
from pathlib import Path

import python_weather
import yaml


def detect_rain(weather):
    return any(
        any(w in str(f.type).lower() for w in ['rain', 'shower'])
        for f in next(weather.forecasts).hourly
    )


async def main():
    async with python_weather.Client(format=python_weather.METRIC) as client:
        if sys.platform.startswith("linux"):
            config_path = os.getenv("HOME") / Path('.butler.yaml')
        else:
            config_path = os.getenv("APPDATA") / Path('butler/butler.yaml')

        if not config_path.exists():
            config = {}
        else:
            config = yaml.safe_load(config_path.read_text())

        if 'city' not in config:
            config['city'] = input('What city are you in right now?\n')

        weather_future = client.get("New-Orleans")

        if 'username' not in config:
            config['username'] = input('How would you like me to call you?\n')

        print(", ".join([config.get('greeting', 'Welcome home'), config['username']]))

        weather = await weather_future

        kind_of_weather = weather.current.type.name

        print(f"The weather in {config['city']} is ", end="")
        if kind_of_weather in config.get('weather', {}).get('bad', []):
            print("terrible, I'm sorry.")
        elif kind_of_weather in config.get('weather', {}).get('good', []):
            print("nice, it could be a chance for a good walk.")
        else:
            print(kind_of_weather.lower() + ".")

        if weather.current.temperature >= config.get('hot_temperature', 30):
            print("It is hot today, dress lightly.")

        if detect_rain(weather):
            print("And there could be a rain, I suggest taking an umbrella.")

        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(yaml.safe_dump(config))


if __name__ == '__main__':
    if os.name == "nt":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    asyncio.run(main())
