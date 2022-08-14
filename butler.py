import asyncio
import os
import python_weather


def detect_rain(weather):
    return any(
        any(w in str(f.type).lower() for w in ['rain', 'shower'])
        for f in next(weather.forecasts).hourly
    )


async def main():
    async with python_weather.Client(format=python_weather.METRIC) as client:
        weather_future = client.get("New-Orleans")
        print("Welcome home, Nikita")

        weather = await weather_future

        kind_of_weather = weather.current.type.name

        print("The weather in New-Orleans is ", end="")
        if kind_of_weather in ["Clear", "Sunny"]:
            print("terrible, I'm sorry.")
        elif kind_of_weather in ["Cloudy", "Partly cloudy"]:
            print("nice, it could be a chance for a good walk.")
        else:
            print(kind_of_weather.lower() + ".")

        if weather.current.temperature >= 30:
            print("It is hot today, dress lightly")

        if detect_rain(weather):
            print("And there could be a rain, I suggest taking an umbrella")


if __name__ == '__main__':
    if os.name == "nt":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    asyncio.run(main())
