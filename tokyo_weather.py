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
from colorama import Fore, Back, Style, init

# Coloramaを初期化 (Initialize colorama)
init(autoreset=True)


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
    
    def _get_weather_emoji(self, weather_desc: str) -> str:
        """
        天気の説明に基づいて絵文字を返す
        Return emoji based on weather description
        
        Args:
            weather_desc: 天気の説明 (Weather description)
            
        Returns:
            対応する絵文字 (Corresponding emoji)
        """
        weather_desc_lower = weather_desc.lower()
        
        # 天気状態に応じた絵文字マッピング (Emoji mapping based on weather conditions)
        if any(word in weather_desc_lower for word in ['晴', 'clear', 'sunny']):
            return '☀️'
        elif any(word in weather_desc_lower for word in ['雲', 'cloud', '曇']):
            return '☁️'
        elif any(word in weather_desc_lower for word in ['雨', 'rain', 'drizzle']):
            return '🌧️'
        elif any(word in weather_desc_lower for word in ['雪', 'snow']):
            return '❄️'
        elif any(word in weather_desc_lower for word in ['雷', 'thunder', 'storm']):
            return '⚡'
        elif any(word in weather_desc_lower for word in ['霧', 'fog', 'mist', 'haze']):
            return '🌫️'
        else:
            return '🌤️'
    
    def _get_temp_color(self, temp: float) -> str:
        """
        温度に基づいて色を返す
        Return color based on temperature
        
        Args:
            temp: 温度 (Temperature in Celsius)
            
        Returns:
            ANSI色コード (ANSI color code)
        """
        if temp >= 30:
            return Fore.RED + Style.BRIGHT  # 暑い (Hot)
        elif temp >= 25:
            return Fore.YELLOW + Style.BRIGHT  # 暖かい (Warm)
        elif temp >= 15:
            return Fore.GREEN + Style.BRIGHT  # 快適 (Comfortable)
        elif temp >= 5:
            return Fore.CYAN + Style.BRIGHT  # 涼しい (Cool)
        else:
            return Fore.BLUE + Style.BRIGHT  # 寒い (Cold)
    
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
        
        # 天気絵文字を取得 (Get weather emoji)
        weather_emoji = self._get_weather_emoji(weather_desc)
        
        # 温度の色を取得 (Get temperature color)
        temp_color = self._get_temp_color(temp) if units == "metric" else Fore.YELLOW + Style.BRIGHT
        
        # ボックス描画文字 (Box drawing characters)
        top_line = "╔" + "═" * 58 + "╗"
        bottom_line = "╚" + "═" * 58 + "╝"
        
        # カラフルで豪華な出力を作成 (Create colorful and luxurious output)
        formatted = f"""
{Fore.CYAN + Style.BRIGHT}{top_line}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW + Style.BRIGHT}🌏  東京の天気情報  Tokyo Weather Information  🌏{Style.RESET_ALL}    {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN + Style.BRIGHT}╠{"═" * 58}╣{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {weather_emoji}  {Fore.WHITE + Style.BRIGHT}天気:{Style.RESET_ALL} {Fore.MAGENTA + Style.BRIGHT}{weather_desc:^45s}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╠{"─" * 58}╣{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}🌡️  気温:{Style.RESET_ALL}         {temp_color}{temp:>6.1f}{temp_unit}{Style.RESET_ALL}                              {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}👤 体感温度:{Style.RESET_ALL}     {temp_color}{feels_like:>6.1f}{temp_unit}{Style.RESET_ALL}                              {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}❄️  最低気温:{Style.RESET_ALL}     {Fore.BLUE + Style.BRIGHT}{temp_min:>6.1f}{temp_unit}{Style.RESET_ALL}                              {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}🔥 最高気温:{Style.RESET_ALL}     {Fore.RED + Style.BRIGHT}{temp_max:>6.1f}{temp_unit}{Style.RESET_ALL}                              {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╠{"─" * 58}╣{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}💧 湿度:{Style.RESET_ALL}         {Fore.LIGHTBLUE_EX + Style.BRIGHT}{humidity:>5d}%{Style.RESET_ALL}                                {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE + Style.BRIGHT}💨 風速:{Style.RESET_ALL}         {Fore.LIGHTGREEN_EX + Style.BRIGHT}{wind_speed:>5.1f} m/s{Style.RESET_ALL}                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                          {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN + Style.BRIGHT}{bottom_line}{Style.RESET_ALL}
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
