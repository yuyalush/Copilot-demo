"""
東京の天気情報を取得するAPIクライアント
Tokyo Weather API Client

このモジュールはOpenWeatherMap APIを使用して東京の天気情報を取得します。
This module uses OpenWeatherMap API to fetch weather information for Tokyo.
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv


class TokyoWeatherClient:
    """東京の天気情報を取得するクライアント (Client for fetching Tokyo weather information)"""
    
    # 東京の座標 (Tokyo coordinates)
    TOKYO_LAT = 35.6762
    TOKYO_LON = 139.6503
    
    # OpenWeatherMap APIのベースURL (OpenWeatherMap API base URL)
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        クライアントを初期化する (Initialize the client)
        
        Args:
            api_key: OpenWeatherMap APIキー。指定しない場合は環境変数から読み込む
                     OpenWeatherMap API key. If not provided, reads from environment variable
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError(
                "APIキーが設定されていません。環境変数OPENWEATHER_API_KEYを設定するか、"
                "api_keyパラメータで指定してください。\n"
                "API key not set. Please set OPENWEATHER_API_KEY environment variable "
                "or provide api_key parameter."
            )
    
    def get_current_weather(self, units: str = "metric", lang: str = "ja") -> Dict:
        """
        東京の現在の天気情報を取得する (Get current weather information for Tokyo)
        
        Args:
            units: 温度の単位 (Temperature units)
                  - "metric": 摂氏 (Celsius)
                  - "imperial": 華氏 (Fahrenheit)
                  - "standard": ケルビン (Kelvin)
            lang: 言語コード (Language code) - 例: "ja" (日本語), "en" (English)
        
        Returns:
            天気情報を含む辞書 (Dictionary containing weather information)
        
        Raises:
            requests.RequestException: API呼び出しが失敗した場合
                                      (When API call fails)
        """
        params = {
            'lat': self.TOKYO_LAT,
            'lon': self.TOKYO_LON,
            'appid': self.api_key,
            'units': units,
            'lang': lang
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(
                f"天気情報の取得に失敗しました (Failed to fetch weather information): {e}"
            ) from e
    
    def get_formatted_weather(self, units: str = "metric", lang: str = "ja") -> str:
        """
        東京の天気情報を整形された文字列で取得する
        Get formatted weather information for Tokyo as a string
        
        Args:
            units: 温度の単位 (Temperature units) - "metric", "imperial", or "standard"
            lang: 言語コード (Language code)
        
        Returns:
            整形された天気情報の文字列 (Formatted weather information string)
        """
        data = self.get_current_weather(units=units, lang=lang)
        
        # 温度単位の記号を設定 (Set temperature unit symbol)
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        formatted = f"""
========================================
東京の天気情報 (Tokyo Weather Information)
========================================
天気: {weather_desc}
気温: {temp}{temp_unit}
体感温度: {feels_like}{temp_unit}
最低気温: {temp_min}{temp_unit}
最高気温: {temp_max}{temp_unit}
湿度: {humidity}%
風速: {wind_speed} m/s
========================================
"""
        return formatted.strip()


def main():
    """
    メイン関数 - 使用例を示す
    Main function - demonstrates usage
    """
    try:
        # クライアントを作成 (Create client)
        client = TokyoWeatherClient()
        
        # 天気情報を取得して表示 (Fetch and display weather information)
        print(client.get_formatted_weather())
        
        # 生のJSONデータも取得可能 (Raw JSON data is also available)
        # weather_data = client.get_current_weather()
        # print(weather_data)
        
    except ValueError as e:
        print(f"エラー (Error): {e}")
        print("\n使用方法 (Usage):")
        print("1. OpenWeatherMapでAPIキーを取得: https://openweathermap.org/api")
        print("2. .envファイルを作成して以下を記載:")
        print("   OPENWEATHER_API_KEY=your_api_key_here")
    except requests.RequestException as e:
        print(f"エラー (Error): {e}")


if __name__ == "__main__":
    main()
