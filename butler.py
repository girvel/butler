import asyncio
import os
import sys
from pathlib import Path

import python_weather
from tiny_storage import Unit


def detect_rain(weather):
    return any(
        any(w in str(f.type).lower() for w in ['rain', 'shower'])
        for f in next(weather.forecasts).hourly
    )


async def main():
    async with python_weather.Client(format=python_weather.METRIC) as client:
        config = Unit('butler')

        weather_future = client.get(config('city').put(lambda: input('What city are you in right now?\n')))

        print(", ".join([
            config('greeting').pull('Welcome home'),
            config('username').put(lambda: input('How would you like me to call you?\n'))
        ]))

        weather = await weather_future

        kind_of_weather = weather.current.type.name

        print(f"The weather in {config('city').pull()} is ", end="")
        if kind_of_weather in config('weather.bad').pull([]):
            print("terrible, I'm sorry.")
        elif kind_of_weather in config('weather.good').pull([]):
            print("nice, it could be a chance for a good walk.")
        else:
            print(kind_of_weather.lower() + ".")

        if weather.current.temperature >= config('hot_temperature').pull(30):
            print("It is hot today, dress lightly.")

        if detect_rain(weather):
            print("And there could be a rain, I suggest taking an umbrella.")


if __name__ == '__main__':
    if os.name == "nt":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    asyncio.run(main())
